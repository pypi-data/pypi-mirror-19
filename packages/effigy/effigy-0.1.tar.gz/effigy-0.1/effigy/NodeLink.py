from PyQt5.QtWidgets import QGraphicsItem

from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsPathItem
from PyQt5.QtCore import QRectF, QPointF
from PyQt5.QtGui import QBrush, QColor, QPainterPath, QPen

from enum import Enum

class NodeIODirection(Enum):
    """Establish if IO direction is input, output or any"""
    any = 0
    output = 1
    input = 2

class NodeIOMultiplicity(Enum):
    """Whether the node can be connected to multiple other nodes, or just one"""
    single = 0
    multiple = 1

class InvalidLinkException(Exception):
    pass

class NodeLink(QGraphicsPathItem):
    def __init__(self, linktype, startIO=None, endIO=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.linktype = linktype

        self.valid = False

        self.startIO = startIO
        self.endIO = endIO

        if startIO == endIO:
            raise InvalidLinkException("startIO (ID: %s) and endIO (ID: %s) can not be the same!" % (startIO.id, endIO.id))

        if startIO is not None and endIO is not None:
            if issubclass(startIO.iotype, endIO.iotype):
                if type(self.startIO).classMultiplicity == NodeIOMultiplicity.single:
                    for link in self.startIO.nodeLinks:
                        self.startIO.removeLink(link)
                self.startIO.nodeLinks.append(self)

                if type(self.endIO).classMultiplicity == NodeIOMultiplicity.single:
                    for link in self.endIO.nodeLinks:
                        self.endIO.removeLink(link)
                self.endIO.nodeLinks.append(self)

                self.valid = True


    def updateBezier(self, overrideStartpos=QPointF(0, 0), overrideEndpos=QPointF(0, 0)):
        path = QPainterPath()

        if self.startIO is not None:
            startpos = self.startIO.scenePos()
        else:
            startpos = overrideStartpos

        if self.endIO is not None:
            endpos = self.endIO.scenePos()
        else:
            endpos = overrideEndpos

        path.moveTo(startpos)

        controlpoint = QPointF(abs((endpos - startpos).x()) * 0.8, 0)
        path.cubicTo(startpos + controlpoint,
                     endpos - controlpoint,
                     endpos)

        self.setPath(path)
