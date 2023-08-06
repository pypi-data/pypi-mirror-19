from PyQt5.QtWidgets import QGraphicsItem

from effigy.NodeIO import NodeIO

class QNodeSceneNode(QGraphicsItem):
    """Graphical representation of Node"""

    # Here we define some information about the node
    author = "DrLuke"       # Author of this node (only used for namespacing, never visible to users)
    name = "Basenode"       # Human-readable name

    placeable = False       # Whether or not this node should be placeable from within the editor
    Category = ["Builtin"]     # Nested categories this Node should be sorted in

    # Description, similar to python docstrings (Brief summary on first line followed by a long description)
    description = """This node is the base class for all nodes.
It should never be placeable in the editor. However if you DO see this in the editor, something went wrong!"""

    def __init__(self, deserializedata=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.IO = []
        """Stores all IO for this Node."""

        self.setFlag(QGraphicsItem.ItemIsMovable)   # Item can be dragged with left-click

        if deserializedata is not None:
            self.deserialize(deserializedata)
        else:
            self.addGraphicsItems()
            self.addIO()

    def deserialize(self, data):
        """Gets data that has been serialized with 'serialize', reconstructs the object state from that data"""
        raise NotImplementedError("This method must be implemented in derived class")

    def addIO(self):
        """Add IOs to Node"""
        raise NotImplementedError("This method must be implemented in derived class")

    def addGraphicsItems(self):
        """Add Graphic Items for rendering the node"""
        raise NotImplementedError("This method must be implemented in derived class")

    def boundingRect(self):
        """Define appropriate bounding rect for Node body (necessary for interaction like dragging!)"""
        raise NotImplementedError("This method must be implemented in derived class")

    def paint(self, *__args):
        pass

    def mouseMoveEvent(self, QGraphicsSceneMouseEvent):
        for IO in self.IO:
            for link in IO.nodeLinks:
                link.updateBezier()

        super().mouseMoveEvent(QGraphicsSceneMouseEvent)


