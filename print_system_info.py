import os
from os.path import expanduser

DOCKER_SETTINGS = f"{expanduser('~')}/Library/Group Containers/group.com.docker/settings.json"


def main():
    print("### Docker Settings")
    print(_read_file(DOCKER_SETTINGS))
    print("\n### Docker System DF")
    os.system('docker system df')
    print("\n### df -h /var/lib/docker")
    os.system('df -h /var/lib/docker')
    print("\n### docker stats --no-stream")
    os.system('docker stats --no-stream')
    print("\n### cat docker_logs/output.log")
    os.system('cat docker_logs/output.log')
    print("\n### docker logs backend-web-1")
    os.system('docker logs backend-web-1')
    print("\n### cat logs/logs.log")
    os.system('cat logs/logs.log')


def _read_file(file_path):
    try:
        with open(file_path) as file:
            return file.read()
    except Exception:
        pass


if __name__ == '__main__':
    main()