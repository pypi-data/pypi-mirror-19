# -*- coding: utf-8 -*-

import unittest
from element_tree import parent, ET, MyElementTree, xml_compare_with_visitor, diff
from mock import MagicMock
from default_visitor import StdVisitor


class TestMyTree(unittest.TestCase):
    def setUp(self):
        self.tree = ET.fromstring("<parent><child></child></parent>")
        self.myTree = MyElementTree(self.tree)
        self.child = self.myTree.find("child")

    def test_parent(self):
        self.assertEqual(parent(self.tree, self.child), self.tree)

    def test_mytree_parent(self):
        self.assertEqual(self.myTree.parent(self.child), self.myTree.getroot())

    def test_path(self):
        self.assertEqual(self.myTree.path(self.child), [self.myTree.getroot(), self.child])


class TestDiff(unittest.TestCase):
    def testDiff(self):
        lhs = {'attr': 'value', 'attr1': 'value2'}
        rhs = {'attr': 'value2', 'attr2': 'value3'}
        (add, remove, modify) = diff(lhs, rhs)
        self.assertEqual(add, ['attr2'])
        self.assertEqual(remove, ['attr1'])
        self.assertEqual(modify, ['attr'])


class TestXmlCompareWithVisitor(unittest.TestCase):
    def setUp(self):
        self.mockVisitor = MagicMock()

    def test_xml_attr_add(self):
        tree1 = MyElementTree(ET.fromstring("<parent></parent>"))
        tree2 = MyElementTree(ET.fromstring("<parent attr=\"value\"></parent>"))
        xml_compare_with_visitor(tree1, tree2, self.mockVisitor)
        self.mockVisitor.attribAdd.assert_called_with([tree1.getroot()], tree2.getroot(), ['attr'])

    def test_xml_attr_remove(self):
        tree1 = MyElementTree(ET.fromstring("<parent attr=\"value\"></parent>"))
        tree2 = MyElementTree(ET.fromstring("<parent></parent>"))
        xml_compare_with_visitor(tree1, tree2, self.mockVisitor)
        self.mockVisitor.attribRemove.assert_called_with([tree1.getroot()], tree1.getroot(), ['attr'])

    def test_xml_attr_modify(self):
        tree1 = MyElementTree(ET.fromstring("<parent attr=\"value\"></parent>"))
        tree2 = MyElementTree(ET.fromstring("<parent attr=\"value2\"></parent>"))
        xml_compare_with_visitor(tree1, tree2, self.mockVisitor)
        self.mockVisitor.attribModify.assert_called_with([tree1.getroot()], tree1.getroot(), tree2.getroot(), ['attr'])

    def test_xml_subchild_add(self):
        tree1 = MyElementTree(ET.fromstring("<parent></parent>"))
        tree2 = MyElementTree(ET.fromstring("<parent><child1></child1><child2></child2></parent>"))
        xml_compare_with_visitor(tree1, tree2, self.mockVisitor)
        self.mockVisitor.childElementAdd.assert_called_with([tree1.getroot()], tree2.getroot(),
                                                            tree2.getroot().getchildren())

    def test_xml_subchild_remove(self):
        tree2 = MyElementTree(ET.fromstring("<parent></parent>"))
        tree1 = MyElementTree(ET.fromstring("<parent><child1></child1><child2></child2></parent>"))
        xml_compare_with_visitor(tree1, tree2, self.mockVisitor)
        self.mockVisitor.childElementRemove.assert_called_with([tree1.getroot()], tree1.getroot(),
                                                               tree1.getroot().getchildren())

    def test_xml_subchild_move(self):
        tree2 = MyElementTree(ET.fromstring("<parent><child2></child2><child1></child1></parent>"))
        tree1 = MyElementTree(ET.fromstring("<parent><child1></child1><child2></child2></parent>"))
        xml_compare_with_visitor(tree1, tree2, self.mockVisitor)
        self.mockVisitor.childElementMove.assert_called_with([tree1.getroot()], tree1.getroot(), tree2.getroot(),
                                                             tree1.getroot().getchildren())


if __name__ == '__main__':
    unittest.main()
