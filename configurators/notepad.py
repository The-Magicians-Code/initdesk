import win32gui
import win32api
import win32con
from params import colours, prepare_location

def setup(hwnd, app_config, monitor):
    if monitor:
        if app_config["fullscreen"]:
            win32gui.MoveWindow(hwnd, monitor.x, monitor.y, monitor.width, monitor.height, True)
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            print("Fullscreen configured")
        elif "location" in app_config:
            # Calculate the coords according to the monitor
            top_left, size = prepare_location(app_config["location"], monitor)
            for i in range(2):
                win32gui.MoveWindow(hwnd, *top_left, *size, True)
            print("App moved")
        else:
            win32gui.MoveWindow(hwnd, monitor.x, monitor.y, monitor.width, monitor.height, True)
            print("App moved and with default size set")
    else:    
        if app_config["fullscreen"]:
            top_left, size = prepare_location(app_config["location"], monitor)
            for i in range(2):
                win32gui.MoveWindow(hwnd, *top_left, *size, True)
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            print("Fullscreen configured")
        elif "location" in app_config:
            # Calculate the coords according to the monitor
            top_left, size = prepare_location(app_config["location"], monitor)
            for i in range(2):
                win32gui.MoveWindow(hwnd, *top_left, *size, True)
            print("App moved")