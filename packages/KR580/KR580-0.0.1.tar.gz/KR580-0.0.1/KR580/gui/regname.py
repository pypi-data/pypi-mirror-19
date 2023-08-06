from PyQt5.QtWidgets import QLabel

class Regname(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedSize(30, 18)
        self.setStyleSheet('.Regname { min-height: 15; min-width: 30; border: 1px solid black; alignment: center; }')
