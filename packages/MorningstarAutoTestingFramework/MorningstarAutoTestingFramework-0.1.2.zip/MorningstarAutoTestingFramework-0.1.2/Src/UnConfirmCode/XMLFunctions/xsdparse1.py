# -*- coding: utf-8 -*-
from lxml import etree
import os


def __ingest_file_and_strip_mime(filename):
    data = ''
    f = open(filename, 'rb')
    for line in f.readlines():
        if line == '\r\n':
            continue
        if line == '\n':
            continue
        if line.find('Content-Type') >= 0:
            continue
        data = data + line
    f.close()
    return data


def substitute_opengis_schema_location(location, alternate_opengisschemas_location):
    if alternate_opengisschemas_location is not None and location.startswith('http://schemas.opengis.net/'):
        location = alternate_opengisschemas_location + '/' + location[len('http://schemas.opengis.net/'):]
    return location


def validate(xml_filename_or_content, xsd_filename=None,
             application_schema_ns='http://mapserver.gis.umn.edu/mapserver',
             alternate_opengisschemas_location='SCHEMAS_OPENGIS_NET'):
    if xml_filename_or_content.find('<?xml') == 0:
        doc = etree.XML(xml_filename_or_content)
    else:
        doc = etree.XML(__ingest_file_and_strip_mime(xml_filename_or_content))

    # Special case if this is a schema
    if doc.tag == '{http://www.w3.org/2001/XMLSchema}schema':
        for child in doc:
            if child.tag == '{http://www.w3.org/2001/XMLSchema}import':
                location = child.get('schemaLocation')
                location = substitute_opengis_schema_location(location, alternate_opengisschemas_location)
                child.set('schemaLocation', location)
        etree.XMLSchema(etree.XML(etree.tostring(doc)))
        return True

    schema_locations = doc.get("{http://www.w3.org/2001/XMLSchema-instance}schemaLocation")

    # Our stripped GetFeature document have an empty timeStamp, put a
    # fake value one instead
    if doc.get('timeStamp') == '':
        doc.set('timeStamp', '1970-01-01T00:00:00Z')

    locations = schema_locations.split()

    # get schema locations
    schema_def = etree.Element("schema", attrib={
        "elementFormDefault": "qualified",
        "version": "1.0.0",
    }, nsmap={
        None: "http://www.w3.org/2001/XMLSchema"
    }
                               )

    tempfiles = []

    # Special case for the main application schema
    for ns, location in zip(locations[::2], locations[1::2]):
        if ns == application_schema_ns:
            if xsd_filename is not None:
                location = xsd_filename
            else:
                location = xml_filename[0:-3] + 'xsd'

            # Remove mime-type header line if found to generate a valid .xsd
            sanitized_content = __ingest_file_and_strip_mime(location)
            location = '/tmp/tmpschema%d.xsd' % len(tempfiles)
            f = open(location, 'wb')
            f.write(sanitized_content)
            tempfiles.append(location)
            f.close()

            xsd = etree.XML(sanitized_content)
            for child in xsd:
                if child.tag == '{http://www.w3.org/2001/XMLSchema}import':
                    sub_ns = child.get('namespace')
                    sub_location = child.get('schemaLocation')
                    sub_location = substitute_opengis_schema_location(sub_location, alternate_opengisschemas_location)
                    etree.SubElement(schema_def, "import", attrib={
                        "namespace": sub_ns,
                        "schemaLocation": sub_location
                    }
                                     )

            etree.SubElement(schema_def, "import", attrib={
                "namespace": ns,
                "schemaLocation": location
            }
                             )

    # Add each schemaLocation as an import
    for ns, location in zip(locations[::2], locations[1::2]):
        if ns == application_schema_ns:
            continue
        location = substitute_opengis_schema_location(location, alternate_opengisschemas_location)
        etree.SubElement(schema_def, "import", attrib={
            "namespace": ns,
            "schemaLocation": location
        }
                         )

    # TODO: ugly workaround. But otherwise, the doc is not recognized as schema
    schema = etree.XMLSchema(etree.XML(etree.tostring(schema_def)))

    try:
        schema.assertValid(doc)
        ret = True
    except etree.Error as e:
        print(str(e))
        ret = False

    for filename in tempfiles:
        os.remove(filename)

    return ret


if __name__ == '__main__':
    validate(r"D:\git\EquityProductionTesting\EquityQATools\Data\Sample\CompanyInfo.xml",
             r"C:\Users\bzhou\Desktop\EquityXOISchema\CompanyInfo.xsd", "http://www.w3.org/2001/XMLSchema")
