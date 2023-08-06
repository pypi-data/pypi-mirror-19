from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant, pyqtSignal

class MemoryModel(QAbstractTableModel):
    dataChanged = pyqtSignal()

    def __init__(self, data):
        super().__init__()
        self.row_width = 16
        self.arraydata = data
        self.column_indices = ['%0X' % i for i in range(self.columnCount())]
        self.row_indices = ['%03X' % i for i in range(self.rowCount())]

    def rowCount(self, parent=None):
        return len(self.arraydata) // self.row_width

    def columnCount(self, parent=None):
        return self.row_width

    def data(self, index, role):
        if not index.isValid() or role != Qt.DisplayRole:
            return QVariant()
        actual_index = index.row()*self.row_width + index.column()
        return QVariant(self.arraydata[actual_index])

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.column_indices[section]
            elif orientation == Qt.Vertical:
                return self.row_indices[section]
        else:
            return QVariant()
