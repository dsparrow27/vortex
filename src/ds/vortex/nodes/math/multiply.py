from ds.vortex.core import baseNode
from ds.vortex.core import plug as plugs


class MultiplyNode(baseNode.BaseNode):
    """Add math node, sums the values from the input port and outputs the total sum.
    default input port names : input1, input2 (input1 + input2)
    default output port name: output.
    """

    def __init__(self, name):
        """
        :param name: str, the name of the node
        """
        baseNode.BaseNode.__init__(self, name)

    def initialize(self):
        baseNode.BaseNode.initialize(self)
        self.addPlug(plugs.OutputPlug("output", self), clean=True)
        self.addPlug(plugs.InputPlug("input1", self), 0, clean=True)
        self.addPlug(plugs.InputPlug("input2", self), 0, clean=True)

    def compute(self):
        baseNode.BaseNode.compute(self)
        result = self.getPlug("input1").value * self.getPlug("input2").value
        output = self.getPlug("output")
        if output is not None:
            output.value = result
        output.dirty = False
        return result


def getNode():
    """General function that returns our node, used to get create our node via Ui etc
    :return: Node instance
    """
    return MultiplyNode
