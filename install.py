import requests
import git
import os
import sys
import shutil
import winshell
from win32com.client import Dispatch

def download_newest_files(path):
    repo_url = "https://github.com/123Maciek/BotProgrammer"
    try:
        git.Repo.clone_from(repo_url, path)
    except Exception as e:
        pass

download_newest_files("C:\\Program Files\\BotMaker")
with open("C:\\Program Files\\BotMaker\\start.bat", 'w') as file:
    file.write("@echo off\n")
    file.write('cd "C:\\Program Files\\BotMaker"\n')
    file.write('py "C:\\Program Files\\BotMaker\\main.py"')

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

create_shortcut("C:\\Program Files\\BotMaker\\window.vbs", "BotMaker", icon_path="C:\\Program Files\\BotMaker\\icon.ico")