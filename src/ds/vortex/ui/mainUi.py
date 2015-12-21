from functools import partial
import os

from ds.qt.qtAuto import QtGui, QtCore
from ds.qt.widgets import mainWindow
from ds.qt.widgets import graphicView
from ds.qt.widgets import node as qnode
from ds.qt.widgets import graphicsScene
from ds.qt.extendedWidgets import treeViewPlus
from ds.vortex.core import graph
import model


class MainUi(mainWindow.MainWindow):
    """
    """

    def __init__(self, title="Vortex", width=900, height=700,
                 parent=None, createMenuBar=True,
                 loadStyleSheet=True, showOnInitalize=True):
        super(MainUi, self).__init__(title, width, height, parent, createMenuBar, loadStyleSheet, showOnInitalize)
        self.modulesDict = {}
        widget = QtGui.QWidget()
        self.setCentralWidget(widget)
        self.mainLayout = QtGui.QVBoxLayout(widget)
        self.view = graphicView.GraphicsView(self)
        self.scene = graphicsScene.GraphicsScene()
        self.scene.setObjectName("nodeDropGraphScene")
        self.scene.setSceneRect(0, 0, 500, 546)
        self.view.setScene(self.scene)
        self.mainLayout.addWidget(self.view)
        self.dockOutliner = QtGui.QDockWidget("Outliner", self)
        self.dockOutliner.setObjectName("Outliner")
        self.outliner = Outliner(self)
        self.dockOutliner.setWidget(self.outliner)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dockOutliner)

        # temp
        QtCore.QObject.connect(QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape), self),
                               QtCore.SIGNAL('activated()'), self.close)
        self.getNodeClasses("E:/tools/vortex\src\ds/vortex/nodes") # hard coded :(
        self.view.tabPressSignal.connect(self.showNodeList)
        # temp hardcode

    def showNodeList(self, mousePos):
        menu = QtGui.QMenu(self)
        for name, values in self.modulesDict.iteritems():
            action = QtGui.QAction(name, menu)
            menu.addAction(action)
            action.triggered.connect(partial(self.addNode, name))
        menu.exec_(mousePos)

    def addNode(self, name):
        node = self.modulesDict.get(name).get("object")(name)
        self.outliner.dataSource.addNode(node)
        winNode = qnode.QNode(name)
        for plugName, plug in node.plugs.iteritems():
            if plug.isInput():
                winNode.addInput(plug.name)
            elif plug.isOutput():
                winNode.addOutput(plug.name)
        self.view.addItem(winNode)
        self.outliner.reset()

    def getNodeClasses(self, path):
        """Crude function :P
        recusive function
        searches all directories within the components folder gets all available modules
        :param path : string,
        """
        # list all directories
        res = os.listdir(path)

        toReturn = []
        for r in res:
            cleanPath = os.path.normpath(os.path.join(path, r))
            ext = os.path.basename(cleanPath).split(".")[-1]
            baseName = os.path.basename(cleanPath).split(".")[0]
            if os.path.isdir(cleanPath):
                self.getNodeClasses(cleanPath)
            if ext == "py" and all(r != name for name in ["__init__.py", ".gitignore"]):
                toReturn.append(r)

                modulePath = cleanPath.replace("\\", ".").split("src.")[-1].replace("."+ext, "")
                if not modulePath:
                    self.logger.error("modulePath not correct : %s" % modulePath)
                    return False
                try:
                    module = __import__(modulePath, globals(), locals(), [baseName], -1)
                except ImportError, er:
                    self.logger.error("""importing {0} Failed! , have you typed the right name?,
                        check self.modulesDict for availablesModules.""".format(modulePath))
                    raise er

                self.modulesDict[baseName] = {
                    "object": module.getNode(),
                    "fileName": cleanPath,
                    "modulePath": modulePath}


class Outliner(QtGui.QWidget):
    """
    """

    def __init__(self, name="", parent=None):
        super(Outliner, self).__init__(parent)

        self.setObjectName("central widget")
        mainlayout = QtGui.QVBoxLayout(self)
        self.treeViewPlus = treeViewPlus.TreeViewPlus(parent=self)
        mainlayout.addWidget(self.treeViewPlus)
        self.dataSource = graph.Graph(name="testGraph")
        self.model = model.SceneGraphModel(self.dataSource)
        self.treeViewPlus.setSourceModel(self.model)

    def reset(self):
        self.model.modelReset.emit()



if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    win = MainUi()
    win.show()
    sys.exit(app.exec_())
