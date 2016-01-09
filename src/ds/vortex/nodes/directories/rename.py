import os
from ds.vortex.core import baseNode
from ds.vortex.core import plug as plugs


class RenameNode(baseNode.BaseNode):
    def __init__(self, name):
        """
        :param name: str, the name of the node
        """
        baseNode.BaseNode.__init__(self, name)

    def initialize(self):
        baseNode.BaseNode.initialize(self)
        self.outputPlug_ = plugs.OutputPlug("output", self)
        self.sourcePlug_ = plugs.InputPlug("source", self, [])
        self.destinationPlug_ = plugs.InputPlug("destination", self, [])

        self.addPlug(self.outputPlug_, clean=True)
        self.addPlug(self.sourcePlug_, clean=True)
        self.addPlug(self.destinationPlug_, clean=True)

        self.plugAffects(self.sourcePlug_, self.outputPlug_)
        self.plugAffects(self.destinationPlug_, self.outputPlug_)

    def compute(self, requestPlug):
        baseNode.BaseNode.compute(self, requestPlug=requestPlug)
        if requestPlug != self.outputPlug_:
            return None
        source = list(self.sourcePlug_.value)
        destination = list(self.destinationPlug_.value)
        [os.rename(src, destination[i]) for i, src in enumerate(source)]

        requestPlug.value = destination
        requestPlug.dirty = False
        return destination


def getNode():
    """General function that returns our node, used to get create our node via Ui etc
    :return: Node instance
    """
    return RenameNode
