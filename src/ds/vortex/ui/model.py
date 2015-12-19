"""
@author : David Sparrow
@Created on : Nov 1, 2015
@email : dsparrow27@gmail.com
@website : www.david-sparrow.com
"""

from PyQt4 import QtCore, QtGui


class SceneGraphModel(QtCore.QAbstractItemModel):
    def __init__(self, graph, parent=None):
        """
        :param root: QObject
        """
        super(SceneGraphModel, self).__init__(parent)
        self.graph = graph

    def rowCount(self, parent):
        """
        :param parent: QModelIndex
        """
        if not parent.isValid():
            return len(self.graph)
        parentItem = parent.internalPointer()
        if hasattr(parentItem, "_plugs"):
            return len(parentItem.plugs)
        return 0

    def columnCount(self, parent):
        """Returns the column count
        :param parent:
        """
        return 2

    def data(self, index, role):
        """
        :param index:
        :param role:
        """
        if not index.isValid():
            return None

        item = index.internalPointer()
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            if index.column() == 0:
                return item.name
            elif index.column() == 1 and hasattr(item, "_connections"):
                return str([i.fullPath() for i in item.connections])

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if not index.isValid():
            return False

        if role == QtCore.Qt.EditRole:
            item = index.internalPointer()
            item.name = value.toString()
            return True

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
                return "Connections"

    def flags(self, index):
        """sets the flags for the model eg. editable , if the index is 0 then not editable
        """
        if index.column() == 0:
            return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        else:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def parent(self, index):
        """Returns the parent of the node with the given index
        :param index: QModelIndex
        @return: QModelIndex
        """
        return QtCore.QModelIndex()

    def index(self, row, column, parent):
        """Should return the QModelIndex that corresponds to the given row, colum and parent node
        :param row: int, the row number to get
        :param column: int, the column number to get
        :param parent: QModelIndex, the parent index
        @return QModelIndex
        """

        if not parent.isValid():
            parentNode = self.graph
            child = parentNode.nodes.values()[row]
        else:
            parentNode = parent.internalPointer()
            child = parentNode.plugs.values()[row]
        return self.createIndex(row, column, child)
