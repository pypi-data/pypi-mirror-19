# -*- coding: utf-8 -*-

def dictlist(node):
    res = {}
    res[node.tag] = {}
    xmltodict(node, res[node.tag])
    reply = {}
    reply[node.tag] = res[node.tag]
    return reply


def xmltodict(node, res):
    rep = {}
    if len(node):
        # n = 0
        for n in list(node):
            rep[node.tag] = {}
            value = xmltodict(n, rep[node.tag])
            if len(n):
                value = rep[node.tag]
                res.update({n.tag: value})
            else:
                res.update(rep[node.tag])
    else:
        value = {}
        value = {'value': node.text, 'attributes': node.attrib, 'tail': node.tail}
        res.update({node.tag: node.text})
    return


def main():
    print "Do something."


if __name__ == '__main__':
    main()
