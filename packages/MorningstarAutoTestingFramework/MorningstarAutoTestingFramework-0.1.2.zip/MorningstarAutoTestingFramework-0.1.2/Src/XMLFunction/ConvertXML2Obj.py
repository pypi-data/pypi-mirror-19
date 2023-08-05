# -*- coding: utf-8 -*-

"""
 untangle

 Converts xml to python objects.

 The only method you need to call is parse()

 Partially inspired by xml2obj
 (http://code.activestate.com/recipes/149368-xml2obj/)

 Author: Christian Stefanescu (http://0chris.com)
 License: MIT License - http://www.opensource.org/licenses/mit-license.php
"""

import os
from xml.sax import make_parser, handler
import lxml.etree
from collections import Counter

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

__version__ = '1.1.0'


class Element:
    """
    Representation of an XML element.
    """

    def __init__ (self, name, attributes):
        self._name = name
        self._attributes = attributes
        self.children = []
        self.is_root = False
        self.cdata = ''

    def add_child (self, element):
        self.children.append (element)

    def add_cdata (self, cdata):
        self.cdata = self.cdata + cdata

    def get_attribute (self, key):
        return self._attributes.get (key)

    def get_elements (self, name=None):
        if name:
            return [e for e in self.children if e._name == name]
        else:
            return self.children

    def __getitem__ (self, key):
        return self.get_attribute (key)

    def __getattr__ (self, key):
        matching_children = [x for x in self.children if x._name == key]
        if matching_children:
            if len (matching_children) == 1:
                self.__dict__[key] = matching_children[0]
                return matching_children[0]
            else:
                self.__dict__[key] = matching_children
                return matching_children
        else:
            raise IndexError ('Unknown key <%s>' % key)

    def __iter__ (self):
        yield self

    def __str__ (self):
        return (
            "Element <%s> with attributes %s and children %s" %
            (self._name, self._attributes, self.children)
        )

    def __repr__ (self):
        return (
            "Element(name = %s, attributes = %s, cdata = %s)" %
            (self._name, self._attributes, self.cdata)
        )

    def __nonzero__ (self):
        return self.is_root or self._name is not None

    def __eq__ (self, val):
        return self.cdata == val

    def __dir__ (self):
        children_names = [x._name for x in self.children]
        return children_names


class Handler (handler.ContentHandler):
    """
    SAX handler which creates the Python object structure out of ``Element``s
    """

    def __init__ (self):
        self.root = Element (None, None)
        self.root.is_root = True
        self.elements = []

    def startElement (self, name, attributes):
        name = name.replace ('-', '_')
        name = name.replace ('.', '_')
        name = name.replace (':', '_')
        attrs = dict ()
        for k, v in attributes.items ():
            attrs[k] = v
        element = Element (name, attrs)
        if len (self.elements) > 0:
            self.elements[-1].add_child (element)
        else:
            self.root.add_child (element)
        self.elements.append (element)

    def endElement (self, name):
        self.elements.pop ()

    def characters (self, cdata):
        self.elements[-1].add_cdata (cdata)


def parse_xml_to_object (filename):
    """
    Interprets the given string as a filename, URL or XML data string,
    parses it and returns a Python object which represents the given
    document.

    Raises ``ValueError`` if the argument is None / empty string.

    Raises ``xml.sax.SAXParseException`` if something goes wrong
    during parsing.s
    """
    if filename is None or filename.strip () == '':
        raise ValueError ('parse() takes a filename, URL or XML string')
    parser = make_parser ()
    sax_handler = Handler ()
    parser.setContentHandler (sax_handler)
    if os.path.exists (filename) or is_url (filename):
        parser.parse (filename)
    else:
        parser.parse (StringIO (filename))

    return sax_handler.root


def sort_list_by_name (list_, reverse=False):
    """
    Sort by element by element Name
    :param list_:
    :param reverse:
    :return:
    """
    return sorted (list_, key=lambda x: x._name, reverse=reverse)


def sort_list_by_cdata (list_, reverse=False):
    """
    Sort by element by element value(CDATA)
    :param list_:
    :param reverse:
    :return:
    """
    return sorted (list_, key=lambda x: x.cdata, reverse=reverse)


def sort_list_by_attr (list_, attr_name, reverse=False):
    """
    Sort by element attribute name
    :param list_:
    :param attr_name:
    :param reverse:
    :return:
    """
    return sorted (list_, key=lambda x: x[attr_name], reverse=reverse)


def is_url (string):
    return string.startswith ('http://') or string.startswith ('https://')


# def toString(self, level=0):
#     retval = " " * level
#     retval += "&lt;%s" % self._name
#     for attribute in self._attributes:
#         retval += " %s=\"%s\"" % (attribute, self._attributes[attribute])
#     c = ""
#     for child in self.children:
#         c += child.toString(level+1)
#     if c == "":
#         retval += "/>\n"
#     else:
#         retval += ">\n" + c + ("&lt;/%s>\n" % self._name)
#     return retval



def main ():
    # xml_file = r"D:\AutoTestingCases\RobotFrameworkTesting\RobotFrameworkTutorial\SampleData\2014-11-30.xml"
    # doc = parse_xml_to_object (xml_file)
    # print doc.SurveyData.AustralianSurvey.AssetAllocation.BreakdownValue[0].cdata
    # print len (doc.SurveyData.AustralianSurvey.AssetAllocation.BreakdownValue)
    # print sort_list_by_name (doc.SurveyData.AustralianSurvey.AssetAllocation.BreakdownValue)

    xml_file = r"C:\Users\bzhou\Desktop\new4.xml"
    doc = parse_xml_to_object (xml_file)
    # print doc.StockExchangeSecuritys.MessageInfo
    list = doc.StockExchangeSecuritys.children
    print list

if __name__ == '__main__':
    main ()
