import logging

logging.getLogger(__name__)


class Graph(object):
    def __init__(self, name=""):
        self._name = name
        self._nodes = set()

    def __repr__(self):
        return "{}{}".format(self.__class__.__name__, self.__dict__)

    def addNode(self, node):
        """Adds a Node instance to the graph this will also add the node to the graph class instance as a attribute which
        can be accessed by graph.node
        :param node: Node instance, the node to add
        :return None
        """
        if self.hasNode(node):
            return
        self._nodes.add(node)
        return node

    @property
    def nodes(self):
        return self._nodes

    def hasNode(self, node):
        """Checks the graph for the given node _name
        :param node: node instance
        :return: bool
        """
        return node in self._nodes

    def deleteNode(self, node):
        self._nodes.discard(node)

    def getNode(self, nodeName):
        return [item for item in self._nodes if item.name == nodeName]

    def clear(self):
        """
        :return:
        """
        self._nodes.clear()

    def allLeaves(self):
        leafNodes = []
        for node in self._nodes:
            if any(plug.connections for plug in node.plugs):
                continue
            leafNodes.append(node)

        if not leafNodes:
            return None

    def compute(self):
        for node in self._nodes:
            node.compute()