import logging
import inspect
from collections import OrderedDict

logger = logging.getLogger(__name__)


class Graph(object):
    """This graph class stores the nodes and will evaluate the graph on request, to request a compute you will first need
    the output plug instance and then call Graph.requestEvaluate(outputPlug)
    """

    def __init__(self, name="", graph=None):
        """
        :param name: str, the name of the graph
        """
        self._name = name
        self._nodes = OrderedDict()
        self.graph = Graph

    def __repr__(self):
        return "{}{}".format(self.__class__.__name__, self.__dict__)

    def __len__(self):
        """Returns the length of the nodes in the graph
        :return: int, the length of nodes in this graph
        """
        return len(self._nodes)

    def __eq__(self, other):
        return isinstance(other, Graph) and self._nodes == other.nodes

    def addNode(self, node, **kwargs):
        """Adds a Node instance to the graph this will also add the node to the graph class instance as a attribute
        which can be accessed by graph.node
        :param node: Node instance, the node to add
        :param kwargs: plugName=plugValue, the kwargs sets the input plugs value.
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
        :return: OrderedDict
        """
        return self._nodes

    @nodes.setter
    def nodes(self, newNodes):
        self._nodes = newNodes

    def hasNode(self, node):
        """Checks the graph for the given node _name
        :param node: node instance
        :return: bool
        """
        return node in self._nodes.values()

    def deleteNode(self, node):
        """Removes a node from the graph
        :param node: the node instance to delete
        """
        del self._nodes[node.name]

    def getNode(self, nodeName):
        """Returns a node based on the name or empty list
        :param nodeName: the name of the node to get
        :return:Node instance
        """
        return self._nodes.get(nodeName)

    def generateUniqueName(self, node):
        """Create a unique name for the node in the graph, on node creation a digit is appended , eg nodeName00, nodeName01
        :param node: node Instance
        :return: str, returns the new node name as a string
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

    def requestEvaluate(self, outputPlug):
        """Computes the appropriate nodes for the output plug, will evaluate all dirty plugs/nodes that need to be done
        for this plug
        :param outputPlug: plug instance to compute
        """
        if not outputPlug.dirty:
            return outputPlug.value

        node = outputPlug.node
        for plug in node.inputs():
            if plug.dirty:
                if not plug.isConnected():
                    # mark clean
                    plug.dirty = False
                    continue
                connectedPlug = plug.connections[0]
                logger.debug("requesting plug ::{0}, nodeName::{1}".format(connectedPlug.name, connectedPlug.node.name))
                if connectedPlug.dirty:
                    self.requestEvaluate(connectedPlug)
                plug.value = connectedPlug.value
                plug.dirty = False

        node.compute()
        logger.debug("computed output is::{0}, nodeName::{1}, plug::{2}".format(outputPlug.value, node.name,
                                                                                outputPlug.name))

    def serializeGraph(self):
        logger.debug("serializing graph")
        serializedGraph = {"name": self._name,
                           "version": "1.0.0",
                           "nodes": OrderedDict(),
                           "className": type(self).__name__,
                           "moduleName": inspect.getmodulename(__file__),
                           "modulePath": __file__.replace("\\", ".").split("src.")[-1].replace(".pyc", "").replace(
                               ".py", "")
                           }
        logger.debug(serializedGraph)
        for node in self._nodes.values():
            serializedGraph["nodes"][node.name] = node.serialize()

        return serializedGraph

    @classmethod
    def loadGraph(cls, graphData):
        graph = cls(name=graphData.get("name"))
        for node in graphData["nodes"].values():
            modulePath = node.get("modulePath")
            try:
                module = __import__(modulePath, globals(), locals(), [node.get("moduleName")], -1)
            except ImportError, er:
                logger.error("""importing {0} Failed! , have you typed the right name?,
                    check self.modulesDict for availablesModules.""".format(modulePath))
                raise er
            newNode = module.getNode()(name=node.get("name"))
            newNode.addPlugsFromDict(node.get("plugs"))
            graph.addNode(newNode)
        return graph


class IncrementObject(object):
    """A class to help with incrementing a number with a padding
    """

    def __init__(self, startNumber, padding):
        """initializes the seq number with start number and a padding value, use self.add() to add one number
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
