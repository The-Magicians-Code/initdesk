import win32gui
import win32api
import win32con
from params import colors

def setup(hwnd, app_config, monitor):
    if app_config["location"]:
        x0, y0, x1, y1 = app_config["location"]
        # Calculate the coords according to the monitor
        top_left = [monitor.x + x0, monitor.y + y0]
        bottom_right = [monitor.x + x1, monitor.y + y1]
        win32gui.MoveWindow(hwnd, *top_left, *bottom_right, True)
    elif app_config["fullscreen"]:
        win32gui.MoveWindow(hwnd, monitor.x, monitor.y, monitor.width, monitor.height, True)
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
    else:
        x0, y0, x1, y1 = win32gui.GetWindowRect(hwnd)
        print("Window position before moving", x0, y0, x1, y1)
        # if any(x > monitor.width for x in current_size[:2]) or any(y > monitor.height for y in current_size[2:]):
        x = [value if value < monitor.width else monitor.width for value in [x0, x1]]
        y = [value if value < monitor.height else monitor.height for value in [y0, y1]]
        for xq, yq in zip(x, y):
            print(xq, yq)
        # win32gui.MoveWindow(hwnd, monitor.x + x[0], monitor.y + y[0], x[1] - x[0], y[1] - y[0], True)
        win32gui.MoveWindow(
            hwnd, 
            monitor.x + 10,# + x[0], 
            monitor.y + 200,# + y[0], 
            monitor.width - (monitor.x - monitor.width),    # This param is window horiz size
            monitor.height - (monitor.y - monitor.height),  # This param is window vert size
            True
        )

        x0, y0, x1, y1 = win32gui.GetWindowRect(hwnd)
        print("Window position after moving", x0 - monitor.x, y0 - monitor.y, x1 - monitor.x, y1 - monitor.y)
        print("Unaltered position", win32gui.GetWindowRect(hwnd))
        print("Monitor params", monitor.x, monitor.y, monitor.width, monitor.height)
    
    
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