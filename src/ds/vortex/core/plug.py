import inspect
from ds.vortex.core import baseEdge
from ds.vortex import customLogger as customLogger
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
        self.name = name
        self._node = node
        self._io = "input"
        self._connections = []
        self._dirty = False  # false is clean
        self._value = value
        self.affects = set()

    def __repr__(self):
        return "{}{}".format(self.__class__, self.__dict__)

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
        self.dirty = True

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
        for edge in self._connections:
            if edge.isConnected(self, plug):
                return True
        return False

    def getConnection(self, plug):
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

    def connect(self, plug):
        """Connects two attributes together if self isInput type then if there's a current connections then this gets
        replaced.
        :param plug: BasePlug, InputPlug or Outputplug instance
        :return: edge
        """
        log.debug("connecting plugs::".format(plug.name, self.name))

    def serialize(self):
        """Serializes the plug as a dict
        :return: dict,
        """
        data = {"name": self.name,
                "io": self.io,
                "value": self._value,
                "className": type(self).__name__,
                "moduleName": inspect.getmodulename(__file__),
                "modulePath": __file__.replace("\\", ".").split("src.")[-1].replace(".pyc", "").replace(".py", "")
                }
        return data

    def log(self, tabLevel=-1):
        """
        :param tabLevel: int, the tab size
        :return: str, the logged string that can be used to print
        """
        output = ""
        tabLevel += 1

        for i in range(tabLevel):
            output += "\t"

        output += "|------" + self.name + " ------connections -->> {}\n".format(self._connections)

        tabLevel -= 1
        output += "\n"

        return output

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
        return self._value

    @value.setter
    def value(self, value):
        """sets the value of the plug and sets the plug dirty, calls on the parent node setDownStreamDirty(inputPlug)
        :param value: the value to set
        """
        # pass the value to all connected plugs if it is connected
        self._value = value
        self.dirty = True
        self._node.setDownStreamDirty(self)

    def connect(self, plug):
        """creates a connection between to plugs, a input can only have one input so current connections is cleared
        before creating the new connection
        :param plug:
        :return:
        """
        if plug.isInput() or self.getConnection(plug):
            return
        edge = baseEdge.Edge(self.name + "_" + plug.name, input=self, output=plug)
        if self._connections:
            self._connections[0].delete()
        # inputs can only have a single connection
        self._connections = [edge]
        plug.connect(self)
        try:
            self.node.setDownStreamDirty(self)
        except AttributeError:
            log.debug("plug has no node parent::{}".format(self.name))

        self.dirty = True

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

    def connect(self, plug):
        if not self.isConnectedTo(plug):
            edge = plug.getConnection(self)
            if not edge:
                edge = baseEdge.Edge(self.name + "_" + plug.name, input=plug, output=self)
            self._connections.append(edge)
            plug.connect(self)