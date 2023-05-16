import os
import shutil

from win32com.client import Dispatch


# # get the current users username
username = os.getlogin()
# # get the current users startup folder
startup_folder = f"C:\\Users\\{username}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
current_directory = os.getcwd()
shell = Dispatch('Wscript.Shell')
shortcut = shell.CreateShortCut(f"{current_directory}\\checker.lnk")
shortcut.Targetpath = f"{current_directory}\\dist\\checker\\checker.exe"
if os.path.exists(f"{startup_folder}\\checker.lnk") == False:
    shortcut.save()
if os.path.exists(f"{startup_folder}\\checker.lnk") == False:
    shutil.move(f"{current_directory}\\checker.lnk", startup_folder)

shortcut = shell.CreateShortCut(f"{current_directory}\\adder.lnk")
shortcut.Targetpath = f"{current_directory}\\dist\\adder.exe"
shortcut.save()






