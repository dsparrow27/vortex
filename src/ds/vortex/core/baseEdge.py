import inspect
from ds.vortex import customLogger as customLogger
from ds.vortex.core import vortexEvent

logger = customLogger.getCustomLogger()


class Edge(object):
    """Base class for graph edges , a simple class that holds the connection values of plugs,
    """
    deleted = vortexEvent.VortexSignal()  # emit nothing
    connected = vortexEvent.VortexSignal()  # emit inputPlug instance, outputPlug instance

    def __init__(self, name="edge", inputPlug=None, outputPlug=None):
        """
        :param name: str, the name for the edge
        :param inputPlug: InputPlug instance, the input plug instance
        :param outputPlug: OutputPlug instance, the output plug instance
        """
        if inputPlug is not None and outputPlug is not None:
            self.connect(inputPlug, outputPlug)
        if not name and inputPlug and outputPlug:
            self.name = inputPlug.name + "_" + outputPlug.name
        self.name = name
        self.input = inputPlug
        self.output = outputPlug

    def __repr__(self):
        return "{0} {1}".format(self.__class__.__name__, self.__dict__)

    def __eq__(self, other):
        return isinstance(other, Edge) and self.input == other.input and self.output == other.output

    def delete(self):
        """Preps for deletion by first disconnecting the edge from the plug.
        Emit the deleted signal
        """
        self.input._connections = []
        for index, connection in enumerate(self.output.connections):
            if connection == self:
                outputConnections = self.output.connections
                if index in range(len(outputConnections)):
                    del outputConnections[index]

                break
        self.deleted.emit()

    def isConnected(self, plug1, plug2):
        return plug1 == self.input and \
               plug2 == self.output or \
               plug1 == self.output and \
               plug2 == self.input

    def connect(self, input, output):
        self.input = input
        self.output = output
        input._connections = [self]
        if self not in output.connections:
            output.connections.append(self)
        self.input.dirty = True
        self.connected.emit(input, output)

    def serialize(self):
        """Returns a dict of the input, output and the arbitraryData
        :return: dict
        """
        return {"name": self.name,
                "input": (self.input.name, self.input.node.name),
                "output": (self.output.name, self.output.node.name),
                "moduleName": inspect.getmodulename(__file__)
                }
