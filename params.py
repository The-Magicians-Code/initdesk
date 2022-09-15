from screeninfo import get_monitors # pip install screeninfo
from pathlib import Path
from lxml import etree
import win32process
import xmltodict
import wmi

def read_monitors():
    """Read monitor configuration from the system

    Returns:
        list: List of monitors, main first, then left, then right ones
    """
    list_monitors = get_monitors()
    main_monitor = [monitor for monitor in list_monitors if monitor.is_primary][0]
    left = [monitor for monitor in list_monitors if [monitor.x, monitor.y] < [main_monitor.x, main_monitor.y]]
    right = [monitor for monitor in list_monitors if [monitor.x, monitor.y] > [main_monitor.x, main_monitor.y]]

    return [main_monitor, *left, *right]

def valid_settings(app_settings):
    """Validates set parameters if XML validation is passed

    Args:
        app_settings (JSON): Settings data parsed from XML to JSON

    Returns:
        bool: True if settings are valid else returns an error
    """
    
    monitors = read_monitors()

    for app in app_settings:
        if not app_settings[app]["configured"]:
            try:
                monitor = monitors[app_settings[app]["monitor_id"]] if app_settings[app]["monitor_id"] != None else monitors[0]
            except IndexError:
                print(f"[{app}] -> {IndexError.__name__}: Invalid monitor index: Available are 0-{len(monitors) - 1}\n")
                print("Available monitors from left to right, starting with main:", *monitors, sep="\n - ")
            if app_settings[app]["fullscreen"]:
                print(f"Application: {app} will be set to fullscreen mode on the monitor, ignoring any set location variables")
            elif "location" in app_settings[app]:
                x0, y0, x1, y1 = app_settings[app]["location"]
                if any(x > monitor.width for x in [x0, x1]) or any(y > monitor.height for y in [y0, y1]):
                    raise ValueError(
                        f"{app}: x/y parameter(s) exceed monitor height/width\n" \
                        f"Allowed limits: x: 0-{monitor.width}, y: 0-{monitor.width}"
                    )
                if x0 > x1 or y0 > y1:
                    raise ValueError("x0 / y0 can't be bigger than x1 / y1, you pillock!")
            elif "location" not in app_settings[app]:
                print(f"Application: {app} will be enlarged and set to windowed mode on the monitor")
            if not Path(f'configurators/{app_settings[app]["configurator"]}.py').is_file():
                raise FileNotFoundError(f"{app} configurator: {app_settings[app]['configurator']} does not exist")
        else:
            print(f"Application {app} configured: {app_settings[app]['configured']}, ignoring setup")
    return True

def prepare_location(location, monitor):
    """Configure parameters for win32gui windows move function

    Args:
        location (list): List of specified coordinates
        monitor (monitor): Selected monitor object

    Returns:
        list, list: Top left corner and application window size
    """
    
    x0, y0, x1, y1 = location
    top_left = [
        monitor.x + x0, 
        monitor.y + y0
    ]
    size = [
        x1 - x0, 
        y1 - y0
    ]
    return top_left, size

# https://xmlschema.readthedocs.io/en/latest/usage.html#data-decoding-and-encoding
# https://www.freeformatter.com/xsd-generator.html#before-output

def valid_xml():
    """Validate XML settings file, using a predefined XSD schema

    Returns:
        bool: True if successful validation
    """
    
    xml_schema_doc = etree.parse("schema.xsd")
    xml_doc = etree.parse("settings.xml")
    xml_schema = etree.XMLSchema(xml_schema_doc)
    status = xml_schema.validate(xml_doc)
    if xml_schema.error_log:
        print(xml_schema.error_log)
    
    return status

def load_settings():
    """Load and parse settings from validated XML settings file to JSON

    Returns:
        dict: Settings in JSON format
    """
    
    with open("settings.xml", "r") as f:
        d = xmltodict.parse(f.read())
    
    settings = {}
    bools = {'true': True, 'false': False}
    for i in range(len(d['settings']['app'])):
        settings.update({d['settings']['app'][i]['@name']:{}})
        for key in d['settings']['app'][i]:
            if key == '@name':
                continue    # Skip every operation in this loop
            value = str(d['settings']['app'][i][key])
            if value.isdigit():
                setval = int(value)
            elif value.lower() in bools:
                setval = bools[value.lower()]
            elif key == 'location':
                setval = [int(d['settings']['app'][i][key][item]) for item in d['settings']['app'][i][key]]
            else:
                setval = d['settings']['app'][i][key]
            settings[d['settings']['app'][i]['@name']].update({key: setval})

    return settings

# c = wmi.WMI()

def get_app_path(hwnd):
    """Get applicatin path given hwnd."""
    try:
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        for p in wmi.WMI().query('SELECT ExecutablePath FROM Win32_Process WHERE ProcessId = %s' % str(pid)):
            exe = p.ExecutablePath
            break
    except:
        return None
    else:
        return exe

def get_app_name(hwnd):
    """Get applicatin filename given hwnd."""
    try:
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        for p in wmi.WMI().query('SELECT Name FROM Win32_Process WHERE ProcessId = %s' % str(pid)):
            exe = p.Name
            break
    except:
        return None
    else:
        return exe

ignore = [
    "BBar",
    "Settings",
    "CN=Microsoft Windows, O=Microsoft Corporation, L=Redmond, S=Washington, C=US",
    "Malwarebytes Tray Application",
    "Microsoft Text Input Application",
    "C:\Program Files\Rainmeter\Rainmeter.exe",
    "Program Manager"
]

class colours:
    """Colours for custom terminal messages
    """
    
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

from xmltodict import unparse

def convert(input_data):
    """
    Convert JSON to XML

    :param input_data: The incoming json document as a list
    :type input_data: list of str

    :return: XML list
    :rtype: list of str
    """
    return [unparse({"settings": i}, pretty=True) for i in input_data]