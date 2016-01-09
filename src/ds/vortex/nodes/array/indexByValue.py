from ds.vortex.core import baseNode
from ds.vortex.core import plug as plugs


class ArrayIndexNode(baseNode.BaseNode):
    def __init__(self, name):
        """
        :param name: str, the name of the node
        """
        baseNode.BaseNode.__init__(self, name)

    def initialize(self):
        baseNode.BaseNode.initialize(self)
        self.outputPlug_ = plugs.OutputPlug("output", self)
        self.addPlug(self.outputPlug_, clean=True)
        self.arrayPlug_ = plugs.OutputPlug("array", self, value=[])
        self.valuePlug_ = plugs.InputPlug("value", self, value=0)

        self.addPlug(self.arrayPlug_, clean=True)
        self.addPlug(self.valuePlug_, clean=True)

        self.plugAffects(self.arrayPlug_, self.outputPlug_)
        self.plugAffects(self.valuePlug_, self.outputPlug_)

    def compute(self, requestPlug):
        baseNode.BaseNode.compute(self, requestPlug=requestPlug)
        if requestPlug != self.outputPlug_:
            return None
        value = self.valuePlug_.value
        array = self.arrayPlug_.value

        if value in array:
            result = array.index(value)
        else:
            return
        requestPlug.value = result
        requestPlug.dirty = False

        return result


def getNode():
    """General function that returns our node, used to get create our node via Ui etc
    :return: Node instance
    """
    return ArrayIndexNode
