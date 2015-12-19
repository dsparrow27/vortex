import logging

logger = logging.getLogger(__name__)


class BasePlug(object):
    """Base Plug class that should be a child of a node class.
    """

    def __init__(self, name, node, value=None):
        """
        :param name: str, the name for the plug
        :param node: BaseNode instance, the parent node
        :param value: anything, data storage that this plug is equal to eg. float value, gets used by the compute method in the node
        """
        self.name = name
        self._node = node
        self._io = "input"
        self._connections = []
        self.dirty = False
        self.value = value

    def __repr__(self):
        return "{}{}".format(self.__class__, self.__dict__)

    def __len__(self):
        return len(self._connections)

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

    def connect(self, plug):
        """Connects two attributes together if self isinput type then if theres a current connections then this gets
        replaced.
        :param plug: BasePlug instance
        :return: None
        """

        if self.isInput:
            self._connections = []
        self._connections.append(plug)

    def isConnected(self):
        """Returns True if self is connected to another plug
        :return: bool
        """
        if self._connections:
            return True
        return False

    def disconnect(self, plug):
        """Removes the plug from the connections list
        :param plug: baseAttribute instance
        :return: bool
        """
        del self._connections[self._connections.index(plug)]

    def log(self, tabLevel=-1):

        output = ""
        tabLevel += 1

        for i in range(tabLevel):
            output += "\t"

        output += "|------" + self.name + " ------connections -->> {}\n".format(self._connections)

        tabLevel -= 1
        output += "\n"

        return output

    def fullPath(self):
        """Returns the fullpath of the is plug , eg nodeName|plugName
        :return: str
        """
        return "{0}|{1}".format(self.node.name, self.name)


class InputPlug(BasePlug):
    def __init__(self, name, node, value=None):
        """
        :param name: str, the name for the plug
        :param node: BaseNode instance, the parent node
        :param value: anything, data storage that this plug is equal to eg. float value, gets used by the compute method in the node
        """
        super(InputPlug, self).__init__(name, node, value)
        self._io = "input"


class OutputPlug(BasePlug):
    def __init__(self, name, node, value=None):
        """
        :param name: str, the name for the plug
        :param node: BaseNode instance, the parent node
        :param value: anything, data storage that this plug is equal to eg. float value, gets used by the compute method in the node
        """
        super(OutputPlug, self).__init__(name, node, value)

        self._io = "output"
