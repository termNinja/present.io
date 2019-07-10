class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def regular_msg(msg: str) -> None:
    """Prints out a blue colored message to standard output."""
    print(f"{bcolors.OKBLUE} {msg} {bcolors.ENDC}")


def success_msg(msg: str) -> None:
    """Prints out a green colored message to standard output."""
    print(f"{bcolors.OKGREEN} {msg} {bcolors.ENDC}")


def fail_msg(msg: str) -> None:
    """Prints out a red colored message to standard output."""
    print(f"{bcolors.FAIL} {msg} {bcolors.ENDC}")


def warn_msg(msg: str) -> None:
    """Prints out a yellowish colored message to standard output."""
    print(f"{bcolors.WARNING} {msg} {bcolors.ENDC}")