import subprocess
import win32con
import win32gui # pip install pywin32
import time
from importlib import import_module
from params import read_monitors, valid_settings, valid_xml, load_settings, convert, get_app_path, colours, ignore

# TODO: Generate a conf file with the current setup, aka you have notepad on first monitor, terminal on second
# Run winporn.py --get-conf to get the current desktop state as an XML conf file, which can then be launched [@Haigutus]
# IDEA: https://stackoverflow.com/questions/14394513/win32gui-get-the-current-active-application-name

# TODO: Create a terminal prompt for saving conf or running it
# IDEA: If conf file in terminal prompt, then load it, else save with default name

# Globals
SAVE_CONFIG = 0
LOAD_CONFIG = not SAVE_CONFIG
open_processes = []
json = {
    "settings": {
        "app": []
    }
}

def load_config(hwnd, monitors):
    app_window_title = win32gui.GetWindowText(hwnd)
    app_window_exists = win32gui.IsWindowVisible(hwnd)

    for app in app_settings:
        if app_window_title == app_settings[app]["wintitle"] and app_window_exists and not app_settings[app]["configured"]:            
            print(f"[\u29D6] Setup: {app}")
            
            import_module(f"configurators.{app_settings[app]['configurator']}").setup(
                win32gui.FindWindow(None, app_window_title),
                app_settings[app], 
                monitors[app_settings[app]["monitor_id"]] if "monitor_id" in app_settings[app] else 0
            )
            
            print(f"[{colours.OKGREEN}\u2713{colours.ENDC}] Setup complete: {app}")
            app_settings[app]["configured"] = True
            
        open_processes.append(app_settings[app]["wintitle"]) if app_settings[app]["wintitle"] not in open_processes and app_settings[app]["configured"] else open_processes

def save_config(hwnd, s):
    app_window_title = win32gui.GetWindowText(hwnd)
    app_window_exists = win32gui.IsWindowVisible(hwnd)
    if app_window_exists and app_window_title:
        if get_app_path(hwnd) not in ignore and app_window_title not in ignore:
            window = win32gui.FindWindow(None, app_window_title)
            xmin, ymin, xmax, ymax = win32gui.GetWindowRect(hwnd)
            if window:                
                d = { 
                    "@name": str(app_window_title).split(' ')[-1],
                    "cmd": get_app_path(hwnd),
                    "wintitle": app_window_title,
                    # "monitor_id": None,
                    "fullscreen": int(win32gui.GetWindowPlacement(window)[1] == win32con.SW_SHOWMAXIMIZED),
                    "location": {
                        "xmin": xmin,
                        "ymin": ymin,
                        "xmax": xmax,
                        "ymax": ymax
                    },
                    "configurator": "notepad",
                    "configured": False
                }
                json["settings"]["app"].append(d)
                
if __name__ == "__main__":
    if SAVE_CONFIG:
        win32gui.EnumWindows(save_config, None)
        with open("settings.xml", "w") as f:
            f.write(convert(json))

    if LOAD_CONFIG:
        set_file = "settings.xml"
        if valid_xml(set_file):                
            app_settings = load_settings(set_file)
            if valid_settings(app_settings):
                for app in app_settings:
                    if not app_settings[app]["configured"]:
                        subprocess.Popen(app_settings[app]["cmd"])

                while len(open_processes) != len(app_settings.keys()):
                    time.sleep(1)
                    win32gui.EnumWindows(load_config, read_monitors())
            else:
                print("Settings XML validation: SUCCESS, settings parameters JSON validation: FAILED")
        else:
            print("Settings XML validation: FAILED")