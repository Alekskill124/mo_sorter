import os
import winreg
import configparser

from tkinter import filedialog
from tkinter import messagebox

def is_valid_mo_path(mo_path):
    try:
        for paths, folders, files in os.walk(mo_path):
            if "ModOrganizer.exe" in files and "mods" in folders:
                return True
            else:
                break
    except TypeError:
        return False

def is_valid_mo_profile(mo_path, mo_profile):
    profiles = get_profiles(mo_path)
    return mo_profile in profiles

def get_mo_path():
    
    path = ""

    try:
        REG_PATH = r"nxm\\shell\\open\\command"

        registry_key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, REG_PATH)
        value, regtype = winreg.QueryValueEx(registry_key, None)

        started = 0
        for i in value:
            if started == 0 and i == '"':
                started = 1
            elif started == 1 and i == '"':
                started = 0
                break
            else:
                path += str(i)
   
        for i in path[::-1]:
            path = path[:-1:]

            if i == '\\':
                break

        winreg.CloseKey(registry_key)
    except:
        pass
       
    while not is_valid_mo_path(path):
        path = filedialog.askdirectory(title="Select your ModOrganizer folder")
        if (path == ""):
            exit()

    return path

def get_master_profile(mo_path):
    ConfigParser = configparser.SafeConfigParser()
    ConfigParser.add_section("General")

    ConfigParser.read(mo_path + "\\ModOrganizer.ini")
    try:
        master_profile = ConfigParser.get("General", "selected_profile")
    except configparser.NoOptionError:
        master_profile = None
    
    return master_profile

def get_profiles(mo_path): 
    if not is_valid_mo_path(mo_path):
        exit()
    profiles = next(os.walk(mo_path + "\\profiles"))[1]
    return profiles
