import win32gui
import win32api
import win32con

def setup(hwnd, app_config, monitor):
    if not app_config["location"]:
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
    else:
        print("Coords")