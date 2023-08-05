# -*- coding: utf-8 -*-
import xml.dom.minidom
from xml.dom import Node


def main():
    path = 'D:\PythonCode\CodeLib\src\XML\Test.xml'
    dom = xml.dom.minidom.parse(path)
    root = dom.documentElement

    listInfos = []
    for child in root.childNodes:
        if child.nodeType == Node.ELEMENT_NODE:
            dictAttr = {}
            for key in child.attributes.keys():
                attr = child.attributes[key]
                dictAttr[attr.name] = attr.value
            listInfos.append({child.nodeName: dictAttr})

    # 输出结果更清晰直观一点
    for index, each in enumerate(listInfos):
        print '----', index + 1, '----', each


if __name__ == '__main__':
    main()
