import logging
from collections import OrderedDict

logging.getLogger(__name__)


class Graph(object):
    def __init__(self, name=""):
        """
        :param name: str, the name of the graph to set
        """
        self._name = name
        self._nodes = OrderedDict()

    def __repr__(self):
        return "{}{}".format(self.__class__.__name__, self.__dict__)

    def __len__(self):
        """Returns the length of the nodes in the graph
        :return:
        """
        return len(self._nodes)

    def addNode(self, node, **kwargs):
        """Adds a Node instance to the graph this will also add the node to the graph class instance as a attribute
        which can be accessed by graph.node
        :param node: Node instance, the node to add
        :kwargs: plugName=plugValue, the kwargs sets the input plugs value.
        :return Node instance
        """
        if self.hasNode(node):
            return
        node.name = self.generateUniqueName(node)
        self._nodes[node.name] = node
        for plugName, plugValue in kwargs.iteritems():
            plug = node.getPlug(plugName)
            if plug.isInput():
                plug.value = plugValue

        return node

    @property
    def nodes(self):
        """Returns all the nodes in the graph
        :return:
        """
        return self._nodes

    def hasNode(self, node):
        """Checks the graph for the given node _name
        :param node: node instance
        :return: bool
        """
        return node in self._nodes.values()

    def deleteNode(self, node):
        """Removes a node from the graph
        :param node:
        """
        del self._nodes[node.name]

    def getNode(self, nodeName):
        """Returns a node based on the name or empty list
        :param nodeName:
        :return:
        """
        return self._nodes.get(nodeName)

    def generateUniqueName(self, node):
        """Create a unique name for the node in the graph, on node creation a digit is appended , eg nodeName00, nodeName01
        :param node: node Instance
        :return: str
        """
        increObj = IncrementObject(0, 2)
        num = increObj.add()
        name = node.name + num
        while name in self._nodes:
            name = node.name + increObj.add()

        return name

    def clear(self):
        """Clears all the nodes from the graph
        :return: None
        """
        self._nodes.clear()

    def allLeaves(self):
        """Returns all the leaf nodes in the graph, a Leaf node is any node that has on connections
        :return: list(Node)
        """
        leafNodes = []

        for node in self._nodes.values():

            if not any(plug.connections for plug in node.inputs()):
                leafNodes.append(node)

        return leafNodes


class IncrementObject(object):
    """A class to help with incrementing a number with a padding
    """
    def __init__(self, startNumber, padding):
        """initilizes the seq number with start number and a padding value, use self.add() to add one number
        :param startNumber: int, the number for the sequence to start at
        :param padding: int, the number of numbers(zeros) to add in front of the seq number
        """
        self.seq = startNumber
        self.padding = padding
        self.currentValue = ""

    def add(self):
        """Increments the seq by and adds a padding value
        :return: str
        """
        value = "%0{}d".format(self.padding)
        value = value % self.seq
        self.seq += 1
        self.currentValue = value
        return value
