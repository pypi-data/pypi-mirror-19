# -*- coding: utf-8 -*-
import copy

import diff
from lxml import etree


# Heuristic function for the diffing algorithm.
def heuristic(d1, d2):
    tags1 = [e.tag for e in d1.xpath("//*")]
    tags2 = [e.tag for e in d2.xpath("//*")]
    commontags = set(tags1).intersection(set(tags2))
    return len(tags1) + len(tags2) - 2 * len(commontags)


# Domain sets.
UNIT = set([None])
T = set(["b", "img"])

# Input documents.
doc1 = etree.fromstring("<root>hello</root>")
doc2 = etree.fromstring("<root>hi</root>")
doc2 = etree.fromstring("<root><img/><b>hello</b></root>")


# Transformation functions.
def addtag_domain(document):
    return T


def addtag(tag, position, document):
    doc = copy.deepcopy(document)
    selector = "(//*)[%d]" % position
    pos = doc.xpath(selector)

    if pos is not None:
        etree.SubElement(pos[0], tag)
        return doc

    raise Exception


def deltag_domain(document):
    return UNIT


def deltag(unit, position, document):
    doc = copy.deepcopy(document)
    selector = "(//*)[%d]" % position
    pos = doc.xpath(selector)

    if pos is not None:
        pos[0].clear()
        return doc

    raise Exception


def updatetext_domain(document):
    return set([e.text for e in doc2.xpath("//*")])


def updatetext(text, position, document):
    doc = copy.deepcopy(document)
    selector = "(//*)[%d]" % position
    pos = doc.xpath(selector)

    if pos is not None:
        pos[0].text = text
        return doc

    raise Exception


# Transformation functions set.
F = [
    (addtag_domain, addtag),
    (deltag_domain, deltag),
    (updatetext_domain, updatetext),
]

# The delta between the input documents is calculated.
delta = diff.delta(doc1, doc2, F, heuristic, debug=False)

# If a delta is retrieved, it is printed out.
if delta is not None:
    current = doc1
    for f, value, position in delta:
        result = f(value, position, current)
        row = "{0}({1},{2})".format(f.__name__, value, position)
        print(row)
        current = result
else:
    print("Goal document is unreachable from given source.")

