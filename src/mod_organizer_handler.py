import os
import winreg

from tkinter import filedialog
from tkinter import messagebox

def is_valid_mo_path(path):
    try:
        for paths, folders, files in os.walk(path):
            if "ModOrganizer.exe" in files and "mods" in folders:
                return True
            else:
                break
    except TypeError:
        return False

def is_valid_mo_profile(mo_path, mo_profile):
    profiles = get_profiles(mo_path)
    return mo_profile in profiles

def get_mo_path(current_path):
    path = current_path

    if not is_valid_mo_path(current_path):
        REG_PATH = r"nxm\\shell\\open\\command"

        registry_key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, REG_PATH)
        value, regtype = winreg.QueryValueEx(registry_key, None)

        temp_path = ""
        started = 0
        for i in value:
            if started == 0 and i == '"':
                started = 1
            elif started == 1 and i == '"':
                started = 0
                break
            else:
                temp_path += str(i)

        for i in temp_path[::-1]:
            temp_path = temp_path[:-1:]

            if i == '\\':
                break

        if is_valid_mo_path(temp_path):
            path = temp_path

        winreg.CloseKey(registry_key)

    while not is_valid_mo_path(path):
        path = filedialog.askdirectory(title="Select your ModOrganizer folder")
        if (path == ""):
            exit()

    return path

def get_master_profile(current_profile, current_path):
    if not is_valid_mo_profile(current_path, current_profile):
        return "None"
    return current_profile

def get_profiles(mo_path):
    if not is_valid_mo_path(mo_path):
        exit()
    profiles = next(os.walk(mo_path + "\\profiles"))[1]
    return profiles
