import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication, QMainWindow
from board import Board

class MonopolyGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Monopoly QT")
        self.setGeometry(100, 100, 800, 800)

        self.board = Board()
        self.setCentralWidget(self.board)

if __name__ == "__main__":
    app = QApplication([])
    game = MonopolyGame()
    game.show()
    app.exec()
