import subprocess
import os
import platform
import sys


def beep():
    if platform.system() == "Windows":
        import winsound
        winsound.Beep(1000, 200)
    else:
        sys.stdout.write("\a")
        sys.stdout.flush()

def clear():
    command = "clear"
    if os.name == "nt":
        command = "cls"
    subprocess.call(command, shell=True)