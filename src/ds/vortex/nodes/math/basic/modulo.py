from ds.vortex.core import baseNode
from ds.vortex.core import plug as plugs


class ModuloNode(baseNode.BaseNode):

    def __init__(self, name):
        """
        :param name: str, the name of the node
        """
        baseNode.BaseNode.__init__(self, name)

    def initialize(self):
        baseNode.BaseNode.initialize(self)
        self.outputPlug_ = plugs.OutputPlug("output", self)
        self.valuePlug_ = plugs.InputPlug("value", self, value=0)
        self.moduloBy = plugs.InputPlug("moduloBy", self, value=0)

        self.addPlug(self.outputPlug_, clean=True)
        self.addPlug(self.valuePlug_, clean=True)
        self.addPlug(self.moduloBy, clean=True)

        self.plugAffects(self.valuePlug_, self.outputPlug_)
        self.plugAffects(self.moduloBy, self.outputPlug_)

    def compute(self, requestPlug):
        baseNode.BaseNode.compute(self, requestPlug=requestPlug)
        if requestPlug != self.outputPlug_:
            return None

        result = self.valuePlug_.value % self.moduloBy.value

        requestPlug.value = result
        requestPlug.dirty = False

        return result


def getNode():
    """General function that returns our node, used to get create our node via Ui etc
    :return: Node instance
    """
    return ModuloNode
