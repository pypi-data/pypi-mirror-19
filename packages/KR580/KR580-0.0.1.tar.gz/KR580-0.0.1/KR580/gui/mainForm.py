from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QStyledItemDelegate, QHeaderView

from .base_form import Ui_MainWindow

class MemoryCellDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        #self.Siz

    def displayText(self, value, locale):
        return '%02X' % value

class MainForm(Ui_MainWindow):
    compileSignal = pyqtSignal(str, Ui_MainWindow)
    executeSignal = pyqtSignal()

    def setupUi(self, w):
        super().setupUi(w)
        self.actionCompile.triggered.connect(self.compile)
        self.actionExecute.triggered.connect(self.execute_)
        self.tableView.setItemDelegate(MemoryCellDelegate())
        self.tableView.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        #QHeaderView.rest
        #self.tableView.verticalHeader

    def compile(self):
        self.compileSignal.emit(self.codeEditor.toPlainText(), self)

    def execute_(self):
        self.executeSignal.emit()

    def bind_memory(self, memory):
        self.tableView.setModel(memory)

    def redraw_memory(self):
        self.tableView.reset()
