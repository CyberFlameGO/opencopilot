import os
import json
import time
import re
import urllib.request
import argparse
from typing import List, Dict

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.unity.sidekik.ai/")
UNITY_LOG_FILE_PATH = os.path.expanduser('~/Library/Logs/Unity/Editor.log')
LOG_LINES_TO_INCLUDE = 20


def _send_info(conversation_id: str, info: Dict) -> bool:
    try:
        data = {
            "context": json.dumps(info) 
        }
        data_json = json.dumps(data)
        data_bytes = data_json.encode('utf-8')  # convert string to bytes
        req = urllib.request.Request(f"{API_BASE_URL}v0/conversation/{conversation_id}/context")
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        req.add_header('Content-Length', len(data_bytes))
        response = urllib.request.urlopen(req, data_bytes)
        response_json = json.loads(response.read())
        return response_json["response"] == "OK"
    except Exception as e:
        print(f"Error sending information to Unity Copilot: {str(e)}")
        return False


def _walk_folder_tree(directory, abs_path):
    all_files_folders = []
    for root, dirs, files in os.walk(os.path.join(abs_path, directory)):
        relative_root = os.path.relpath(root, abs_path)
        for name in files:
            all_files_folders.append(os.path.join(relative_root, name))
        for name in dirs:
            all_files_folders.append(os.path.join(relative_root, name))

    return all_files_folders


def _get_packages(project_path: str):
    try:
        with open(f"{project_path}/Packages/packages-lock.json", "r") as f:
            return json.load(f)
    except:
        return {}


def _get_directory_tree(project_path):
    directories = ["Assets", "ProjectSettings", "Packages"]

    tree = []
    for directory in directories:
        tree.extend(_walk_folder_tree(directory, project_path))
    return tree


def _extract_info(line):
    pattern = r'\w+:\s+(?:Info\s+)?(?P<Info>.*)'
    info = re.search(pattern, line)
    return info.group('Info') if info else None


def _parse_os_unity_info(data: List[str]) -> Dict:
    '''
        Unity Editor version:    2021.3.28f1 (232e59c3f087)
        Branch:                  2021.3/release
        Build type:              Release
        Batch mode:              NO
        macOS version:           Version 13.2 (Build 22D49)
        Darwin version:          22.3.0
        Architecture:            arm64
        Running under Rosetta:   NO
        Available memory:        16384 MB
    '''

    return {
        "unity_version": _extract_info(data[0]),
        "macOS_version": _extract_info(data[4]),
        "darwin version": _extract_info(data[5]),
        "architecture": _extract_info(data[6]),
        "rosetta": _extract_info(data[7]) == "YES",
        "available_memory_mb": int(_extract_info(data[8]).split()[0]) 
    }


def _process_log_file() -> Dict:
    try:
        with open(UNITY_LOG_FILE_PATH, 'r') as file:
            lines = file.readlines()
            # extract OS and Unity information
            info = _parse_os_unity_info(lines[:9])
            # scan the log to find project information
            project_path = None
            for i, line in enumerate(lines):
                if '-projectpath' in line or "-createproject" in line:
                    project_path = re.findall(r'(/[\w\W]*)', lines[i+1])
                    break
            if project_path:
                project_path = project_path[0].strip()
                packages = _get_packages(project_path)
                project_structure = _get_directory_tree(project_path)
                # put everything together
                info["project_path"] = project_path
                info["project_structure"] = project_structure
                info["packages"] = packages
            info["editor_log"] = lines[-LOG_LINES_TO_INCLUDE:]
            return info
    except FileNotFoundError:
        print(f"{UNITY_LOG_FILE_PATH} does not exist.")
    except PermissionError:
        print(f"Permission denied for {UNITY_LOG_FILE_PATH}.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def _monitor_unity_log_file() -> Dict:
    last_log_mt = None
    last_package_mt = None
    current_package_mt = None
    packages_file = None

    while True:
        try:
            # Check if the file has been modified
            current_log_mt = os.path.getmtime(UNITY_LOG_FILE_PATH)
            if packages_file:
                current_package_mt = os.path.getmtime(packages_file)
            if last_log_mt != current_log_mt or last_package_mt != current_package_mt:
                # modified, get info
                last_log_mt = current_log_mt
                last_package_mt = current_package_mt
                info = _process_log_file()
                if "project_path" in info:
                    packages_file = f"{info['project_path']}/Packages/packages-lock.json"
                yield info
        except FileNotFoundError:
            print(f"{UNITY_LOG_FILE_PATH} does not exist.")
            return
        except PermissionError:
            print(f"Permission denied for {UNITY_LOG_FILE_PATH}.")
            return
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return

        # Pause for a bit
        time.sleep(2)


def main(conversation_id: str):
    for info in _monitor_unity_log_file():
        _send_info(conversation_id, info)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "conversation_id",
        type=str
    )
    args = parser.parse_args()
    main(args.conversation_id)
