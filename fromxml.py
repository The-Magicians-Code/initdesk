from lxml import etree

# https://xmlschema.readthedocs.io/en/latest/usage.html#data-decoding-and-encoding
# https://www.freeformatter.com/xsd-generator.html#before-output

xml_schema_doc = etree.parse("schema.xml")
xml_doc = etree.parse("settings.xml")
xml_schema = etree.XMLSchema(xml_schema_doc)
status = xml_schema.validate(xml_doc)
print(xml_schema.error_log, status)