"""
@author : David Sparrow
@Created on : Nov 1, 2015
@email : dsparrow27@gmail.com
@website : www.david-sparrow.com
"""
# var = {"nodeName": {"ports": {"port1":{"object": "",
#                                        "connections":["connection1"]}}}}

from PyQt4 import QtCore, QtGui


class SceneGraphModel(QtCore.QAbstractItemModel):
    """
    """

    def __init__(self, sceneGraph, parent=None):
        """
        :param root: QObject
        """
        super(self.__class__, self).__init__(parent)
        self.graph = sceneGraph

    def rowCount(self, parent):
        """
        :param parent: QModelIndex
        """
        return len(self.graph)

    def data(self):
        pass

    def setData(self):
        pass

    def columnCount(self, parent):
        """Returns the column count
        :param parent:
        """
        return 2

    def headerData(self, section, orientation, role):
        """
        :param section:
        :param orientation:
        :param role:
        """
        if role == QtCore.Qt.DisplayRole:
            if section == 0:
                return "SceneGraph"
            elif section == 1:
                return "output"

    def flags(self, index):
        """sets the flags for the model
        """
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def index(self, row, column, parent):
        """Should return the QModelIndex that corresponds to the given row, colum and parent node
        :param row: int, the row number to get
        :param column: int, the column number to get
        :param parent: QModelIndex, the parent index
        @return QModelIndex
        """

        return QtCore.QModelIndex()
