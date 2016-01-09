import os
from ds.vortex.core import baseNode
from ds.vortex.core import plug as plugs


class SubDirectoriesNode(baseNode.BaseNode):
    def __init__(self, name):
        """
        :param name: str, the name of the node
        """
        baseNode.BaseNode.__init__(self, name)

    def initialize(self):
        baseNode.BaseNode.initialize(self)
        self.outputPlug_ = plugs.OutputPlug("output", self)
        self.directoriesPlug_ = plugs.InputPlug("directories", self, [])
        self.recursivePlug_ = plugs.InputPlug("recursive", self, True)

        self.addPlug(self.outputPlug_, clean=True)
        self.addPlug(self.directoriesPlug_, clean=True)
        self.addPlug(self.recursivePlug_, clean=True)

        self.plugAffects(self.directoriesPlug_, self.outputPlug_)
        self.plugAffects(self.recursivePlug_, self.outputPlug_)

    def compute(self, requestPlug):
        baseNode.BaseNode.compute(self, requestPlug=requestPlug)
        if requestPlug != self.outputPlug_:
            return None
        result = []
        if self.recursivePlug_.value:
            for directory in self.directoriesPlug_.value:
                if not os.path.isdir(directory):
                    continue
                result.extend([d[0] for d in os.walk(os.path.normpath(directory))])
        else:
            for directory in self.directoriesPlug_.value:
                if not os.path.isdir(directory):
                    continue
                result.extend([d for d in os.listdir(directory) if os.path.isdir(d)])
        requestPlug.value = result
        requestPlug.dirty = False
        return result


def getNode():
    """General function that returns our node, used to get create our node via Ui etc
    :return: Node instance
    """
    return SubDirectoriesNode
