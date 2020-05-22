import shlex
import subprocess
import os
import signal

proc = None


def handle_SIGINT(signum, frame):
    if proc:
        proc.send_signal(signal.SIGINT)
    print()


signal.signal(signal.SIGINT, handle_SIGINT)

while True:
    try:
        cmd = input("> ")
    except EOFError:
        print("\nBye")
        break

    args = shlex.split(cmd)

    if not args:
        continue

    if args[0] == "cd":
        if len(args) > 1:
            os.chdir(args[1])
        else:
            os.chdir(os.environ["HOME"])
        continue

    try:
        proc = subprocess.Popen(args, stdout=subprocess.PIPE)
    except FileNotFoundError:
        print(args[0], "not found")
        continue
    except subprocess.CalledProcessError as e:
        print(e.stderr.decode(), end="")
        continue

    print(proc.communicate()[0].decode(), end="")
