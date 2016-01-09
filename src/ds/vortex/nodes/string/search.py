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
        self.outputPlug_ = plugs.OutputPlug("output", self)
        self.valuePlug_ = plugs.InputPlug("value", self, value=[])
        self.searchPlug_ = plugs.InputPlug("searchValue", self, value="")

        self.addPlug(self.outputPlug_, clean=True)
        self.addPlug(self.valuePlug_, clean=True)
        self.addPlug(self.searchPlug_, clean=True)

        self.plugAffects(self.valuePlug_, self.outputPlug_)
        self.plugAffects(self.searchPlug_, self.outputPlug_)

    def compute(self, requestPlug):
        baseNode.BaseNode.compute(self, requestPlug=requestPlug)
        if requestPlug != self.outputPlug_:
            return None
        result = [char for char in [self.valuePlug_.value] if re.search(self.searchPlug_.value, char)]

        requestPlug.value = result
        requestPlug.dirty = False
        return result


def getNode():
    """General function that returns our node, used to get create our node via Ui etc
    :return: Node instance
    """
    return SearchStringNode
