import re
from ds.vortex.core import baseNode
from ds.vortex.core import plug as plugs


class SearchStringNode(baseNode.BaseNode):
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

    def compute(self):
        baseNode.BaseNode.compute(self)
        result = [char for char in [self.getPlug("value").value] if re.search(self.getPlug("searchValue"), char)]

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
    return SearchStringNode
