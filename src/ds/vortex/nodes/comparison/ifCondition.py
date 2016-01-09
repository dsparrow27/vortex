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
        self.outputPlug_ = self.addPlug(self.outputPlug_, clean=True)
        self.conditionPlug_ = plugs.InputPlug("condition", self, value=True)
        self.ifTruePlug_ = plugs.InputPlug("ifTrue", self, value=0)
        self.ifFalsePlug = plugs.InputPlug("ifFalse", self, value=0)

        self.addPlug(self.conditionPlug_, clean=True)
        self.addPlug(self.ifTruePlug_, clean=True)
        self.addPlug(self.ifFalsePlug, clean=True)

        self.plugAffects(self.conditionPlug_, self.outputPlug_)
        self.plugAffects(self.ifTruePlug_, self.outputPlug_)
        self.plugAffects(self.ifFalsePlug, self.outputPlug_)

    def compute(self, requestPlug):
        baseNode.BaseNode.compute(self, requestPlug=requestPlug)
        if self.conditionPlug_.value:
            result = self.ifTruePlug_.value
        else:
            result = self.ifFalsePlug.value

        requestPlug.value = result
        requestPlug.dirty = False
        return result


def getNode():
    """General function that returns our node, used to get create our node via Ui etc
    :return: Node instance
    """
    return IfNode
