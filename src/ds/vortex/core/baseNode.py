
class BaseNode(object):
    def __init__(self, name):
        """
        :param name: str, the name of the node
        :param value:
        """
        self.name = name
        self._plugs = set()

    def __repr__(self):
        return "{}{}".format(self.__class__.__name__, self.__dict__)

    def __eq__(self, other):
        return isinstance(other, BaseNode) and self.plugs == other.plugs

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
        self._plugs.add(plug)

    def getPlug(self, plugName):
        """Returns the plug based on the name
        :param plugName: str, the plug name to get
        :return: plug instance or None
        """
        plugs = [plug for plug in self._plugs if plug.name == plugName]
        if plugs:
            return plugs[0]

    def deletePlug(self, plug):
        """Removes the plug from the node
        :param plug:
        """
        self._plugs.discard(plug)

    def inputs(self):
        """Finds and returns all the inputs for self
        :return: list(Plug)
        """
        return [plug for plug in self._plugs if plug.isInput()]

    def outputs(self):
        """Finds and returns all the outputs for self
        :return: list(Plug)
        """
        return [plug for plug in self._plugs if plug.isOutput()]

    def compute(self):
        """Intended to be overridden
        :return: None
        """
        pass
