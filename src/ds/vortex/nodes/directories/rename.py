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
        self.addPlug(plugs.OutputPlug("output", self), clean=True)
        self.addPlug(plugs.InputPlug("source", self), [], clean=True)
        self.addPlug(plugs.InputPlug("destination", self), [], clean=True)

    def compute(self):
        baseNode.BaseNode.compute(self)
        source = list(self.getPlug("source").value)
        destination = list(self.getPlug("destination").value)
        [os.rename(src, destination[i]) for i, src in enumerate(source)]

        output = self.getPlug("output")
        if output is not None:
            output.value = destination
        output.dirty = False
        return destination


def getNode():
    """General function that returns our node, used to get create our node via Ui etc
    :return: Node instance
    """
    return RenameNode
