from PySide6.QtWidgets import (QMainWindow, QTableView, QHeaderView,
                               QVBoxLayout, QWidget, QStyledItemDelegate)
from PySide6.QtCore import Qt

class BomDelegate(QStyledItemDelegate):
    """可以在这里定制单元格样式"""
    pass

class BomManagerView(QMainWindow):
    def __init__(self, model):
        super().__init__()
        self.setWindowTitle("BOM Manager - MVD Structure")
        self.resize(1000, 600)

        self.table = QTableView()
        self.table.setModel(model)
        self.table.setItemDelegate(BomDelegate())

        # 表头配置
        header = self.table.horizontalHeader()
        header.setSectionsMovable(True)
        header.setSectionsClickable(True)
        self.table.setSortingEnabled(True)

        # 性能与视觉优化
        self.table.verticalHeader().setDefaultSectionSize(30)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table.setAlternatingRowColors(True) # 开启隔行变色便于阅读

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.table)
        self.setCentralWidget(central_widget)