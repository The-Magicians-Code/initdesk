import win32gui
import win32api
import win32con
from params import colors

def setup(hwnd, app_config, monitor):
    if app_config["location"]:
        x0, y0, x1, y1 = app_config["location"]
        # Calculate the coords according to the monitor
        top_left = [monitor.x + x0, monitor.y + y0]
        size = [x1 - x0, y1 - y0]
        for i in range(2):
            win32gui.MoveWindow(hwnd, *top_left, *size, True)
        print("App moved")
    elif app_config["fullscreen"]:
        win32gui.MoveWindow(hwnd, monitor.x, monitor.y, monitor.width, monitor.height, True)
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
        print("Fullscreen configured")
    else:
        win32gui.MoveWindow(hwnd, monitor.x, monitor.y, monitor.width, monitor.height, True)
        print("App moved and with default size set")