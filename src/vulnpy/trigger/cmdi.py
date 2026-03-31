import shlex
import subprocess

ALLOWED_COMMANDS = {"echo", "ls", "whoami", "date", "uname"}


def _validate_command(command):
    args = shlex.split(command)
    if not args:
        raise ValueError("Empty command")
    if args[0] not in ALLOWED_COMMANDS:
        raise ValueError(f"Command '{args[0]}' is not allowed")
    return args


def do_os_system(command):
    args = _validate_command(command)
    result = subprocess.run(args, capture_output=True, text=True)
    return result.returncode


def do_subprocess_popen(command):
    args = _validate_command(command)
    process = subprocess.Popen(
        args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    stdout, _ = process.communicate()
    return stdout
