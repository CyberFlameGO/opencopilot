from typing import List, Optional

# ANSI escape sequences for some colors
YELLOW = "\033[33m"
RED = "\033[31m"
GREEN = "\033[32m"
BLUE = "\033[34m"
RESET = "\033[0m"  # Reset color


def print_green(msg: str):
    print(f"{GREEN}{msg}{RESET}")


def print_red(msg: str):
    print(f"{RED}{msg}{RESET}")


def print_yellow(msg: str):
    print(f"{YELLOW}{msg}{RESET}")


def select(choices: List[str]) -> Optional[int]:
    while True:
        for i, choice in enumerate(choices):
            print(f"{i + 1}) {choice}")
        try:
            selection = int(input("-> "))
            if selection in range(1, len(choices) + 1):
                return selection - 1
        except KeyboardInterrupt:
            return None
        except:
            pass
