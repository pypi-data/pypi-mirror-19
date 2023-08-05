# -*- coding: utf-8 -*-

# region    Import
import lxml.etree as etree
try:
    import xml.etree.cElementTree as et
except ImportError:
    import xml.etree.ElementTree as et
# endregion


def parse_xml_from_string(xml_content_string):
    """
    从String变量中装载XML 对象
    :param xml_content_string: XML内容
    :return: 返回XML Element
    """
    root = et.fromstring(xml_content_string)
    return root


# region    Output the XPath from XML


def __remove_ns(tag):
    if tag.find('}') == -1:
        return tag
    else:
        return tag.split('}', 1)[1]


def __linearize(el, path):
    xpathlist = []

    # Print text value if not empty
    if el.text is None:
        text = ""
    else:
        text = el.text.strip()

    if text == "":
        # print path
        xpathlist.append(path)
    else:
        # Several lines ?
        lines = text.splitlines()
        if len(lines) > 1:
            line_nb = 1
            for line in lines:
                # print path + "[line %d]=%s " % (line_nb, line)
                xpathlist.append(path + "[line %d]=%s " % (line_nb, line))
                line_nb += 1
        else:
            # print path + "=" + text
            xpathlist.append(path + "=" + text)

    # Print attributes
    for name, val in el.items():
        # print path + "/@" + __remove_ns(name) + "=" + val
        xpathlist.append(path + "/@" + __remove_ns(name) + "=" + val)

    # Counter on the sibbling element names
    counters = {}

    # Loop on child elements
    for childEl in el:
        # Remove namespace
        tag = __remove_ns(childEl.tag)

        # Tag name already encountered ?
        if tag in counters:
            counters[tag] += 1
            # Number it
            numbered_tag = tag + "[" + str(counters[tag]) + "]"
        else:
            counters[tag] = 1
            numbered_tag = tag

        # Print child node recursively
        xpathlist.extend(__linearize(childEl, path + '/' + numbered_tag))
    return xpathlist


def __process(stream, prefix):
    # Parse the XMLFunction
    tree = et.parse(stream)

    # Get root element
    root = tree.getroot()

    # Linearize
    return __linearize(root, prefix + "//" + __remove_ns(root.tag))


def parse_xpath_from_xml(file_path, output_to_console=True):
    """
    输出给定XML中的节点对应的XPath
    :param file_path: XML文件的Path
    :param output_to_console: 是否输出xpath结果到
    :return: 输出每个节点的xpath值
    """
    l_file = open(file_path)
    return_list = __process(l_file, "")

    if output_to_console:
        for xpath in return_list:
            print xpath

    return return_list


# endregion


@staticmethod
def pretty_print_xml(xml_file_path):
    x = etree.parse(xml_file_path)
    print etree.tostring(x, pretty_print=True)


def validate_xml(schema_file, xml_file):
    xsd_doc = etree.parse(schema_file)
    xsd = etree.XMLSchema(xsd_doc)
    xml = etree.parse(xml_file)
    return xsd.validate(xml)

if __name__ == '__main__':
    print ""
