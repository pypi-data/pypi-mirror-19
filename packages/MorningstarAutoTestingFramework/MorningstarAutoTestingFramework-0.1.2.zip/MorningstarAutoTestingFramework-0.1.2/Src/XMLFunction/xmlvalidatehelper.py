# -*- coding: utf-8 -*-
# https://github.com/joelmir/validate-xml-from-multiple-xsd-schema
from lxml import etree
from lxml.etree import DocumentInvalid


def Validate_XSD (xml_filename, xsd_filename ):
    xml_file = open (xml_filename)
    xsd_file = open (xsd_filename)

    # Get Objects
    xml_doc = etree.XML (xml_file.read ())
    xsd_doc = etree.XML (xsd_file.read ())

    # Create a schema object
    xmlschema = etree.XMLSchema (xsd_doc)
    try:
        xmlschema.assertValid (xml_doc)
        return True, ""
    except DocumentInvalid as e:
        return False, e.message
    finally:
        xml_file.close ()
        xsd_file.close ()


def main ():
    xsd_path = r"C:\Python27\Lib\site-packages\CodeLibWrapper\RobotFrameworkSample\SampleData\StockExchangeSecurity.xsd"
    xml_path = r"C:\Python27\Lib\site-packages\CodeLibWrapper\RobotFrameworkSample\SampleData\new4.xml"

    result, error_message = Validate_XSD (xml_path, xsd_path)
    print result, error_message


if __name__ == '__main__':
    main ()
