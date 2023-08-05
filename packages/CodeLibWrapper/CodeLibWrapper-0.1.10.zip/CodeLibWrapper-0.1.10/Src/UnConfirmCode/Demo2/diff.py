# -*- coding: utf-8 -*-
"""
Provides functions to get the delta of two XML documents.

Copyright (C) 2013 Andrea Aquino <andrex.aquino@gmail.com>
Contributors: Justin Poliey <justin.d.poliey@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from lxml import etree


def _transformations(document, F):
    """
    Return the set of pairs such that: The first element is a document
    obtained applying any function in the F set to the input document,
    any node of that document and any legal input for that function.
    The second element is the triple composed of the applied function,
    the node and the legal input.
    """
    res = []
    nodes = int(document.xpath("count(//*)"))
    for domain, f in F:  # for each function
        for i in domain(document):  # for each legal input for that function
            for p in range(1, nodes + 1):  # for each node in the document
                try:
                    doc = f(i, p, document)
                    label = (f, i, p)
                    res.append((doc, label))
                except InvalidInputError:
                    continue
    return res


class InvalidInputError(Exception):
    """
    Input for transformation function is not valid.
    """


class _Node():
    """
    Model a document node in the infinite multigraph of transformations.
    """

    def __init__(self, value, g=0, h=0):
        self.__parent = None
        self.__label = None
        self.__value = value
        self.__g = g
        self.__h = h

    def getParent(self):
        return self.__parent

    def getLabel(self):
        return self.__label

    def getValue(self):
        return self.__value

    def getG(self):
        return self.__g

    def getH(self):
        return self.__h

    def setParent(self, parent):
        self.__parent = parent

    def setLabel(self, label):
        self.__label = label

    def setValue(self, value):
        self.__value = value

    def setG(self, g):
        self.__g = g

    def setH(self, h):
        self.__h = h

    def getNeighbours(self, F):
        document = etree.fromstring(self.getValue())
        return _transformations(document, F)

    def __hash__(self):
        return hash(self.getValue())


def delta(start, goal, F, heuristic, debug=False):
    """
    Return the delta in terms of the functions in the set F,
    between start and goal documents guiding the search using
    the heuristic function.  The output is a list of triples
    [(f1, i1, p1), (f2, i2, p2), ..., (fn, in, pn)] s.t.
    fn(in,pn,...f2(i2,p2,f1(i1,p1,start))) = goal
    """
    # Start and goal documents are serialized.
    serialized_start = etree.tostring(start)
    serialized_goal = etree.tostring(goal)

    if debug:
        print("starting document: {0}.".format(serialized_start))
        print("goal document: {0}.".format(serialized_goal))

    # The first node to expand is the start node while
    # no other node has been visited yet.
    fringe = set()
    visited = set()
    fringe.add(_Node(serialized_start))

    # While there is at least a node to visit
    while fringe:
        # Get the node that minimizes the sum of the real distance to
        # the goal calcolated so far and the expected distance.
        current = min(fringe, key=lambda e: e.getG() + e.getH())

        if debug:
            print("current: {0}.".format(current.getValue()))
            print("g = {0}.".format(current.getG()))
            print("h = {0}.".format(current.getH()))
            print("#fringe = {0}.".format(len(fringe)))
            print("#visited = {0}.".format(len(visited)))

        # If such a node is the goal the search ends and the list
        # of diffing functions is returned.
        if current.getValue() == serialized_goal:
            if debug:
                print("expdiff complete.")

            path = []
            while current.getParent():
                path.append(current.getLabel())
                current = current.getParent()
            return path[::-1]

        # Otherwise remove the node from the fringe, mark it
        # visited and get its neighbours.
        fringe.remove(current)
        visited.add(current.getValue())
        neighbours = current.getNeighbours(F)

        if debug:
            print("#neighbours: {0}.".format(len(neighbours)))

        # For every neighbour document.
        for neighbour, label in neighbours:
            # Serialize it.
            serialized_neighbour = etree.tostring(neighbour)
            if serialized_neighbour in visited:
                # If it was already visited, skip it.
                if debug:
                    print("document already visited: {0}.".format(serialized_neighbour))
                continue
            else:
                # Otherwise check if it is already in the fringe.
                matches = [e for e in fringe if e.getValue() == serialized_neighbour]
                if matches:
                    # If it is and the path calculated so far is shorter than the
                    # previous one already calculated to this node, update it.
                    if debug:
                        print("document already in fringe.")

                    document = matches[0]
                    new_g = current.getG() + 1  # (1 = movement cost)
                    if document.getG() > new_g:
                        document.setG(new_g)
                        document.setParent(current)
                        document.setLabel(label)
                else:
                    # If it is not add this new node to the fringe.
                    if debug:
                        print("new document: {0}.".format(serialized_neighbour))

                    new = _Node(serialized_neighbour)
                    new.setG(current.getG() + 1)  # (1 = movement cost)
                    new.setH(heuristic(neighbour, goal))
                    new.setParent(current)
                    new.setLabel(label)
                    fringe.add(new)
    return None


def main():
    print "Do something."


if __name__ == '__main__':
    main()