import xml.etree.ElementTree as ET

root = ET.parse("settings.xml")
    
for item in root.findall("app"):
    print(item.get("name"))
    for t in item:
        print(t.tag, t.text)
    print()
    
# tags = {elem.tag for elem in root.iter()}
# print(tags)