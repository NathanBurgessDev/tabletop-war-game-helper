import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsRectItem
from PyQt5.QtCore import Qt

class CircleItem(QGraphicsEllipseItem):
    def __init__(self, id, x, y, diameter):
        super().__init__(x, y, diameter, diameter)
        self.id = id
        self.setAcceptHoverEvents(True)
        self.setBrush(Qt.red)

    def hoverEnterEvent(self, event):
        self.setBrush(Qt.yellow)

    def hoverLeaveEvent(self, event):
        self.setBrush(Qt.red)

    def mousePressEvent(self, event):
        print("Clicked on circle:", self.id)


class GameBoard(QGraphicsRectItem):
    def __init__(self, boardScale, circles, scene):
        super().__init__(0, -150, 220 * boardScale, 150 * boardScale) 
        self.x = 220 * boardScale
        self.y = 150 * boardScale
    #     self.addItem(circles,scene)
        
    # def addItem(self, circles,scene):
    #     for circle in circles:
    #         circleItem = CircleItem(circle["id"], circle["x"], circle["y"], circle["diameter"])
    #         scene.addItem(circleItem)
        

# The board we are using is 22 inches width and 15 inches height
class MainWindow(QMainWindow):
    def __init__(self, circles):
        super().__init__()
        
        self.setStyleSheet("background-color: white;")
        scene = QGraphicsScene(self)
        
        board = GameBoard(4,circles, scene)
        scene.addItem(board)
    
        
        view = QGraphicsView(scene)
        self.setCentralWidget(view)
        
        
        self.setWindowTitle("Clickable Circles")


if __name__ == "__main__":
    circles = [
        {"id": "Circle1", "x": 50, "y": -150 * 4, "diameter": 50},
        {"id": "Circle2", "x": 150, "y": -150 * 4, "diameter": 70},
        {"id": "Circle3", "x": 250, "y": -150 * 3, "diameter": 90}
    ]

    app = QApplication(sys.argv)
    window = MainWindow(circles)
    window.setGeometry(0, 0, 220 * 6, 150 * 6)
    window.show()
    sys.exit(app.exec_())
