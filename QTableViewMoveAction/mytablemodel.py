from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt, QMimeData, QByteArray
from PySide6.QtWidgets import QTableView

class MyTableModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 初始化模拟数据
        self.modelData = []
        for row in range(10):
            row_data = []
            for col in range(6):
                row_data.append(f"{row} {col}")
            self.modelData.append(row_data)
    
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return str(section)
        return None
    
    def rowCount(self, parent=QModelIndex()):
        if parent.isValid():
            return 0
        return len(self.modelData)
    
    def columnCount(self, parent=QModelIndex()):
        if parent.isValid():
            return 0
        return 6 if self.modelData else 0
    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        
        if role == Qt.DisplayRole:
            return self.modelData[index.row()][index.column()]
        return None
    
    def flags(self, index):
        if index.isValid():
            return Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled | super().flags(index)
        return super().flags(index)
    
    def supportedDropActions(self):
        return Qt.DropAction.MoveAction | super().supportedDropActions()
    
    def mimeData(self, indexes):
        data = super().mimeData(indexes)
        if data:
            # parent mimeData中已判断indexes有效性，无效的会返回None
            # 也可以把信息放到model的mutable成员中
            data.setData("application/x-qabstractitemmodeldatalist", QByteArray())
            data.setData("row", QByteArray(str(indexes[0].row()).encode()))
            data.setData("col", QByteArray(str(indexes[0].column()).encode()))
        return data
    
    def dropMimeData(self, data, action, row, column, parent):
        if not data or action != Qt.DropAction.MoveAction:
            return False
        
        # 这里没有判断toint ok（数据转换有效性）
        old_row = int(data.data("row").data().decode())
        old_col = int(data.data("col").data().decode())
        old_index = self.index(old_row, old_col)
        current_index = parent
        
        # 可以先对index有效性进行判断，无效返回False，此处略过
        self.modelData[old_index.row()][old_index.column()], self.modelData[current_index.row()][current_index.column()] = \
            self.modelData[current_index.row()][current_index.column()], self.modelData[old_index.row()][old_index.column()]
        
        return True
