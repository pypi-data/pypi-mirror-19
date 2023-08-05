# -*- coding: utf-8 -*-
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


def get_parent_map(root):
    return dict((c, p) for p in root.getiterator() for c in p)


def parent(root, element):
    parent_map = get_parent_map(root)
    return parent_map[element]


def compare_element(lhs, rhs):
    return lhs.tag < rhs.tag


def diff(old, new):
    add = []
    modify = []
    remove = []
    for key in old:
        if key in new:
            if old[key] != new[key]:
                modify.append(key)
        else:
            remove.append(key)
    for key in new:
        if key not in old:
            add.append(key)

    return (add, remove, modify);


def find_tag(tag, elements):
    for element in elements:
        if tag == element.tag:
            return True

    return False


def diffchildren(old, new):
    old_local = old[0:]
    new_local = new[0:]

    add = []
    remove = []
    move = []

    for child in old_local:
        if not find_tag(child.tag, new_local):
            remove.append(child)

    for child in remove:
        old_local.remove(child)

    for child in new_local:
        if not find_tag(child.tag, old_local):
            add.append(child)

    for child in add:
        new_local.remove(child)

    for index in range(len(old_local)):
        if old_local[index].tag != new_local[index].tag:
            move.append(old_local[index])

    old_local.sort(compare_element)
    new_local.sort(compare_element)

    return (add, remove, move, (old_local, new_local))


class MyElementTree(ET.ElementTree):
    def __init__(self, root):
        ET.ElementTree.__init__(self, root)
        self.parent_map = get_parent_map(self.getroot())
        self.parent_map[self.getroot()] = None

    def parent(self, element):
        return self.parent_map[element]

    def path(self, element):
        path = []
        current = element
        while ET.iselement(current):
            path.append(current)
            current = self.parent_map[current]
        path.reverse()
        return path

    def compare(self, other, visitor):
        self.compare_element(self.getroot(), other.getroot(), visitor)

    def compare_element(self, self_element, other_element, visitor):
        if self_element.tag != other_element.tag:
            return

        (attribAdd, attribRemove, attribModify) = diff(self_element.attrib, other_element.attrib)

        path = self.path(self_element)

        if len(attribAdd) != 0:
            visitor.attribAdd(path, other_element, attribAdd)

        if len(attribRemove) != 0:
            visitor.attribRemove(path, self_element, attribRemove)

        if len(attribModify) != 0:
            visitor.attribModify(path, self_element, other_element, attribModify)

        (childElementAdd, childElementRemove, childElementMove, (sameOldChildren, sameNewChildren)) = diffchildren(
            self_element.getchildren(), other_element.getchildren())

        if len(childElementAdd) != 0:
            visitor.childElementAdd(path, other_element, childElementAdd)

        if len(childElementRemove) != 0:
            visitor.childElementRemove(path, self_element, childElementRemove)

        if len(childElementMove) != 0:
            visitor.childElementMove(path, self_element, other_element, childElementMove)

        for index in range(len(sameOldChildren)):
            self.compare_element(sameOldChildren[index], sameNewChildren[index], visitor)


def xml_compare_with_visitor(lhs, rhs, visitor):
    lhs.compare(rhs, visitor)
