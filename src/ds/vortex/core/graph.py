import logging

logging.getLogger(__name__)


class Graph(object):
    def __init__(self, name=""):
        """
        :param name: str, the name of the graph to set
        """
        self._name = name
        self._nodes = set()

    def __repr__(self):
        return "{}{}".format(self.__class__.__name__, self.__dict__)

    def __len__(self):
        return len(self._nodes)

    def addNode(self, node):
        """Adds a Node instance to the graph this will also add the node to the graph class instance as a attribute
        which can be accessed by graph.node
        :param node: Node instance, the node to add
        :return None
        """
        if self.hasNode(node):
            return
        self._nodes.add(node)
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
        return node in self._nodes

    def deleteNode(self, node):
        """Removes a node from the graph
        :param node:
        """
        self._nodes.discard(node)

    def getNode(self, nodeName):
        """Returns a node based on the name or empty list
        :param nodeName:
        :return:
        """
        return [item for item in self._nodes if item.name == nodeName]

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
        for node in self._nodes:
            if any(plug.connections for plug in node.inputs()):
                continue
            leafNodes.append(node)
        return leafNodes

    def compute(self):
        pass