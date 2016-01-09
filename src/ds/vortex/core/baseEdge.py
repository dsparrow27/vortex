import inspect
from ds.vortex import customLogger as customLogger

logger = customLogger.getCustomLogger()


class Edge(object):
    """Base class for graph edges , a simple class that holds the connection values of plugs,
    """

    def __init__(self, name, input=None, output=None, arbitraryData=None):
        """
        :param name: str, the name for the edge
        :param input: InputPlug instance, the input plug instance
        :param output: OutputPlug instance, the output plug instance
        :param arbitraryData: any extra edge data, should be serializable eg dict,list
        """
        self.name = name
        self.input = input
        self.output = output
        self.arbitraryData = arbitraryData

    def __repr__(self):
        return "{0}{1}".format(self.__class__.__name__, self.__dict__)

    def __eq__(self, other):
        return isinstance(other, Edge) and self.input == other.input and self.output == other.output

    def delete(self):
        if 0 in range(len(self.input.connections)):
            self.input._connections = []
        for index, connection in enumerate(self.output.connections):
            if connection == self:
                outputConnections = self.output.connections
                if index in range(len(outputConnections)):
                    del outputConnections[index]
                break

    def isConnected(self, plug1, plug2):
        return plug1 == self.input and \
               plug2 == self.output or \
               plug1 == self.output and \
               plug2 == self.input

    def connect(self, input, output):
        self.input = input
        self.output = output
        input._connection = [self]
        if self not in output.connections:
            output.connections.append(self)

    def serialize(self):
        """Returns a dict of the input, output and the arbitraryData
        :return: dict
        """
        inputNode = self.input.node
        outputNode = self.output.node
        inputNodeName = None
        outputNodeName = None
        if inputNode:
            inputNodeName = inputNode.name
        if outputNode:
            outputNodeName = outputNode.name
        data = {"name": self.name,
                "className": type(self).__name__,
                "moduleName": inspect.getmodulename(__file__),
                "modulePath": __file__.replace("\\", ".").split("src.")[-1].replace(".pyc", "").replace(".py", ""),
                "input": (self.input.name, inputNodeName),
                "output": (self.output.name, outputNodeName),
                "arbitraryData": self.arbitraryData
                }
        return data
