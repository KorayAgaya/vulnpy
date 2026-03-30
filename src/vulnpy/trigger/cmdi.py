import shlex
import subprocess


def do_os_system(command):
    args = shlex.split(command)
    result = subprocess.run(args, capture_output=True, text=True)
    return result.returncode


def do_subprocess_popen(command):
    args = shlex.split(command)
    process = subprocess.Popen(
        args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    stdout, _ = process.communicate()
    return stdout
