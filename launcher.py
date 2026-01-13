import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import shutil
import gdown
import requests

# =============================
# CONFIGURATION
# =============================

ETS2_EXE = r"C:\Program Files (x86)\Steam\steamapps\common\Euro Truck Simulator 2\bin\win_x64\eurotrucks2.exe"
MOD_FOLDER = os.path.expanduser(
    r"~/Documents/Euro Truck Simulator 2/mod"
)

ONLINE_VERSION_URL = "https://raw.githubusercontent.com/RobayetFerdous/ets2_launcher/refs/heads/main/version.txt"
MOD_DRIVE_URL = "https://drive.google.com/uc?id=1ms1YCJUNA8vUmsENcKZJVlfde2KZG82e"
LOCAL_VERSION_FILE = "version.txt"
TEMP_MOD = "temp_mod.scs"

# =============================
# FUNCTIONS
# =============================

def launch_game():
    if os.path.exists(ETS2_EXE):
        subprocess.Popen(ETS2_EXE)
    else:
        messagebox.showerror("Error", "ETS2 executable not found!")

def get_local_version():
    if not os.path.exists(LOCAL_VERSION_FILE):
        return "0"
    with open(LOCAL_VERSION_FILE, "r") as f:
        return f.read().strip()

def get_online_version():
    response = requests.get(ONLINE_VERSION_URL)
    return response.text.strip()

def check_update():
    try:
        local = get_local_version()
        online = get_online_version()

        if local == online:
            messagebox.showinfo("Update", "Your mod is already up to date!")
            return

        messagebox.showinfo("Update", "New update found! Downloading...")

        # Download mod from Google Drive
        gdown.download(MOD_DRIVE_URL, TEMP_MOD, quiet=False)

        # Ensure mod folder exists
        os.makedirs(MOD_FOLDER, exist_ok=True)

        # Move mod
        shutil.move(TEMP_MOD, os.path.join(MOD_FOLDER, "updated_mod.scs"))

        # Update local version
        with open(LOCAL_VERSION_FILE, "w") as f:
            f.write(online)

        messagebox.showinfo("Success", "Update installed successfully!")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# =============================
# GUI
# =============================

root = tk.Tk()
root.title("ETS2 Launcher")
root.geometry("300x180")
root.resizable(False, False)

tk.Label(root, text="ETS2 Custom Launcher", font=("Arial", 14)).pack(pady=10)

tk.Button(root, text="Launch Game", width=20, command=launch_game).pack(pady=5)
tk.Button(root, text="Check Update", width=20, command=check_update).pack(pady=5)

root.mainloop()
