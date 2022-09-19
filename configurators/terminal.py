import win32gui
import win32api
import win32con
from params import colours, prepare_location

def setup(hwnd, app_config, monitor):
    if app_config["fullscreen"] and monitor:
        win32gui.MoveWindow(hwnd, monitor.x, monitor.y, monitor.width, monitor.height, True)
        # Setup cursor position for scrolling
        # Remember current position
        current_pos = win32api.GetCursorPos()
        print(f"[{colours.WARNING}\u203C{colours.ENDC}] Please do not interact with the mouse, it is being used for screen configuration")
        for _ in range(2):  # Can't detect the right monitor on first try
            win32api.SetCursorPos((monitor.x + 5, monitor.y + 45))
        # Scroll to top
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, *win32api.GetCursorPos(), 1000, 0)
        
        # Reset the cursor position
        for _ in range(2):  # Can't detect the right monitor on first try
            win32api.SetCursorPos(current_pos)
        print(f"[{colours.OKCYAN}\u2713{colours.ENDC}] Restored previous mouse position")
    elif "location" in app_config:
        # Calculate the coords
        top_left, size = prepare_location(app_config["location"], monitor)
        for i in range(2):
            win32gui.MoveWindow(hwnd, *top_left, *size, True)
    if app_config["fullscreen"]:
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
    else:
        print("Nothing to configure")