import sys
sys.path.append(".\\Skyrim Library\\")

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

import os
import time

from file_io import *
from mod_organizer_handler import *
from sort import *

ConfigFile     = "MOSorter_config.ini"
ConfigSettings = {"mo_install_path" : "None",
                  "master_profile" : "None",
                  "show_help" : "True"}

AllProfiles = []

HelpMessage = "Select the profile by which the others will be sorted and press \"Sort Mods\" button. After everything is done a notification should appear. \n\nTo show this window again, press the \"Help\" button"

# Setting up window
root = Tk()
root.wm_title("Mod Organizer Sorter")
root.minsize(310, 122)

# Probably not the cleanest icon loading solution,
# but at least .ico file does not have to be supplied
from base64 import b64decode
icon_path = "icon_temp.ico"
icon = """AAABAAEAEBAAAAAACABoBQAAFgAAACgAAAAQAAAAIAAAAAEACAAAAAAAAAEAAAAAAAAAAAAAAAEAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP//AACQAQAAkAEAAP//AACQAQAAkAEAAP//AACQAQAAkAEAAP//AACQAQAAkAEAAP//AACQAQAAkAEAAP//AAA="""
icon_data = b64decode(icon)

with open(icon_path, "wb") as icon_file:
    icon_file.write(icon_data)
root.iconbitmap(icon_path)
os.remove(icon_path)

def start():

    ConfigSettings["mo_install_path"] = read_config(ConfigFile, "mo_install_path")
    ConfigSettings["mo_install_path"] = get_mo_path(ConfigSettings["mo_install_path"])

    ConfigSettings["master_profile"] = read_config(ConfigFile, "master_profile")
    ConfigSettings["master_profile"] = get_master_profile(ConfigSettings["master_profile"], ConfigSettings["mo_install_path"])

    #Try to get master_profile from currently selected profile in MO
    temp_profile = read_config_new(ConfigSettings["mo_install_path"] + "\\ModOrganizer.ini", "General", "selected_profile")
    if temp_profile:
        ConfigSettings["master_profile"] = temp_profile

    ConfigSettings["show_help"] = read_config(ConfigFile, "show_help")
    if not ConfigSettings["show_help"] == "False":
        ConfigSettings["show_help"] = "True"

    write_config(ConfigFile, ConfigSettings)

    AllProfiles = get_profiles(ConfigSettings["mo_install_path"])

    frame = Frame(root)
    frame.pack()

    option = StringVar(frame)
    option.set(ConfigSettings["master_profile"])
    profile_pick = OptionMenu(frame, option, *tuple(AllProfiles))
    profile_pick.pack()

    sort_button = Button(frame, text="Sort Mods", fg="red", padx=40, pady=10,
                    command=lambda:sort(ConfigSettings["mo_install_path"], option.get(), AllProfiles, root))
    sort_button.pack()

    help_button = Button(frame, text="Help",
                    command=lambda:show_help(HelpMessage))
    help_button.pack(side=LEFT, pady=10)

    # First time help
    if ConfigSettings["show_help"] == "True":
        show_help(HelpMessage)
        ConfigSettings["show_help"] = "False"

    root.mainloop()

    # Cleanup code... Ini writing
    ConfigSettings["master_profile"] = option.get()
    write_config(ConfigFile, ConfigSettings)

def show_help(message):
    messagebox.showinfo("Help", HelpMessage)

if __name__ == "__main__":
    start()
