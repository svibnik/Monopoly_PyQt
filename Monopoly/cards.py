from PySide6.QtWidgets import QMessageBox

class ChanceCard:
    @staticmethod
    def draw_card():
        QMessageBox.information(None, "Шанс", "Пройдите на Старт! Получите $200!")
