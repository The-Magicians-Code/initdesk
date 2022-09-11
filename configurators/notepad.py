import win32gui
import win32api
import win32con

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
        # print("Window position before moving", x0, y0, x1, y1)
        print("Window position before moving", x0 - monitor.x, y0 - monitor.y, x1 - monitor.x, y1 - monitor.y)

        # if any(x > monitor.width for x in current_size[:2]) or any(y > monitor.height for y in current_size[2:]):
        x = [x0, x1]
        y = [y0, y1]
        for xq, yq in zip(x, y):
            print(xq, yq)

        print("Estimated position and size", x[0], y[0], x[1] - x[0], y[1] - y[0])
        # win32gui.MoveWindow(hwnd, monitor.x + x[0], monitor.y + y[0], x[1] - x[0], y[1] - y[0], True)

        print("Window size", x1 - x0, y1 - y0)
        # win32gui.MoveWindow(
        #     hwnd, 
        #     monitor.x + 10,# + x[0], 
        #     monitor.y + 200,# + y[0], 
        #     monitor.width + (monitor.width - x[1]), # monitor.width - (monitor.x - monitor.width),    # This param is window horiz size
        #     monitor.height + (monitor.height - y[1]), # monitor.height - (monitor.y - monitor.height),  # This param is window vert size
        #     True
        # )

        x0, y0, x1, y1 = win32gui.GetWindowRect(hwnd)
        print("Window position after moving", x0 - monitor.x, y0 - monitor.y, x1 - monitor.x, y1 - monitor.y)
        print("Unaltered position", win32gui.GetWindowRect(hwnd))
        print("Monitor location", monitor.x, monitor.y, monitor.width, monitor.height)