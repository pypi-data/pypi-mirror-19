# -*- coding: utf-8 -*-

# http://stackoverflow.com/questions/2979824/in-document-schema-declarations-and-lxml
# https://mailman-mail5.webfaction.com/pipermail/lxml/2011-September/006153.html

from lxml import etree, objectify


def main():
    try:
        xsd = etree.parse(r'C:\Users\bzhou\Desktop\EquityXOISchema\CompanyInfo.xsd')
        children_node = xsd.getroot().getchildren()
        targetNamespace = xsd.getroot().get('targetNamespace')
        qualified = xsd.getroot().get('elementFormDefault')
        if len(children_node) != 0:
            for child in children_node:
                if child.tag == '{http://www.w3.org/2001/XMLSchema}include':
                    location = child.get('schemaLocation')
                    # child.set('targetNamespace', targetNamespace)
                    # child.set('elementFormDefault', qualified)

                    # child.attrib['namespace'] = namespace
                    # child.attrib['schemaLocation'] = location

                    child.attrib['schemaLocation'] = r"file:///C:/Users/bzhou/Desktop/EquityXOISchema/" + location
                    # print child.attrib['schemaLocation']

        xmlschema = etree.XMLSchema(xsd)
        xml_doc = etree.parse(r'D:\git\EquityProductionTesting\EquityQATools\Data\Sample\CompanyInfo.xml')
        xmlschema.assertValid(xml_doc)
        print "YEAH!, my xml file has validated"
    except Exception, e:
        print "Oh NO!, my xml file does not validate"
        print e.message


def format_xml(parent):
    """
    Recursive operation which returns a tree formated
    as dicts and lists.
    Decision to add a list is to find the 'List' word
    in the actual parent tag.
    """
    ret = {}
    if parent.items():
        ret.update(dict(parent.items()))
    if parent.text:
        ret['__content__'] = parent.text
    if 'List' in parent.tag:
        ret['__list__'] = []
        for element in parent:
            if element.tag is not etree.Comment:
                ret['__list__'].append(format_xml(element))
    else:
        for element in parent:
            if element.tag is not etree.Comment:
                ret[element.tag] = format_xml(element)
    return ret
