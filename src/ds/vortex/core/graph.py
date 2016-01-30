import inspect
from collections import OrderedDict
import baseEdge
from ds.vortex import customLogger
from ds.vortex.core import baseNode
from ds.vortex.core import vortexEvent
from ds.vortex.nodes import allNodes

logger = customLogger.getCustomLogger()


class Graph(object):
    """This graph class stores the nodes and will evaluate the graph on request.
    Simple example:
    gx = Graph("newGraph")
    t = addNode.AddNode("newMathNode") # first create an instance of the node
    gx.addNode(t) # adds a node to the graph
    gx.getNode("newMathNode") # gets node by name
    if t in gx:
        print t.name # check to see if newNode is in the graph
    """
    addedNode = vortexEvent.VortexSignal()
    removedNode = vortexEvent.VortexSignal()
    addedEdge = vortexEvent.VortexSignal()
    deletedEdge = vortexEvent.VortexSignal()

    def __init__(self, name=""):
        """
        :param name: str, the name of the graph
        """
        self._edges = OrderedDict()
        self._name = name
        self._nodes = OrderedDict()

    def __repr__(self):
        return "{}{}".format(self.__class__.__name__, self.__dict__)

    def __len__(self):
        """Returns the length of the nodes in the graph
        :return: int, the length of nodes in this graph
        """
        return len(self._nodes)

    def __eq__(self, other):
        return isinstance(other, Graph) and self._nodes == other.nodes

    def __getitem__(self, index):
        """Gets a node from the graph via a index
        :param index: int, the node index
        :return: Node
        """
        if index in range(self._nodes.values()):
            return self._nodes.values()[index]
        elif index in range(self._edges.values()):
            return self._edges.values()[index]

    def __contains__(self, node):
        """Returns a bool if the node is in the graph
        :param node: BaseNode instance
        :return:bool
        """
        try:
            return node in self._nodes.values()
        except TypeError:
            return False

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
        for plug in node.plugs.values():
            plug.connectionAdded.connect(self.addEdge)
            plug.connectionRemoved.connect(self.deleteEdge)
        self.addedNode.emit(node)
        return node

    @property
    def nodes(self):
        """Returns all the nodes in the graph
        :return: OrderedDict
        """
        return self._nodes

    @nodes.setter
    def nodes(self, newNodes):
        """Empties and sets the nodes dict
        :param newNodes: dict
        """
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
        self.removedNode.emit(node)

    def getNode(self, nodeName):
        """Returns a node based on the name or empty list
        :param nodeName: the name of the node to get
        :return:Node instance
        """
        return self._nodes.get(nodeName)

    @property
    def edges(self):
        """Returns a dict of the graph edges
        :return: Dict
        """
        return self._edges

    def getEdge(self, edgeName):
        """Returns a edge if the edge name is in edges
        :param edgeName: str, th name of the edge
        :return:
        """
        return self._edges.get(edgeName)

    def addEdge(self, edge):
        """Adds the edge to the graph
        :param edge: Edge
        """
        if edge not in self._edges.values():
            self._edges[edge.name] = edge
            self.addedEdge.emit(edge)

    def deleteEdge(self, edge):
        """Removes the edge from the graph
        :param edge: Edge
        """
        if edge in self._edges.values():
            tmpEdge = edge
            del self._edges[edge.name]
            self.deletedEdge.emit(tmpEdge)

    def generateUniqueName(self, node):
        """Create a unique name for the node in the graph, on node creation a digit is appended , eg nodeName00, nodeName01
        :param node: node Instance
        :return: str, returns the new node name as a string
        """
        value = "%0{}d".format(0)
        uIndex = 0
        name = node.name
        while name in self._nodes:
            name = node.name + value % uIndex
            uIndex += 1
        return name

    def clear(self):
        """Clears all the nodes and the edges from the graph
        :return: None
        """
        self._nodes.clear()
        self._edges.clear()

    def allLeaves(self):
        """Returns all the leaf nodes in the graph, a Leaf node is any node that has on connections
        :return: list(Node)
        """
        leafNodes = []

        for node in self._nodes.values():
            if not all(plug.connections for plug in node.inputs()):
                leafNodes.append(node)

        return leafNodes

    def serializeGraph(self):
        """Creates a python dict from the graph, each node,plug and edge gets serialized
        :return:
        """
        logger.debug("serializing graph")
        serializedGraph = {"name": self._name,
                           "version": "1.0.0",
                           "nodes": OrderedDict(),
                           "edges": dict(),
                           "moduleName": inspect.getmodulename(__file__)
                           }
        logger.debug(serializedGraph)
        for node in self._nodes.values():
            serializedGraph["nodes"][node.name] = node.serialize()
        for edge in self._edges.values():
            serializedGraph["edges"][edge.name] = edge.serialize()

        return serializedGraph

    @classmethod
    def loadGraph(cls, graphData):
        """load a vortex graph dict creates and returns a graph object
        :param graphData: dict
        :return: Graph()
        """
        graph = cls(name=graphData.get("name"))
        for node in graphData["nodes"].values():
            moduleName = node.get("moduleName")
            nodeName = node.get("name")

            if moduleName == "baseNode":
                newNode = baseNode.BaseNode(name=nodeName)
            else:
                newNode = allNodes.getNode(node.get("moduleName"))(name=nodeName)
            for plugName, values in node.get("plugs").iteritems():
                plug = newNode.getPlug(plugName=plugName)
                if plug:
                    plug.value = values.get("value")
                    continue
                #?????????????????????????????
                newNode.addPlugByType(ioType=values.get("io"), name=plugName, value=values.get("value"))
            graph.addNode(newNode)

        for edge in graphData["edges"].values():
            inputPlug = graph.getNode(edge["input"][1]).getPlug(edge["input"][0])
            outputPlug = graph.getNode(edge["output"][1]).getPlug(edge["output"][0])
            baseEdge.Edge(name=edge["name"], inputPlug=inputPlug, outputPlug=outputPlug)

        return graph
