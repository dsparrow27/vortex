import inspect
from ds.vortex import customLogger as customLogger
from ds.vortex.core import baseEdge
from ds.vortex.core import vortexEvent

log = customLogger.getCustomLogger()


class BasePlug(object):
    """Base Plug class , inputs and output plug is derived from this class
    """

    def __init__(self, name, node=None, value=None):
        """
        :param name: str, the name for the plug
        :param node: BaseNode instance, the parent node
        :param value: anything, data storage that this plug is equal to eg. float value, gets used by the compute method in the node
        """
        self.dirtyStateChanged = vortexEvent.VortexSignal()  # emits plug instance, dirty state (bool)
        self.valueChanged = vortexEvent.VortexSignal()  # emits plug instance, plug value
        self.valueRequested = vortexEvent.VortexSignal()  # emits plug instance, plug value
        self.connectionAdded = vortexEvent.VortexSignal()  # emits plug instance, edge instance
        self.connectionRemoved = vortexEvent.VortexSignal()  # emits edge instance
        self.name = name
        self._node = node
        self._io = "input"
        self._connections = []
        self._dirty = False  # false is clean
        self._value = value
        self.affects = set()

    def __repr__(self):
        return "{}{}".format(self.__class__.__name__, self.__dict__)

    def __len__(self):
        """returns the length of the connections
        :return: int, the amount of connections
        """
        return len(self._connections)

    @property
    def dirty(self):
        """gets the dirty state of the plug
        :return: bool
        """
        return self._dirty

    @dirty.setter
    def dirty(self, value):
        """sets the dirty state of the plug
        :param value: bool, the dirty state(False==clean, True==dirty)
        :return: None
        """
        self._dirty = value
        if self.isConnected():
            for edge in self.connections:
                if edge.input.dirty:
                    continue
                edge.input.dirty = value
        self.dirtyStateChanged.emit(self, value)

    @property
    def value(self):
        """Return the value of the plug, this can have any data type.
        :return: Type(), returns whatever value for the plug(used in compute function)
        """
        return self._value

    @value.setter
    def value(self, value):
        """sets the value of the plug, can have any data type and any value eg. custom python object, dict etc.
        The function will also set the plug to dirty
        :param value: the value to give the plug
        :return: None
        """
        self._value = value
        self.valueChanged.emit(self, value)

    @property
    def node(self):
        """Returns the parent node
        :return: BaseNode instance
        """
        return self._node

    @property
    def io(self):
        """Returns the input output value
        :return: str
        """
        return self._io

    @property
    def connections(self):
        """returns the plug connections
        :return: set(BasePlug)
        """
        return self._connections

    def isInput(self):
        """Returns true is io type is input
        :return: bool
        """
        return self._io == "input"

    def isOutput(self):
        """Returns true is io type is output
        :return: bool
        """
        return self._io == "output"

    def isConnected(self):
        """Returns True if self is connected to another plug
        :return: bool
        """
        if self._connections:
            return True
        return False

    def isConnectedTo(self, plug):
        """Determines if self is connected to the plug, calls on BaseEdge.isConnected()
        :param plug: Plug instance
        :return: bool
        """
        return any(edge.isConnected(self, plug) for edge in self._connections)

    def getConnection(self, plug):
        """returns the edge that is connected to the plug and self
        :param plug: InputPlug or OutputPlug
        :return: BaseEdge
        """
        for edge in self._connections:
            match = edge.isConnected(self, plug)
            if match:
                return edge

    def disconnect(self, plug):
        """Removes the plug from the connections list
        :param plug: plug instance
        :return: None
        """
        log.debug("Could not find plug in connections")
        for index, edge in enumerate(self._connections):
            if edge.isConnected(self, plug):
                edge.delete()
                self.connectionRemoved.emit(edge)

    def disconnectAll(self):
        """Removes all connections for the plug, emit the connectionRemoved signal
        """
        for index, edge in enumerate(self._connections):
            edge.delete()
            self.connectionRemoved.emit(edge)
            del self._connections[index]

    def connect(self, plug):
        """Connects two attributes together if self isInput type then if there's a current connections then this gets
        replaced.
        :param plug: BasePlug, InputPlug or Outputplug instance
        """
        log.debug("connected plugs::".format(plug.name, self.name))

    def serialize(self):
        """Serializes the plug as a dict
        :return: dict,
        """
        data = {"name": self.name,
                "io": self.io,
                "value": self._value,
                "moduleName": inspect.getmodulename(__file__)
                }
        return data

    def fullPath(self):
        """Returns the fullpath of the plug , eg nodeName|plugName
        :return: str
        """
        return "{0}|{1}".format(self.node.name, self.name)


class InputPlug(BasePlug):
    def __init__(self, name, node=None, value=None):
        """
        :param name: str, the name for the plug
        :param node: BaseNode instance, the parent node
        :param value: anything, data storage that this plug is equal to eg. float value, gets used by the compute method
        in the node
        """
        BasePlug.__init__(self, name, node, value)
        self._io = "input"

    @property
    def value(self):
        """Return the value of the plug, this can have any data type.
        :return: Type(), returns whatever value for the plug(used in compute function)
        """
        if not self.dirty:
            return self._value
        if not self.isConnected():
            self.dirty = False
            return self._value
        edge = self.connections[0]
        connectedValue = edge.output.value
        self.value = connectedValue
        self.dirty = False
        return self._value

    @value.setter
    def value(self, value):
        """sets the value of the plug, can have any data type and any value eg. custom python object, dict etc.
        The function will also set the plug to dirty
        :param value: the value to give the plug
        :return: None
        """
        # pass the value to all connected plugs if it is connected
        self._value = value
        self.dirty = True
        self.valueChanged.emit(self, value)

    @property
    def dirty(self):
        return self._dirty

    @dirty.setter
    def dirty(self, value):
        self._dirty = value
        for plug in self.affects:
            if plug.dirty:
                continue
            plug.dirty = value
        self.dirtyStateChanged.emit(self, value)

    def connect(self, plug):
        """Creates a connection between to plugs, a input can only have one input so current connections is cleared
        before creating the new connection
        :param plug: BasePlug instance

        :return:
        """
        if plug.isInput() or self.getConnection(plug):
            return
        edge = baseEdge.Edge(self.name + "_" + plug.name, inputPlug=self, outputPlug=plug)
        self.dirty = True
        self.connectionAdded.emit(edge)
        return edge


class OutputPlug(BasePlug):
    def __init__(self, name, node=None, value=None):
        """
        :param name: str, the name for the plug
        :param node: BaseNode instance, the parent node
        :param value: anything, data storage that this plug is equal to eg. float value, gets used by the compute method
        in the node
        """
        BasePlug.__init__(self, name, node, value)
        self._io = "output"

    @property
    def value(self):
        """Return the value of the plug, this can have any data type.
        :return: Type(), returns whatever value for the plug(used in compute function)
        """
        if self.dirty:
            self._node.compute(self)
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of the plug, can have any data type and any value eg. custom python object, dict etc.
        The function will also set the plug to dirty
        :param value: the value to give the plug
        :return: None
        """
        self._value = value

    def connect(self, plug, edge=None):
        if not self.isConnectedTo(plug) or not plug.isOutput():
            edge = plug.getConnection(self)
            if not edge:
                edge = baseEdge.Edge("_".join([self.name, plug.name]), inputPlug=plug, outputPlug=self)
                self.connectionAdded.emit(edge)
                return edge
            edge.connect(plug, self)
            self.connectionAdded.emit(edge)
            return edge
