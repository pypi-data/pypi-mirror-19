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
from PyQt5 import QtGui, QtWidgets, QtCore


class SelectionRect(QtWidgets.QGraphicsWidget):
    __backgroundColor = QtGui.QColor(100, 100, 100, 50)
    __pen = QtGui.QPen(QtGui.QColor(25, 25, 25), 1.0, QtCore.Qt.DashLine)

    def __init__(self, graph, mouseDownPos):
        super(SelectionRect, self).__init__()
        self.setZValue(-1)

        self.__graph = graph
        self.__graph.scene().addItem(self)
        self.__mouseDownPos = mouseDownPos
        self.setPos(self.__mouseDownPos)
        self.resize(0, 0)

    def setDragPoint(self, dragPoint):
        topLeft = QtCore.QPointF(self.__mouseDownPos)
        bottomRight = QtCore.QPointF(dragPoint)
        if dragPoint.x() < self.__mouseDownPos.x():
            topLeft.setX(dragPoint.x())
            bottomRight.setX(self.__mouseDownPos.x())
        if dragPoint.y() < self.__mouseDownPos.y():
            topLeft.setY(dragPoint.y())
            bottomRight.setY(self.__mouseDownPos.y())
        self.setPos(topLeft)
        self.resize(bottomRight.x() - topLeft.x(), bottomRight.y() - topLeft.y())

    def paint(self, painter, option, widget):
        rect = self.windowFrameRect()
        painter.setBrush(self.__backgroundColor)
        painter.setPen(self.__pen)
        painter.drawRect(rect)

    def destroy(self):
        self.__graph.scene().removeItem(self)
