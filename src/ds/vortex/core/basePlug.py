import logging

logger = logging.getLogger(__name__)


class BasePlug(object):
    """Base Plug class that should be a child of a node class.
    """

    def __init__(self, name, node, attributeType, io="input"):
        """
        :param name: str, the name for the plug
        :param node: BaseNode instance, the parent node
        :param attributeType: any python type eg, float, int etc
        :param io: str, input or output, whether this plug is an input or output
        """
        self.name = name
        self._node = node
        self._io = io
        self._type = attributeType
        self._connections = set()
        self.dirty = False

    def __repr__(self):
        return "{}{}".format(self.__class__, self.__dict__)

    def __eq__(self, other):
        """Test the equality between two plug classes are the same, for this to return true the
        self.type and _io needs to be the same
        :param other: BasePlug instance
        :return: bool
        """
        if not isinstance(other, BasePlug):
            return False
        return other.type == self._type and self._io == other.io and self._node == other.node

    def __ne__(self, other):
        return not self == other

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
    def type(self):
        """Returns the plug type , any std type eg, float
        :return: std types
        """
        return self._type

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

        if not self.canConnect(plug):
            logger.error("{} is not of the same type".format(plug.name))
            return
        if self.isInput:
            self._connections.clear()
        self._connections.add(plug)

    def isConnected(self):
        """Returns True if self is connected to another plug
        :return: bool
        """
        if self._connections:
            return True
        return False

    def canConnect(self, plug):
        """Test's the plug to see if its a valid plug that can be connected to self, fails if type is different or
        io is the same
        :param plug: Plug
        """
        return self.type == plug.type and self.io != plug.io

    def disconnect(self, plug):
        """Removes the plug from the connections list
        :param plug: baseAttribute instance
        :return: bool
        """

        self._connections.discard(plug)
