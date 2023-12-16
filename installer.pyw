import os
import sys
import platform


def install_dependencies():
    user_system = platform.system().lower()
    print(user_system)
    try:
        os.system("curl -ssLJO https://raw.githubusercontent.com/Ellozac/pb_tech_price/main/requirements.txt && python -m pip install -r requirements.txt")
        os.remove("requirements.txt")
    except Exception as e:
        print(f"error installing dependencies exited with error:\n{e}")


install_dependencies()
