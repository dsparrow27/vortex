from collections import OrderedDict
import logging

logger = logging.getLogger(__name__)


class BaseNode(object):
    def __init__(self, name):
        """
        :param name: str, the name of the node
        """
        self.name = name
        self._plugs = OrderedDict()
        self.initialize()

    def __repr__(self):
        return "{}{}".format(self.__class__.__name__, self.__dict__)

    def __eq__(self, other):
        """Determines if the node and its plugs equal
        :param other:
        :return:
        """
        return isinstance(other, BaseNode) and self.plugs == other.plugs

    def __len__(self):
        """Return the length of the plugs for this node
        :return: int
        """
        return len(self._plugs)

    @property
    def plugs(self):
        """Returns the the plugs for this node
        :return: set(Plug)
        """
        return self._plugs

    def addPlug(self, plug, value=None):
        """Adds a plug to self
        :param plug: Plug instance to add
        :param value: any type, This argument get passed to the plug value attribute
        """
        self._plugs[plug.name] = plug
        plug.value = value

    def getPlug(self, plugName):
        """Returns the plug based on the name
        :param plugName: str, the plug name to get
        :return: plug instance or None
        """
        return self._plugs.get(plugName)

    def deletePlug(self, plug):
        """Removes the plug from the node
        :param plug:
        """
        del self._plugs[plug.name]

    def inputs(self):
        """Finds and returns all the inputs for self
        :return: list(Plug)
        """
        inputs = []
        for plug in self._plugs.values():
            if plug.isInput():
                inputs.append(plug)
        return inputs

    def outputs(self):
        """Finds and returns all the outputs for self
        :return: list(Plug)
        """
        outputs = []
        for plug in self._plugs.values():
            if plug.isOutput():
                outputs.append(plug)
        return outputs

    def initialize(self):
        """Intended to be overridden, this method is for cresting plugs, for the node before this node gets computed for the first time
        :return: None
        """
        pass

    def compute(self):
        """Intended to be overridden
        :return: None
        """
        logger.debug("Computing {}".format(self.name))

    def log(self, tabLevel=-1):
        """Return the hierarchy for this node including the plugs
        :param tabLevel: int, spacing
        :return: str
        """
        output = ""
        tabLevel += 1

        for i in range(tabLevel):
            output += "\t"

        output += "|------" + self.name + "\n"

        for child in self._plugs.values():
            output += child.log(tabLevel)

        tabLevel -= 1
        output += "\n"

        return output
