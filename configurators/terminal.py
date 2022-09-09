import win32gui
import win32api
import win32con
from colours import colors

def setup(hwnd, app_config, monitor):
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