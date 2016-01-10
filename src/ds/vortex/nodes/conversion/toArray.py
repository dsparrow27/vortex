from ds.vortex.core import baseNode
from ds.vortex.core import plug as plugs


class ToArray(baseNode.BaseNode):
    def __init__(self, name):
        """
        :param name: str, the name of the node
        """
        baseNode.BaseNode.__init__(self, name)

    def initialize(self):
        baseNode.BaseNode.initialize(self)
        self.output = plugs.OutputPlug("output", self)
        self.valuePlug_ = plugs.InputPlug("value", self, value=[])
        self.addPlug(self.output, clean=True)
        self.addPlug(self.valuePlug_, clean=True)

        self.plugAffects(self.valuePlug_, self.output)

    def compute(self, requestPlug):
        baseNode.BaseNode.compute(self, requestPlug=requestPlug)
        if not requestPlug == self.output:
            return None
        result = [self.valuePlug_.value]
        requestPlug.value = result
        requestPlug.dirty = False
        return result


def getNode():
    """General function that returns our node, used to get create our node via Ui etc
    :return: Node instance
    """
    return ToArray
