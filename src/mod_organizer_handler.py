import os
import winreg
import configparser

from tkinter import filedialog
from tkinter import messagebox

def is_valid_mo_path(mo_path):
    try:
        for paths, folders, files in os.walk(mo_path):
            if "ModOrganizer.exe" in files and "mods" in folders and "profiles" in folders:
                return True
            else:
                return False
    except TypeError:
        return False

def is_valid_mo_profile(mo_path, mo_profile):
    profiles = get_profiles(mo_path)
    return mo_profile in profiles

def get_mo_path(force_get=False):
    
    path = ""

    try:
        REG_PATH = r"nxm\\shell\\open\\command"

        registry_key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, REG_PATH)
        value, regtype = winreg.QueryValueEx(registry_key, None)
        
        # We expect the format to be - '"C:\...\nxmhandler.exe" "%x"'
        path = value.split("\"")[1]
        # nxmhandler.exe is not needed, remove it
        path = path[:-len("nxmhandler.exe"):]

        winreg.CloseKey(registry_key)
    except:
        pass

    if force_get:
        # If force_get is enabled, no is not an answer, we must return path or exit

        while not is_valid_mo_path(path):
            path = filedialog.askdirectory(title="Select your ModOrganizer folder")

            # If user just closes the dialog, don't ask again, exit
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
        return []
    profiles = next(os.walk(mo_path + "\\profiles"))[1]
    return profiles
