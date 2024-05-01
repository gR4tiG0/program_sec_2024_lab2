import ctypes
import wmi
import hashlib
import os
import tkinter
from tkinter import filedialog
import subprocess
import shutil
import winreg

SOURCE_DIR = "./lab1_sources"


def get_system_info_hash() -> str:
    mouse_buttons = ctypes.windll.user32.GetSystemMetrics(43)
    screen_height = ctypes.windll.user32.GetSystemMetrics(1)

    c = wmi.WMI()
    disk_info = [(disk.Caption, disk.VolumeSerialNumber) for disk in c.Win32_LogicalDisk()]

    username = os.getlogin()
    compname = os.environ['COMPUTERNAME']

    windows_folder = os.environ['WINDIR']
    system32_folder = os.path.join(windows_folder, 'System32')


    info_str = f"{username}{compname}{windows_folder}{system32_folder}{mouse_buttons}{screen_height}{disk_info}"



    print(info_str)

    info_hash = hashlib.sha256(info_str.encode()).hexdigest()

    return info_hash

def install_lab(dest:str) -> None:
    sysinf_hash = get_system_info_hash()
    key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Prikhodko")
    winreg.SetValueEx(key, 'signature', 0, winreg.REG_SZ, sysinf_hash)
    winreg.CloseKey(key)
    subprocess.check_call(['pyinstaller','--onefile', f"{SOURCE_DIR}/main.py"])
    shutil.rmtree('build')
    os.remove('main.spec')
    try:
        shutil.move('dist/main.exe', os.path.join(dest, 'lab1.exe'))
        os.mkdir(os.path.join(dest, 'json'))
    except:
        pass
    shutil.rmtree('dist')



def main() -> None:

    root = tkinter.Tk()
    root.withdraw()

    tkinter.messagebox.showinfo("Welcome", "Welcome to Lab 1 installer")
    tkinter.messagebox.showinfo("Installation", "Where to install app?")

    dest_folder = filedialog.askdirectory()

    if dest_folder:
        install_lab(dest_folder)
        tkinter.messagebox.showinfo("Installation", "Installation complete in " + dest_folder)

    root.destroy()

if __name__ == "__main__":
    main()