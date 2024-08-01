import requests
import git
import os
import sys
import shutil
import winshell
from pathlib import Path
from win32com.client import Dispatch
import subprocess
import stat

requirements = ["winshell", "pywin32", "pathlib", "requests", "gitpython", "pyautogui", "Pillow", "pynput", "keyboard", "pyperclip", "pygithub"]

print("BOTMAKER INSTALLER")
print()

def downloading_pip_libs(libs):
    for lib in libs:
        print(f"Downloading {lib} library . . .")
        result = subprocess.run(["pip", "install", lib], capture_output=True, text=True)
        if result.returncode != 0:
            print("Error installing library:", lib)
            print("ERROR MESSAGE: ")
            print(result.stdout)
            print(result.stderr)
            print("Installation will be aborted.")
            sys.exit()


def remove_read_only(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    func(path)

def download_newest_files(path):
    if os.path.isdir(path):
        shutil.rmtree(path, onerror=remove_read_only)
    os.makedirs(path)
    repo_url = "https://github.com/123Maciek/BotMaker"
    print("Downloading newest BotMaker files . . .")
    try:
        git.Repo.clone_from(repo_url, path)
    except Exception as e:
        pass

downloading_pip_libs(requirements)

documents_path = Path(os.getenv('USERPROFILE')) / 'Documents'
folder_path = str(documents_path) + "\\BotMakerFiles\\"

download_newest_files(folder_path)
print("Creating BotMaker Desktop shortcut . . .")
with open(f"{folder_path}start.bat", 'w') as file:
    file.write("@echo off\n")
    file.write(f'cd "{folder_path}"\n')
    file.write(f'py "{folder_path}main.py"')

def create_shortcut(target_file, shortcut_name, icon_path=None):
    desktop = winshell.desktop()
    path = os.path.join(desktop, f"{shortcut_name}.lnk")
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(path)
    shortcut.TargetPath = target_file
    shortcut.WorkingDirectory = os.path.dirname(target_file)
    if icon_path:
        shortcut.IconLocation = icon_path
    shortcut.save()

create_shortcut(f"{folder_path}window.vbs", "BotMaker", icon_path=f"{folder_path}icon.ico")

print("Instalation finished succesfully :)")