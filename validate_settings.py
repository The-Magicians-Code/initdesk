from settings import app_settings
from params import read_monitors
from pathlib import Path

def valid():
    monitors = read_monitors()

    keys = ['cmd', 'wintitle', 'monitor_id', 'fullscreen', 'location', 'configurator', 'configured']
    for app in app_settings:
        if list(app_settings[app].keys()) == keys:
            try:
                monitor = monitors[app_settings[app]["monitor_id"]] if app_settings[app]["monitor_id"] != None else monitors[0]
            except IndexError:
                print(f"[{app}] -> {IndexError.__name__}: Invalid monitor index: Available are 0-{len(monitors) - 1}\n")
                print("Available monitors from left to right, starting with main:", *monitors, sep="\n - ")
                
            if app_settings[app]["location"] and len(app_settings[app]["location"]) != 4:
                raise ValueError(f"{app}: Location defined with wrong number of values, 4 int values [x0, y0, x1, y1] needed")
            if len(app_settings[app]["location"]) == 4:
                x0, y0, x1, y1 = app_settings[app]["location"]
                if any(x > monitor.width for x in [x0, x1]) or any(y > monitor.height for y in [y0, y1]):
                    raise ValueError(
                        f"{app}: x/y parameter(s) exceed monitor height/width\n" \
                        f"Allowed limits: x: 0-{monitor.width}, y: 0-{monitor.width}"
                    )
            if not app_settings[app]["location"]:
                print("Application will be fit to the monitor")
            if not Path(f'configurators/{app_settings[app]["configurator"]}.py').is_file():
                raise FileNotFoundError(f"{app} configurator: {app_settings[app]['configurator']} does not exist")
        else:
            raise ValueError(f"{app} configuration has missing or too many keys")
    return True