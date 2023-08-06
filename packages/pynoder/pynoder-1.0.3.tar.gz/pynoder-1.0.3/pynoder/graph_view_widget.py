# Copyright 2017 John Roper
#
# ##### BEGIN GPL LICENSE BLOCK ######
# This file is part of PyNoder.
#
# PyNoder is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyNoder is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyNoder.  If not, see <http://www.gnu.org/licenses/>.
# ##### END GPL LICENSE BLOCK #####
import sys
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import QObject, pyqtSignal

from .graph_view import GraphView


class GraphViewWidget(QtWidgets.QWidget):
    rigNameChanged = pyqtSignal()

    def __init__(self, parent=None):

        # constructors of base classes
        super(GraphViewWidget, self).__init__(parent)
        self.openedFile = None
        self.setObjectName('graphViewWidget')
        self.setAttribute(QtCore.Qt.WA_WindowPropagation, True)

    def setGraphView(self, graphView):
        self.graphView = graphView

        # Setup Layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.graphView)
        self.setLayout(layout)

        # Setup hotkeys for the following actions.
        deleteShortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Delete), self)
        deleteShortcut.activated.connect(self.graphView.deleteSelectedNodes)

        frameShortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F), self)
        frameShortcut.activated.connect(self.graphView.frameSelectedNodes)

        frameShortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_A), self)
        frameShortcut.activated.connect(self.graphView.frameAllNodes)

    def getGraphView(self):
        return self.graphView

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    widget = GraphViewWidget()
    graph = GraphView(parent=widget)

    from node import Node
    from port import InputPort, OutputPort, IOPort

    node1 = Node(graph, 'Short')
    node1.addPort(InputPort(node1, graph, 'InPort1', QtGui.QColor(128, 170, 170, 255), 'MyDataX'))
    node1.addPort(InputPort(node1, graph, 'InPort2', QtGui.QColor(128, 170, 170, 255), 'MyDataX'))
    node1.addPort(OutputPort(node1, graph, 'OutPort', QtGui.QColor(32, 255, 32, 255), 'MyDataY'))
    node1.addPort(IOPort(node1, graph, 'IOPort1', QtGui.QColor(32, 255, 32, 255), 'MyDataY'))
    node1.addPort(IOPort(node1, graph, 'IOPort2', QtGui.QColor(32, 255, 32, 255), 'MyDataY'))
    node1.setNodePos(QtCore.QPointF(-100, 0))

    graph.addNode(node1)

    node2 = Node(graph, 'ReallyLongLabel')
    node2.addPort(InputPort(node2, graph, 'InPort1', QtGui.QColor(128, 170, 170, 255), 'MyDataX'))
    node2.addPort(InputPort(node2, graph, 'InPort2', QtGui.QColor(128, 170, 170, 255), 'MyDataX'))
    node2.addPort(OutputPort(node2, graph, 'OutPort', QtGui.QColor(32, 255, 32, 255), 'MyDataY'))
    node2.addPort(IOPort(node2, graph, 'IOPort1', QtGui.QColor(32, 255, 32, 255), 'MyDataY'))
    node2.addPort(IOPort(node2, graph, 'IOPort2', QtGui.QColor(32, 255, 32, 255), 'MyDataY'))
    node2.setNodePos(QtCore.QPointF(100, 0))

    graph.addNode(node2)

    widget.setGraphView(graph)
    widget.show()

    sys.exit(app.exec_())
