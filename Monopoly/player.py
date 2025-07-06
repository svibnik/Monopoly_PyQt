from PySide6.QtWidgets import QGraphicsEllipseItem
from PySide6.QtGui import QColor

class Player:
    def __init__(self, name, color):
        self.name = name
        self.money = 1500
        self.token = QGraphicsEllipseItem(0, 0, 30, 30)
        self.token.setBrush(QColor(color))
