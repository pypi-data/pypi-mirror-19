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


class Connection(QtWidgets.QGraphicsPathItem):
    __defaultPen = QtGui.QPen(QtGui.QColor("#A7A7A7"), 1.5)

    def __init__(self, graph, srcPortCircle, dstPortCircle):
        super(Connection, self).__init__()

        self.__graph = graph
        self.__srcPortCircle = srcPortCircle
        self.__dstPortCircle = dstPortCircle
        penStyle = QtCore.Qt.DashLine

        self.__connectionColor = QtGui.QColor(0, 0, 0)
        self.__connectionColor.setRgbF(*self.__srcPortCircle.getColor().getRgbF())
        self.__connectionColor.setAlpha(125)

        self.__defaultPen = QtGui.QPen(QtGui.QColor("#A7A7A7"), 1.5)

        self.__connectionHoverColor = QtGui.QColor(0, 0, 0)
        self.__connectionHoverColor.setRgbF(*self.__srcPortCircle.getColor().getRgbF())
        self.__connectionHoverColor.setAlpha(255)

        self.__hoverPen = QtGui.QPen(self.__connectionHoverColor, 1.5)

        self.setPen(self.__defaultPen)
        self.setZValue(-1)

        self.setAcceptHoverEvents(True)
        self.connect()

    def setPenStyle(self, penStyle):
        self.__defaultPen.setStyle(penStyle)
        self.__hoverPen.setStyle(penStyle)
        self.setPen(self.__defaultPen)  # Force a redraw

    def setPenWidth(self, width):
        self.__defaultPen.setWidthF(width)
        self.__hoverPen.setWidthF(width)
        self.setPen(self.__defaultPen)  # Force a redraw

    def getSrcPortCircle(self):
        return self.__srcPortCircle

    def getDstPortCircle(self):
        return self.__dstPortCircle

    def getSrcPort(self):
        return self.__srcPortCircle.getPort()

    def getDstPort(self):
        return self.__dstPortCircle.getPort()

    def boundingRect(self):
        srcPoint = self.mapFromScene(self.__srcPortCircle.centerInSceneCoords())
        dstPoint = self.mapFromScene(self.__dstPortCircle.centerInSceneCoords())
        penWidth = self.__defaultPen.width()

        return QtCore.QRectF(
            min(srcPoint.x(), dstPoint.x()),
            min(srcPoint.y(), dstPoint.y()),
            abs(dstPoint.x() - srcPoint.x()),
            abs(dstPoint.y() - srcPoint.y()),
            ).adjusted(-penWidth/2, -penWidth/2, +penWidth/2, +penWidth/2)

    def paint(self, painter, option, widget):
        srcPoint = self.mapFromScene(self.__srcPortCircle.centerInSceneCoords())
        dstPoint = self.mapFromScene(self.__dstPortCircle.centerInSceneCoords())

        dist_between = dstPoint - srcPoint

        self.__path = QtGui.QPainterPath()
        self.__path.moveTo(srcPoint)
        self.__path.cubicTo(
            srcPoint + QtCore.QPointF(0, 0),
            dstPoint - QtCore.QPointF(0, 0),
            dstPoint
            )
        self.setPath(self.__path)
        super(Connection, self).paint(painter, option, widget)

    def hoverEnterEvent(self, event):
        self.setPen(self.__hoverPen)
        super(Connection, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setPen(self.__defaultPen)
        super(Connection, self).hoverLeaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.__dragging = True
            self._lastDragPoint = self.mapToScene(event.pos())
            event.accept()
        else:
            super(Connection, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.__dragging:
            pos = self.mapToScene(event.pos())
            delta = pos - self._lastDragPoint
            if delta.x() != 0:

                self.__graph.removeConnection(self)

                from . import mouse_actions
                if delta.x() < 0:
                    mouse_actions.MouseGrabber(self.__graph, pos, self.__srcPortCircle, 'In')
                else:
                    mouse_actions.MouseGrabber(self.__graph, pos, self.__dstPortCircle, 'Out')

        else:
            super(Connection, self).mouseMoveEvent(event)

    def disconnect(self):
        self.__srcPortCircle.removeConnection(self)
        self.__dstPortCircle.removeConnection(self)

    def connect(self):
        self.__srcPortCircle.addConnection(self)
        self.__dstPortCircle.addConnection(self)
