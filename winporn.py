import subprocess
import win32gui # pip install pywin32
import time
# from screeninfo import get_monitors # pip install screeninfo
from importlib import import_module
from params import read_monitors, colors
from settings import app_settings
from validate_settings import valid

# Application name when being run through terminal
for app in app_settings:
    subprocess.Popen(app_settings[app]["cmd"])
    app_settings[app].update({"configured": False})

open_processes = []
def callback(hwnd, monitors):
    app_window_title = win32gui.GetWindowText(hwnd)
    app_window_exists = win32gui.IsWindowVisible(hwnd)

    for app in app_settings:
        if app_window_title == app_settings[app]["wintitle"] and app_window_exists and not app_settings[app]["configured"]:            
            # hwnd = win32gui.FindWindow(None, app_window_title)
            print(f"[\u29D6] Setup: {app}")
            import_module(f"configurators.{app_settings[app]['configurator']}").setup(
                win32gui.FindWindow(None, app_window_title), 
                app_settings[app], 
                monitors[app_settings[app]["monitor_id"]] if app_settings[app]["monitor_id"] != None else monitors[0]
            )

            # if app == "Teams":
            #     current_size = win32gui.GetWindowRect(hwnd)
            #     while win32gui.GetWindowRect(hwnd) == current_size:
            #         win32gui.MoveWindow(hwnd, monitors[0].x, monitors[0].y, monitors[0].width, monitors[0].height, True)
            #         time.sleep(1)   # Necessary delay
            #     win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            #     print("Setup complete")
            #     app_settings[app]["configured"] = True
            
            print(f"[{colors.OKGREEN}\u2713{colors.ENDC}] Setup complete: {app}")
            app_settings[app]["configured"] = True
            open_processes.append(app_settings[app]["wintitle"]) if app_settings[app]["wintitle"] not in open_processes else open_processes

if valid():
    while len(open_processes) != len(app_settings.keys()):
        time.sleep(1)
        win32gui.EnumWindows(callback, read_monitors())
else:
    print("Invalid settings config")