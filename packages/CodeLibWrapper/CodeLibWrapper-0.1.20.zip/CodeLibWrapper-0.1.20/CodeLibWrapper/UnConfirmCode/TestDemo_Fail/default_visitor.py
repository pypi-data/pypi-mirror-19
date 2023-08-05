# -*- coding: utf-8 -*-
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


def element_to_string(element):
    return ET.tostring(element).replace("\r", "").replace("\n", "").replace("\t", "")


class StdVisitor:
    def out(self, path, op, content):
        print("\t\t\t".join(["".join([e.tag for e in path]), op, content]))

    def attribAdd(self, path, other_element, attribAdd):
        self.out(path, "modify", element_to_string(other_element) + " attribute " + str(attribAdd) + " are added")

    def attribRemove(self, path, element, attribs):
        self.out(path, "modify", element_to_string(element) + " attribute " + str(attribs) + " are removed")

    def attribModify(self, path, self_element, other_element, attribs):
        self.out(path, "modify",
                 "from " + element_to_string(self_element) + " to " + ET.tostring(other_element) + " attribs " + str(
                     attribs) + " are modified")

    def childElementAdd(self, path, element, children):
        for child in children:
            newpath = path[0:]
            newpath.append(child)
            self.out(newpath, "add", "node " + element_to_string(child))

    def childElementRemove(self, path, self_element, children):
        for child in children:
            newpath = path[0:]
            newpath.append(child)
            self.out(newpath, "remove", "node " + element_to_string(child))


if __name__ == '__main__':
    visitor = StdVisitor()
    tree = ET.fromstring("<parent.><child. attr='value'></child.></parent.>")
    element = tree.getchildren()[0]
    path = [tree, element]
    attribs = ['attr']
    visitor.attribAdd(path, element, attribs)
    visitor.attribRemove(path, element, attribs)
    tree1 = ET.fromstring("<parent.><child. attr='value1'></child.></parent.>")
    element1 = tree1.getchildren()[0]
    visitor.attribModify(path, element, element1, attribs)
    path.remove(element)
    childrens = tree.getchildren()
    visitor.childElementAdd(path, tree, childrens)
    visitor.childElementRemove(path, tree, childrens)
