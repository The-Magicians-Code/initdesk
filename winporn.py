import subprocess
import win32gui # pip install pywin32
# import win32con
# import win32api
import time
from screeninfo import get_monitors # pip install screeninfo
from importlib import import_module
from colours import colors

requested_processes = {
    "Terminal": {
        "cmd": "wt",
        "wintitle": "Ubuntu",
        "monitor_id": 0,
        "location": [],
        "configurator": "terminal"
    },
    "Notepad": {
        "cmd": "notepad",
        "wintitle": "Untitled - Notepad",
        "monitor_id": None,
        "location": [],
        "configurator": "notepad"
    }
}

# Application name when being run through terminal
for app in requested_processes:
    subprocess.Popen(requested_processes[app]["cmd"])
    requested_processes[app].update({"configured": False})

open_processes = []
def callback(hwnd, monitors):
    app_window_title = win32gui.GetWindowText(hwnd)
    app_window_exists = win32gui.IsWindowVisible(hwnd)
    main_monitor = [monitor for monitor in monitors if monitor.is_primary][0]

    for app in requested_processes:
        if app_window_title == requested_processes[app]["wintitle"] and app_window_exists and not requested_processes[app]["configured"]:            
            # hwnd = win32gui.FindWindow(None, app_window_title)
            print(f"[\u29D6] Setup: {app}")
            import_module(f"configurators.{requested_processes[app]['configurator']}").setup(
                win32gui.FindWindow(None, app_window_title), 
                requested_processes[app], 
                monitors[requested_processes[app]["monitor_id"]] if requested_processes[app]["monitor_id"] != None else main_monitor
            )

            # if app == "Teams":
            #     current_size = win32gui.GetWindowRect(hwnd)
            #     while win32gui.GetWindowRect(hwnd) == current_size:
            #         win32gui.MoveWindow(hwnd, monitors[0].x, monitors[0].y, monitors[0].width, monitors[0].height, True)
            #         time.sleep(1)   # Necessary delay
            #     win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            #     print("Setup complete")
            #     requested_processes[app]["configured"] = True
            
            print(f"[{colors.OKGREEN}\u2713{colors.ENDC}] Setup complete: {app}")
            requested_processes[app]["configured"] = True
            open_processes.append(requested_processes[app]["wintitle"]) if requested_processes[app]["wintitle"] not in open_processes else open_processes

while len(open_processes) != len(requested_processes.keys()):
    time.sleep(1)
    win32gui.EnumWindows(callback, [m for m in get_monitors()])