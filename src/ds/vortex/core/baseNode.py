
class BaseNode(object):
    def __init__(self, name, value=None):
        self._name = name
        self._plugs = set()
        self.value = value

    def __repr__(self):
        return "{}{}".format(self.__class__.__name__, self.__dict__)

    def __eq__(self, other):
        return isinstance(other, BaseNode) and self.plugs == other.plugs

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def plugs(self):
        return self._plugs

    def addPlug(self, plug):
        self._plugs.add(plug)

    def getPlug(self, plugName):
        plugs = [plug for plug in self._plugs if plug.name == plugName]
        if plugs:
            return plugs[0]


    def deletePlug(self, plug):
        self._plugs.discard(plug)

    def inputs(self):
        return [plug for plug in self._plugs if plug.isInput()]

    def outputs(self):
        return [plug for plug in self._plugs if plug.isOutput()]

    def compute(self):
        """Intended to be overridden
        :return: None
        """
        pass
