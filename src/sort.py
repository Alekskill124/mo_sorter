import os
import time

from tkinter import messagebox

my_file_name = "modorganizersorter_modlist.txt"

def overwrite(modlist_current_path, your_modlist_path):
    os.replace(modlist_current_path, your_modlist_path + ".BAK")
    os.replace(your_modlist_path, modlist_current_path)

def equalize(master_profile_path, profile_path):
    try:
        mp_file = open(master_profile_path + "\\modlist.txt", 'r')
    except:
        message = "Your master profile is missing modlist configuration. Please reopen Mod Organizer with desired profile selected"
        done_box = DialogBox(parent_window, message)
        exit()

    try:
        p_file = open(profile_path + "\\modlist.txt", 'r')
    except:
        p_file = open(profile_path + "\\modlist.txt", 'w+')

    my_file = open(profile_path + "\\" + my_file_name, 'w+')

    for i_mp, line_mp in enumerate(mp_file):
        if line_mp[0] != '-' and line_mp[0] != '+':
            my_file.write(line_mp)
        else:
            current_mod = line_mp[1:]
            current_sign = '-'
            for i_p, line_p in enumerate(p_file):
                if current_mod in line_p:
                    current_sign = line_p[0]
                    break
            my_file.write(current_sign + current_mod)
            p_file.seek(0)

    mp_file.close()
    p_file.close()
    my_file.close()

    p_file_path = p_file.name
    my_file_path = my_file.name
    overwrite(p_file_path, my_file_path)

def sort(mo_path, master_profile, profiles, parent_window):
    if master_profile not in profiles:
        # TODO: Error
        exit()

    profiles.remove(master_profile)

    for profile in profiles:
        equalize(mo_path + "\\profiles\\" + master_profile, mo_path + "\\profiles\\" + profile)

    profiles.append(master_profile)

    message = "All done!"
    messagebox.showinfo("Info", message)
