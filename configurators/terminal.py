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
        # Setup cursor position for scrolling
        # Remember current position
        current_pos = win32api.GetCursorPos()
        print(f"[{colors.WARNING}\u203C{colors.ENDC}] Please do not interact with the mouse, it is being used for screen configuration")
        for _ in range(2):  # Can't detect the right monitor on first try
            win32api.SetCursorPos((monitor.x + 5, monitor.y + 45))
        # Scroll to top
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, *win32api.GetCursorPos(), 1000, 0)
        
        # Reset the cursor position
        for _ in range(2):  # Can't detect the right monitor on first try
            win32api.SetCursorPos(current_pos)
        print(f"[{colors.OKCYAN}\u2713{colors.ENDC}] Restored previous mouse position")
    else:
        win32gui.MoveWindow(hwnd, monitor.x, monitor.y, monitor.width, monitor.height, True)
        print("App moved and with default size set")