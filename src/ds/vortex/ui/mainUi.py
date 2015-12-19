from ds.qt.qtAuto import QtGui, QtCore
from ds.qt.widgets import mainWindow
from ds.qt.widgets import graphicView
from ds.qt.widgets import graphicsScene
from ds.qt.extendedWidgets import treeViewPlus
import model
from ds.vortex.core import graph
from ds.vortex.nodes.math import add

class MainUi(mainWindow.MainWindow):
    """
    """

    def __init__(self, title="Vortex", width=900, height=700,
                 parent=None, createMenuBar=True,
                 loadStyleSheet=True, showOnInitalize=True):
        super(MainUi, self).__init__(title, width, height, parent, createMenuBar, loadStyleSheet, showOnInitalize)
        widget = QtGui.QWidget()
        self.setCentralWidget(widget)
        self.mainLayout = QtGui.QVBoxLayout(widget)
        self.view = graphicView.GraphicsView(self)
        self.scene = graphicsScene.GraphicsScene()
        self.scene.setObjectName("nodeDropGraphScene")
        self.scene.setSceneRect(0, 0, 800, 546)
        self.view.setScene(self.scene)
        self.mainLayout.addWidget(self.view)
        self.dock = QtGui.QDockWidget(self)
        self.dock.setObjectName("outliner")
        self.outliner = Outliner(self)
        self.dock.setWidget(self.outliner)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dock)
        #temp
        QtCore.QObject.connect(QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape), self), QtCore.SIGNAL('activated()'), self.close)

class Outliner(mainWindow.MainWindow):
    """
    """

    def __init__(self, parent=None):
        super(Outliner, self).__init__(parent=parent)
        self.centralWidget = QtGui.QWidget()
        self.centralWidget.setObjectName("central widget")
        self.setCentralWidget(self.centralWidget)
        mainlayout = QtGui.QVBoxLayout(self.centralWidget)
        self.treeViewPlus = treeViewPlus.TreeViewPlus(parent=self.centralWidget)
        mainlayout.addWidget(self.treeViewPlus)
        self.dataSource = graph.Graph(name="testGraph")
        self.dataSource.addNode(add.AddNode("test"))
        self.dataSource.addNode(add.AddNode("test1"))
        self.dataSource.getNode("test").getPlug("output").connect(self.dataSource.getNode("test").getPlug("input1"))
        self.dataSource.getNode("test1").getPlug("input1").connect(self.dataSource.getNode("test").getPlug("output"))
        self.model = model.SceneGraphModel(self.dataSource)
        self.treeViewPlus.setSourceModel(self.model)

if __name__ == "__main__":
    import sys
    from ds.vortex.nodes.math import add
    app = QtGui.QApplication(sys.argv)
    win = MainUi()
    # source = win.outliner.dataSource

    win.show()
    sys.exit(app.exec_())
