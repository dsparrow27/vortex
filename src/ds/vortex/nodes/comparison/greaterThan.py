from ds.vortex.core import baseNode
from ds.vortex.core import plug as plugs


class GreaterThanNode(baseNode.BaseNode):
    def __init__(self, name):
        """
        :param name: str, the name of the node
        """
        baseNode.BaseNode.__init__(self, name)

    def initialize(self):
        baseNode.BaseNode.initialize(self)
        self.outputPlug_ = plugs.OutputPlug("output", self)
        self.addPlug(self.outputPlug_, clean=True)
        self.value1Plug_ = plugs.InputPlug("value1", self, value=0)
        self.value2Plug_ = plugs.InputPlug("value2", self, value=0)

        self.addPlug(self.value1Plug_, clean=True)
        self.addPlug(self.value2Plug_, clean=True)

        self.plugAffects(self.value1Plug_, self.outputPlug_)
        self.plugAffects(self.value2Plug_, self.outputPlug_)

    def compute(self, requestPlug):
        baseNode.BaseNode.compute(self, requestPlug=requestPlug)
        if requestPlug != self.outputPlug_:
            return None
        result = self.value1Plug_ > self.value2Plug_

        requestPlug.value = result
        requestPlug.dirty = False
        return result


def getNode():
    """General function that returns our node, used to get create our node via Ui etc
    :return: Node instance
    """
    return GreaterThanNode
