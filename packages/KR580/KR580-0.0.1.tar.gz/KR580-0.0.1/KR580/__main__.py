import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QStyledItemDelegate
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QModelIndex

from .compiler.compiler import compile_
from .gui.mainForm import MainForm
from .emulator import cpu

from .memory_model import MemoryModel
mem = MemoryModel(cpu.memory)

@pyqtSlot(str)
def compile_src(s):
    compiled = compile_(s)
    print(compiled)
    cpu.write_memory(0, compiled)
    mem.dataChanged.emit()

@pyqtSlot()
def execute():
    cpu.execute()
    mem.dataChanged.emit()

def main():
    import os
    print(os.path.abspath(__file__))
    app = QApplication([])
    w = QMainWindow()
    form = MainForm()
    form.setupUi(w)
    form.bind_memory(mem)
    form.compileSignal.connect(compile_src)
    form.executeSignal.connect(execute)
    mem.dataChanged.connect(form.redraw_memory)

    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main(sys.argv)
