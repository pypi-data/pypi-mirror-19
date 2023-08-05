# -*- coding: utf-8 -*-
from xml.dom.minidom import Document


class Dict2xml(object):
    doc = Document()

    def __init__(self, structure):
        if len(structure) == 1:
            root_name = str(structure.keys()[0])
            self.root = self.doc.createElement(root_name)

            self.doc.appendChild(self.root)
            self.build(self.root, structure[root_name])

    def build(self, father, structure):
        if type(structure) == dict:
            for k in structure:
                tag = self.doc.createElement(k)
                father.appendChild(tag)
                self.build(tag, structure[k])

        elif type(structure) == list:
            grand_father = father.parentNode
            tag_name = father.tagName
            grand_father.removeChild(father)
            for l in structure:
                tag = self.doc.createElement(tag_name)
                self.build(tag, l)
                grand_father.appendChild(tag)

        else:
            data = str(structure)
            tag = self.doc.createTextNode(data)
            father.appendChild(tag)

    def display(self):
        print self.doc.toprettyxml(indent="  ")


def tuple2dict(t):
    return {y: x for x, y in t}


def tuple2dict_1(t):
    return dict(t)


def dict2obj(d):
    if isinstance(d, list):
        d = [dict2obj(x) for x in d]
    if not isinstance(d, dict):
        return d

    class C(object):
        pass

    o = C()
    for k in d:
        o.__dict__[k] = dict2obj(d[k])
    return o


def __dict2obj_test():
    d = {'a': 1, 'b': {'c': 2}, 'd': ["hi", {'foo': "bar"}]}
    x = dict2obj(d)
    print x.a
    print x.b.c
    print x.d[1].foo


def main():
    t = ((1, 'a'), (2, 'b'))
    dic = tuple2dict(t)
    obj = dict2obj(dic)
    print obj.a


def main2():
    example = {'sibbling': {'couple': {'mother': 'mom', 'father': 'dad', 'children': [{'child': 'foo'},
                                                                                      {'child': 'bar'}]}}}
    xml = Dict2xml(example)
    xml.display()


if __name__ == '__main__':
    main()
