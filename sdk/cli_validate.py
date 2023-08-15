"""
TODO: What dependencies are needed...

"""
import os.path

from opencopilot.src.domain.copilot import validate_copilot_files
from opencopilot.src.domain.copilot.validate_copilot_files import ValidateCopilotResult
from sdk.utils import env_utils, print_utils


def main() -> bool:
    if not env_utils.get_copilot_name():
        print_utils.print_red("No Copilot found.")
        return False

    if path := env_utils.get_copilot_path():
        if not os.path.exists(path):
            print_utils.print_red(f"No copilot found on path: {path}")
            return False

    data_path = env_utils.get_copilot_path()
    result = validate_copilot_files.execute(data_path)
    if result.is_valid:
        print_utils.print_green("Configuration is valid.")
        return True
    else:
        print_utils.print_red("Configuration is broken.")
        _print_errors(result)
        return False


def _print_errors(result: ValidateCopilotResult):
    for error_result in result.error_results:
        print(f"  {error_result.error_message}")
