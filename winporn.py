import subprocess
import win32gui # pip install pywin32
import time
from importlib import import_module
from params import read_monitors, valid_settings, valid_xml, load_settings, colours

# TODO: Generate a conf file with the current setup, aka you have notepad on first monitor, terminal on second
# Run winporn.py --get-conf to get the current desktop state as an XML conf file, which can then be launched [@Haigutus]
# IDEA: https://stackoverflow.com/questions/14394513/win32gui-get-the-current-active-application-name

open_processes = []
def callback(hwnd, monitors):
    app_window_title = win32gui.GetWindowText(hwnd)
    app_window_exists = win32gui.IsWindowVisible(hwnd)

    for app in app_settings:
        if app_window_title == app_settings[app]["wintitle"] and app_window_exists and not app_settings[app]["configured"]:            
            print(f"[\u29D6] Setup: {app}")
            
            import_module(f"configurators.{app_settings[app]['configurator']}").setup(
                win32gui.FindWindow(None, app_window_title), 
                app_settings[app], 
                monitors[app_settings[app]["monitor_id"]] if app_settings[app]["monitor_id"] != None else monitors[0]
            )
            
            print(f"[{colours.OKGREEN}\u2713{colours.ENDC}] Setup complete: {app}")
            app_settings[app]["configured"] = True
            
        open_processes.append(app_settings[app]["wintitle"]) if app_settings[app]["wintitle"] not in open_processes and app_settings[app]["configured"] else open_processes

if valid_xml():
    app_settings = load_settings()
    if valid_settings(app_settings):
        for app in app_settings:
            if not app_settings[app]["configured"]:
                subprocess.Popen(app_settings[app]["cmd"])

        while len(open_processes) != len(app_settings.keys()):
            time.sleep(1)
            win32gui.EnumWindows(callback, read_monitors())
    else:
        print("Settings XML validation: SUCCESS, settings parameters JSON validation: FAILED")
else:
    print("Settings XML validation: FAILED")