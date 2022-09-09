from screeninfo import get_monitors

def read_monitors():
    list_monitors = get_monitors()
    main_monitor = [monitor for monitor in list_monitors if monitor.is_primary][0]
    left = [monitor for monitor in list_monitors if [monitor.x, monitor.y] < [main_monitor.x, main_monitor.y]]
    right = [monitor for monitor in list_monitors if [monitor.x, monitor.y] > [main_monitor.x, main_monitor.y]]

    return [main_monitor, *left, *right]

# Colors
class colors:
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'