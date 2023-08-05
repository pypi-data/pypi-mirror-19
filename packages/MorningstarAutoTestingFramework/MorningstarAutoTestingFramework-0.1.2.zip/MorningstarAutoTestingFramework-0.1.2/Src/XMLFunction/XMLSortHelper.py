# -*- coding: utf-8 -*-
from operator import attrgetter
import lxml.etree as le


# region Custom Sort Expression


def sort_by_int_type(elem, attr_name):
    attr_obj = elem.get(attr_name)
    if attr_obj:
        try:
            return int(attr_obj)
        except ValueError:
            return 0
    return 0


def sort_by_id(elem):
    """Sort elements by ID if the 'id' attribute can be cast to an int."""
    id = elem.get('Id')
    if id:
        try:
            return int(id)
        except ValueError:
            return 0
    return 0


def sort_by_text(elem):
    """Sort XML elements by their text contents."""
    text = elem.text
    if text:
        return text
    else:
        return ''


# endregion


def sort_attributes(item, sorted_item, reverse_flag=False):
    """Sort XML attributes alphabetically by key.

    The original item is left unmodified and its attributes are copied to the provided `sorted_item`.
    """
    attribute_keys = sorted(item.keys(), reverse=reverse_flag)
    for key in attribute_keys:
        sorted_item.set(key, item.get(key))


def sort_elements(items, new_element):
    # Sort by Node attrib order from left to right
    items = sorted(items, key=attrgetter('tag'))

    # Custom Sort,
    # items = sorted(items, key=sort_by_text)

    # Once sorted, we sort each of the items
    for item in items:
        # Create a new item to represent the sorted version of the next item,and copy the tag name and contents
        new_item = le.Element(item.tag)
        if item.text and item.text.isspace() is False:
            new_item.text = item.text

        # Copy the attributes (sorted by key) to the new item
        sort_attributes(item, new_item, False)

        # Copy the children of item (sorted) to the new item
        sort_elements(list(item), new_item)

        # Append this sorted item to the sorted root
        new_element.append(new_item)


def sort_xml_file(origin_input_xml_file, sorted_output_xml_file):
    with open(origin_input_xml_file, 'r') as original:
        # Parse the XML file and get a pointer to the top
        input_xml_doc = le.parse(original)

        input_xml_root = input_xml_doc.getroot()

        # Create a new XML element that will be the top of the sorted copy of the XML file
        output_xml_root = le.Element(input_xml_root.tag, nsmap=input_xml_root.nsmap)

        # Create the sorted copy of the XML element, sort all attribute
        sort_attributes(input_xml_root, output_xml_root)

        # Custom Sort
        # items = sorted(items, key=sort_by_id)
        # items = sorted(items, key=sort_by_text)
        # items = sorted(items, key=lambda x: x[0])
        # from operator import itemgetter
        # items = sorted(items, key=attrgetter('grade', 'age')) # Please keep the attrib "grade" and "age" exist.

        sort_elements(list(input_xml_root), output_xml_root)

        # Write the sorted XML file to the temp file
        output_xml_tree = le.ElementTree(output_xml_root)
        with open(sorted_output_xml_file, 'wb') as output_file:
            output_xml_tree.write(output_file, pretty_print=True)


def sort_xml_content(origin_input_xml_content):
    input_xml_doc = le.fromstring(origin_input_xml_content)

    input_xml_root = input_xml_doc

    # Create a new XML element that will be the top of the sorted copy of the XML file
    output_xml_root = le.Element(input_xml_root.tag, nsmap=input_xml_root.nsmap)

    # Create the sorted copy of the XML element, sort all attribute
    sort_attributes(input_xml_root, output_xml_root)

    # Custom Sort
    # items = sorted(items, key=sort_by_id)
    # items = sorted(items, key=sort_by_text)
    # items = sorted(items, key=lambda x: x[0])
    # from operator import itemgetter
    # items = sorted(items, key=attrgetter('grade', 'age')) # Please keep the attrib "grade" and "age" exist.

    sort_elements(list(input_xml_root), output_xml_root)

    # Write the sorted XML file to the temp file
    output_xml_tree = le.ElementTree(output_xml_root)
    sorted_output_xml_content = le.tostring(output_xml_tree, pretty_print=True, encoding="utf-8")
    return sorted_output_xml_content
