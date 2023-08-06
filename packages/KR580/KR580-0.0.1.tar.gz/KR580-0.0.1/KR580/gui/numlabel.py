from PyQt5.QtWidgets import QLabel

class Numlabel(QLabel):
    styleSheet = '.Numlabel\n {\n border-radius: 5px; \n }'

    def __init__ (self, parent):
        super().__init__(parent)
