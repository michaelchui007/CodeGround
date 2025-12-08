from PySide6.QtCore import Qt, QMimeData, QByteArray
from PySide6.QtGui import QStandardItemModel, QStandardItem

class MyStandardItemModel(QStandardItemModel):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def flags(self, index):
        if index.isValid():
            return Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled | super().flags(index)
        return super().flags(index)
    
    def supportedDropActions(self):
        return Qt.DropAction.MoveAction | super().supportedDropActions()
    
    def mimeData(self, indexes):
        """
        重写方法
        Args:
            indexes: 点击元素

        Returns:

        """
        data = super().mimeData(indexes)
        if data:
            # parent mimeData中已判断indexes有效性，无效的会返回None
            # 也可以把信息放到model的mutable成员中
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
        old_item = self.takeItem(old_index.row(), old_index.column())
        current_item = self.takeItem(current_index.row(), current_index.column())
        
        # 交换两个item
        self.setItem(old_index.row(), old_index.column(), current_item)
        self.setItem(current_index.row(), current_index.column(), old_item)
        return True
