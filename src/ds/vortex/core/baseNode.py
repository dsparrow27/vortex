from collections import OrderedDict


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
        return isinstance(other, BaseNode) and self.plugs == other.plugs

    def __len__(self):
        return len(self._ports)

    @property
    def plugs(self):
        """Returns the the plugs for this node
        :return: set(Plug)
        """
        return self._plugs

    def addPlug(self, plug):
        """Adds a plug to self
        :param plug: Plug instance
        """
        self._plugs[plug.name] = plug

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
        for name, plug in self._plugs.iteritems():
            if plug.isInput():
                inputs.append(plug)
        return inputs

    def outputs(self):
        """Finds and returns all the outputs for self
        :return: list(Plug)
        """
        outputs = []
        for name, plug in self._plugs.iteritems():
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
        pass

    def log(self, tabLevel=-1):

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
