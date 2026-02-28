from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex

class BomRow:
    """定义行数据结构"""
    __slots__ = ('item', 'cpn', 'qty', 'rd_str', 'vendor', 'mpn', 'is_first_in_block')
    def __init__(self, item, cpn, qty, rd_str, vendor, mpn, is_first=True):
        self.item = item
        self.cpn = cpn
        self.qty = qty
        self.rd_str = rd_str
        self.vendor = vendor
        self.mpn = mpn
        self.is_first_in_block = is_first

class BomManagerModel(QAbstractTableModel):
    def __init__(self, data_list=None):
        super().__init__()
        self._column_configs = [
            {"title": "Item", "key": "item", "is_cpn_level": True},
            {"title": "CPN", "key": "cpn", "is_cpn_level": True},
            {"title": "Qty", "key": "qty", "is_cpn_level": True},
            {"title": "Manufacturer", "key": "vendor", "is_cpn_level": False},
            {"title": "MPN", "key": "mpn", "is_cpn_level": False},
            {"title": "References", "key": "rd_str", "is_cpn_level": True}
        ]
        self._visible_indices = list(range(len(self._column_configs)))
        self._data = data_list if data_list else []

    def rowCount(self, parent=QModelIndex()):
        return max(len(self._data), 15) # 即使没数据也显示15行空行

    def columnCount(self, parent=QModelIndex()):
        return len(self._visible_indices)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or index.row() >= len(self._data):
            return None

        row_obj = self._data[index.row()]
        col_conf = self._column_configs[self._visible_indices[index.column()]]

        if role == Qt.DisplayRole:
            # 块状显示逻辑：非首行则隐藏CPN级别字段
            if col_conf["is_cpn_level"] and not row_obj.is_first_in_block:
                return ""
            return str(getattr(row_obj, col_conf["key"]))
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._column_configs[self._visible_indices[section]]["title"]
        return None

    def sort(self, column, order):
        """双重排序逻辑：维持块结构"""
        if not self._data: return
        self.layoutAboutToBeChanged.emit()

        col_idx = self._visible_indices[column]
        key = self._column_configs[col_idx]["key"]
        reverse = (order == Qt.DescendingOrder)

        # 排序：目标列为主，CPN为辅
        self._data.sort(key=lambda x: (str(getattr(x, key)), x.cpn), reverse=reverse)

        # 重新计算块首标记
        for i, row in enumerate(self._data):
            row.is_first_in_block = True if i == 0 else (row.cpn != self._data[i-1].cpn)

        self.layoutChanged.emit()

    def update_columns(self, indices):
        self.beginResetModel()
        self._visible_indices = indices
        self.endResetModel()