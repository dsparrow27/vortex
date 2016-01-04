import re
from ds.vortex.core import baseNode
from ds.vortex.core import plug as plugs


class SubStringNode(baseNode.BaseNode):
    """Returns a list of strings that have the search string in it.
    """
    def __init__(self, name):
        """
        :param name: str, the name of the node
        """
        baseNode.BaseNode.__init__(self, name)

    def initialize(self):
        baseNode.BaseNode.initialize(self)
        self.addPlug(plugs.OutputPlug("output", self), clean=True)
        self.addPlug(plugs.InputPlug("value", self), [], clean=True)
        self.addPlug(plugs.InputPlug("searchValue", self), "", clean=True)
        self.addPlug(plugs.InputPlug("replaceValue", self), "", clean=True)

    def compute(self):
        baseNode.BaseNode.compute(self)
        searchValue = self.getPlug("searchValue").value
        replaceValue = self.getPlug("replaceValue").value
        print searchValue, replaceValue, self.getPlug("value").value
        result = [re.sub(searchValue, replaceValue, char) for char in self.getPlug("value").value]

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
    return SubStringNode
