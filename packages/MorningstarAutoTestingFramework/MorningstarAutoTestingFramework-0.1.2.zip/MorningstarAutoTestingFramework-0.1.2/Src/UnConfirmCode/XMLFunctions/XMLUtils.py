# -*- coding: utf-8 -*-
import os
import sys
import lxml.etree as etree


class XMLUtils:
    SHOW_LOG = True
    XML_PATH = None

    def __init__(self):
        pass

    # region    basic operation
    @staticmethod
    def get_xml_root(path):
        """
        parse the XML file,and get the tree of the XML file
        finally,return the root element of the tree.
        if the XML file dose not exist,then print the information
        :param path:
        :return:
        """
        if os.path.exists(path):
            if XMLUtils.SHOW_LOG:
                print('start to parse the file : [{}]'.format(path))
            try:
                tree = etree.parse(path)  # 打开xml文档
                return tree.getroot()  # 获得root节点
            except Exception, e:
                print "Error:cannot parse file:" + path + ". Details information is:" + e.message
                sys.exit(1)
        else:
            print('the path [{}] dose not exist!'.format(path))

    @staticmethod
    def get_element_tag(element):
        """
        return the element tag if the element is not None.
        :param element:
        :return:
        """
        if element is not None:
            if XMLUtils.SHOW_LOG:
                print('begin to handle the element : [{}]'.format(element))
            return element.tag
        else:
            print('the element is None!')

    @staticmethod
    def get_element_attrib(element):
        """
        return the element attrib if the element is not None.
        :param element:
        :return:
        """
        if element is not None:
            if XMLUtils.SHOW_LOG:
                print('begin to handle the element : [{}]'.format(element))
            return element.attrib
        else:
            print('the element is None!')

    @staticmethod
    def get_element_text(element):
        """
        return the text of the element.
        :param element:
        :return:
        """
        if element is not None:
            return element.text
        else:
            print('the element is None!')

    @staticmethod
    def get_element_children(element):
        """
        return the element children if the element is not None.
        :param element:
        :return:
        """
        if element is not None:
            if XMLUtils.SHOW_LOG:
                print('begin to handle the element : [{}]'.format(element))
            return [c for c in element]
        else:
            print('the element is None!')

    @staticmethod
    def get_elements_tag(elements):
        """
        return the list of tags of element's tag
        :param elements:
        :return:
        """
        if elements is not None:
            tags = []
            for e in elements:
                tags.append(e.tag)
            return tags
        else:
            print('the elements is None!')

    @staticmethod
    def get_elements_attrib(elements):
        """
        return the list of attribs of element's attrib
        :param elements:
        :return:
        """
        if elements is not None:
            attribs = []
            for a in elements:
                attribs.append(a.attrib)
            return attribs
        else:
            print('the elements is None!')

    @staticmethod
    def get_elements_text(elements):
        """
        return the dict of element
        """
        if elements is not None:
            text = []
            for t in elements:
                text.append(t.text)
            return dict(zip(XMLUtils.get_elements_tag(elements), text))
        else:
            print('the elements is None!')


            # def init():
            #     global SHOW_LOG
            #     SHOW_LOG = True
            #     global XML_PATH
            #     XML_PATH = 'c:\\test\\hongten.xml'
            #
            #
            # def main():
            #     init()
            #     # root
            #     root = get_root(XML_PATH)
            #     root_tag = get_element_tag(root)
            #     print(root_tag)
            #     root_attrib = get_element_attrib(root)
            #     print(root_attrib)
            #     # children
            #     children = get_element_children(root)
            #     print(children)
            #     children_tags = get_elements_tag(children)
            #     print(children_tags)
            #     children_attribs = get_elements_attrib(children)
            #     print(children_attribs)
            #
            #     print('#' * 50)
            #     # 获取二级元素的每一个子节点的名称和值
            #     for c in children:
            #         c_children = get_element_children(c)
            #         dict_text = get_elements_text(c_children)
            #         print(dict_text)
            #
            #
            # if __name__ == '__main__':
            #     main()

    # endregion

    @staticmethod
    def pretty_print_xml(xml_file_path):
        x = etree.parse(xml_file_path)
        print etree.tostring(x, pretty_print=True)

    def indent(self, elem, level=0):
        i = "\n" + level * "  "
        j = "\n" + (level - 1) * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for subelem in elem:
                self.indent(subelem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = j
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = j
        return elem


def main():
    print "Do something."


if __name__ == '__main__':
    main()
