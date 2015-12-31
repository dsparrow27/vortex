from ds.vortex.core import baseNode
from ds.vortex.core import plug as plugs


class IfNode(baseNode.BaseNode):
    def __init__(self, name):
        """
        :param name: str, the name of the node
        """
        baseNode.BaseNode.__init__(self, name)

    def initialize(self):
        baseNode.BaseNode.initialize(self)
        self.addPlug(plugs.InputPlug("condition", self), True, clean=True)
        self.addPlug(plugs.InputPlug("ifTrue", self), 0, clean=True)
        self.addPlug(plugs.InputPlug("ifFalse", self), 0, clean=True)
        self.addPlug(plugs.OutputPlug("output", self), clean=True)

    def compute(self):
        baseNode.BaseNode.compute(self)
        if self.getPlug("condition").value:
            result = self.getPlug("ifTrue").value
        else:
            result = self.getPlug("ifFalse").value
        output = self.getPlug("output")
        if output is not None:
            output.value = result
        output.dirty = False
        return result


def getNode():
    """General function that returns our node, used to get create our node via Ui etc
    :return: Node instance
    """
    return IfNode
