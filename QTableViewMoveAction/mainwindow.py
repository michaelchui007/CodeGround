from PySide6.QtWidgets import QMainWindow, QTableView, QAbstractItemView
from PySide6.QtCore import Qt

from QTableViewMoveAction.ui_mainwindow import Ui_MainWindow
from mytablemodel import MyTableModel
from mystandarditemmodel import MyStandardItemModel

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.model = None
        
        self.initMyTableModel()
        self.initMyStandardItemModel()

    
    # def initMyTableModel(self):
    #     view = self.ui.tableViewA
    #     model = MyTableModel()
    #     view.setModel(model)
    #
    #     view.setSelectionMode(QAbstractItemView.SingleSelection)
    #     view.setDragEnabled(True)
    #     view.setDefaultDropAction(Qt.DropAction.MoveAction)
    #     view.setDragDropMode(QAbstractItemView.InternalMove)
    #
    def initMyTableModel(self):
        self.model = MyStandardItemModel(self)
        view = self.ui.tableViewB
        view.setModel(self.model)

        view.setSelectionMode(QAbstractItemView.SingleSelection)
        view.setDragEnabled(True)
        view.setDefaultDropAction(Qt.DropAction.MoveAction)
        view.setDragDropMode(QAbstractItemView.InternalMove)
    
    def initMyStandardItemModel(self):

        row_count = 10
        col_count = 6
        
        # 设置列标题
        self.model.setColumnCount(col_count)
        for col in range(col_count):
            self.model.setHeaderData(col, Qt.Horizontal, str(col))
        
        # 设置行标题
        self.model.setRowCount(row_count)
        for row in range(row_count):
            self.model.setHeaderData(row, Qt.Vertical, str(row))
        
        # 设置数据
        for row in range(row_count):
            for col in range(col_count):
                from PySide6.QtGui import QStandardItem
                item = QStandardItem(f"{row} {col}")
                self.model.setItem(row, col, item)

