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
printed_lines = []
main_line = ""

def downloading_pip_libs(libs):
    global main_line
    main_line = "Downloading required python libraries"
    clear_console()
    for lib in libs:
        new_print(f"Downloading {lib} library . . .")
        result = subprocess.run(["pip", "install", lib], capture_output=True, text=True)
        if result.returncode != 0:
            new_print("Error installing library:", lib)
            new_print("ERROR MESSAGE: ")
            new_print(result.stdout)
            new_print(result.stderr)
            new_print("Installation will be aborted.")
            sys.exit()

def new_print(text):
    os.system("cls")
    printed_lines.append(text)
    print("BOTMAKER INSTALLER")
    print(main_line)
    print()
    for t in printed_lines:
        print(t)

def remove_read_only(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    func(path)

def clear_console():
    printed_lines = []
    os.system("cls")
    print("BOTMAKER INSTALLER")
    print(main_line)


def download_newest_files(path):
    global main_line
    main_line = "Creating BotMaker App"
    clear_console()
    if os.path.isdir(path):
        shutil.rmtree(path, onerror=remove_read_only)
    os.makedirs(path)
    repo_url = "https://github.com/123Maciek/BotMaker"
    new_print("Downloading newest BotMaker files . . .")
    try:
        git.Repo.clone_from(repo_url, path)
    except Exception as e:
        pass

downloading_pip_libs(requirements)

documents_path = Path(os.getenv('USERPROFILE')) / 'Documents'
folder_path = str(documents_path) + "\\BotMakerFiles\\"

download_newest_files(folder_path)
new_print("Creating BotMaker Desktop shortcut . . .")
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

main_line = "Instalation finished :)"
clear_console()
print()