from ds.vortex.core import baseNode
from ds.vortex.core import plug as plugs


class BoolNode(baseNode.BaseNode):
    def __init__(self, name):
        """
        :param name: str, the name of the node
        """
        baseNode.BaseNode.__init__(self, name)

    def initialize(self):
        baseNode.BaseNode.initialize(self)
        self.addPlug(plugs.OutputPlug("output", self), clean=True)
        self.addPlug(plugs.InputPlug("value", self), True, clean=True)

    def compute(self):
        baseNode.BaseNode.compute(self)
        result = bool(self.getPlug("value").value)
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
    return BoolNode

