import math
from ds.vortex.core import baseNode
from ds.vortex.core import plug as plugs


class PiNode(baseNode.BaseNode):
    def __init__(self, name):
        """
        :param name: str, the name of the node
        """
        baseNode.BaseNode.__init__(self, name)

    def initialize(self):
        baseNode.BaseNode.initialize(self)
        self.addPlug(plugs.OutputPlug("output", self), clean=True)

    def compute(self):
        baseNode.BaseNode.compute(self)
        result = math.pi
        if result is None:
            return
        output = self.getPlug("output")
        if output is not None:
            output.value = result
        output.dirty = False
        return result


def getNode():
    """General function that returns our node, used to get create our node via Ui etc
    :return: Node instance
    """
    return PiNode
