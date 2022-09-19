# Default imports
import win32gui
import win32api
import win32con
from params import colours, prepare_location

def setup(hwnd, app_config, monitor):
    if monitor and app_config["fullscreen"]:
        # Set to screen
        win32gui.MoveWindow(hwnd, monitor.x, monitor.y, monitor.width, monitor.height, True)
        print("Set to monitor")
    elif "location" in app_config:
        # Read the location parameters from the configuration file
        top_left, size = prepare_location(app_config["location"], monitor)
        for i in range(2):
            win32gui.MoveWindow(hwnd, *top_left, *size, True)
        print("App moved")
    if app_config["fullscreen"]:
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
        print("Fullscreen configured")