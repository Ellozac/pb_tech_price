import os
import sys


def install_dependencies():
    if os.uname().sysname.lower() == "linux":
        user_system = "linux"
    elif os.uname().sysname.low() == "windows":
        user_system = "windows"
    try:
        os.system("curl -ssLJO https://raw.githubusercontent.com/Ellozac/pb_tech_price/main/requirements.txt && python -m pip install -r requirements.txt")
    except Exception as e:
        print(f"error installing dependencies exited with error:\n{e}")


install_dependencies()
