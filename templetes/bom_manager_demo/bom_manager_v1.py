import sys
import random
import time
from PySide6.QtWidgets import (QApplication, QMainWindow, QTableView,
                               QHeaderView, QVBoxLayout, QHBoxLayout,
                               QWidget, QPushButton, QCheckBox, QLabel)
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, QSize
from PySide6.QtGui import QColor

# ---------------------------------------------------------
# 1. 数据模型类：使用 __slots__ 节省内存，适合几十万条数据
# ---------------------------------------------------------
class BomRow:
    __slots__ = ('item', 'cpn', 'qty', 'rd_str', 'vendor', 'mpn', 'is_first_in_block')

    def __init__(self, item, cpn, qty, rd_str, vendor, mpn, is_first_in_block):
        self.item = item
        self.cpn = cpn
        self.qty = qty
        self.rd_str = rd_str
        self.vendor = vendor
        self.mpn = mpn
        self.is_first_in_block = is_first_in_block

# ---------------------------------------------------------
# 2. 高性能 QAbstractTableModel
# ---------------------------------------------------------
class BomManagerModel(QAbstractTableModel):
    def __init__(self, data_list=None):
        super().__init__()
        # 所有定义的列
        self._column_configs = [
            {"title": "Item", "key": "item", "is_cpn_level": True},
            {"title": "Part Number (CPN)", "key": "cpn", "is_cpn_level": True},
            {"title": "Quantity", "key": "qty", "is_cpn_level": True},
            {"title": "Manufacturer", "key": "vendor", "is_cpn_level": False},
            {"title": "MPN", "key": "mpn", "is_cpn_level": False},
            {"title": "Reference Designator", "key": "rd_str", "is_cpn_level": True}
        ]

        # 当前可见列的索引列表
        self._visible_indices = list(range(len(self._column_configs)))

        self._data = data_list if data_list else []
        self._empty_placeholder_count = 20 # 无数据时显示的空行数

    def rowCount(self, parent=QModelIndex()):
        # 即使数据为空，也返回空行数，确保网格显示
        return max(len(self._data), self._empty_placeholder_count)

    def columnCount(self, parent=QModelIndex()):
        return len(self._visible_indices)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        # 处理空行逻辑
        if index.row() >= len(self._data):
            return None

        row_obj = self._data[index.row()]
        col_conf = self._column_configs[self._visible_indices[index.column()]]

        if role == Qt.DisplayRole:
            # 【业务逻辑】如果该列是 CPN 级别的，且不是块的第一行，则留空
            if col_conf["is_cpn_level"] and not row_obj.is_first_in_block:
                return ""

            val = getattr(row_obj, col_conf["key"])
            return str(val)

        # 视觉辅助：块的第一行稍微换个底色（可选）
        if role == Qt.BackgroundRole:
            if row_obj.is_first_in_block:
                return QColor("#FFFFFF") # 纯白
            else:
                return QColor("#FAFAFA") # 极浅灰，区分 MP 行

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._column_configs[self._visible_indices[section]]["title"]
        return None

    def sort(self, column, order):
        """
        高性能块状排序：
        维持同一个 CPN 的 MP 始终在一起，并确保第一行显示主信息。
        """
        if not self._data:
            return

        self.layoutAboutToBeChanged.emit()

        # 1. 确定排序列的 Key
        col_idx = self._visible_indices[column]
        key = self._column_configs[col_idx]["key"]
        reverse = (order == Qt.DescendingOrder)

        # 2. 执行双重排序 (Double Sorting)
        # 核心：先按 CPN 排（次要），再按目标列排（主要）。
        # Python 的 sort 是稳定的(Stable)，所以我们可以分步，或者用元组作为 Key。
        # 这里我们用元组：(目标列值, CPN值)
        self._data.sort(
            key=lambda x: (str(getattr(x, key)), x.cpn),
            reverse=reverse
        )

        # 3. 【最关键】重新扫描并重置块首标记
        # 因为排序后，原本属于同一个 CPN 块的第一行可能已经变了
        for i in range(len(self._data)):
            if i == 0:
                self._data[i].is_first_in_block = True
            else:
                # 如果当前行的 CPN 与上一行不同，则它是新块的第一行
                self._data[i].is_first_in_block = (self._data[i].cpn != self._data[i-1].cpn)

        self.layoutChanged.emit()

    def update_visible_columns(self, indices):
        """由外部控制哪些列展示"""
        self.beginResetModel()
        self._visible_indices = indices
        self.endResetModel()

# ---------------------------------------------------------
# 3. 主窗口及 Mock 数据
# ---------------------------------------------------------
class BomManagerDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BOM Manager 高性能渲染 Demo (10万行)")
        self.resize(1200, 800)

        # 1. 模拟 10 万条复合数据
        print("正在 Mock 10万条复合数据...")
        start_time = time.time()
        mock_data = self.mock_composite_data(100000)
        print(f"数据准备完成，耗时: {time.time() - start_time:.2f}秒")

        # 2. UI 布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 控制栏
        ctrl_layout = QHBoxLayout()
        self.chk_header = QCheckBox("显示列标题")
        self.chk_header.setChecked(True)
        self.chk_header.toggled.connect(self.on_toggle_header)
        ctrl_layout.addWidget(self.chk_header)

        btn_toggle_col = QPushButton("隐藏/显示 Quantity 列")
        btn_toggle_col.clicked.connect(self.on_toggle_qty_column)
        ctrl_layout.addWidget(btn_toggle_col)

        ctrl_layout.addStretch()
        layout.addLayout(ctrl_layout)

        # 3. 表格配置
        self.table = QTableView()
        self.model = BomManagerModel(mock_data)
        self.table.setModel(self.model)

        # 表头功能：移动、点击排序
        header = self.table.horizontalHeader()
        header.setSectionsMovable(True)
        header.setSectionsClickable(True)
        self.table.setSortingEnabled(True)

        # --- 极致性能设置 ---
        # 锁死行高是处理十万行数据不卡顿的秘诀
        self.table.verticalHeader().setDefaultSectionSize(28)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)

        layout.addWidget(self.table)

        self.qty_visible = True

    def mock_composite_data(self, total_rows):
        """
        模拟复合型数据：
        一个 CPN 块包含多个 MP 行
        Quantity = len(rd)
        """
        data = []
        rows_created = 0
        item_counter = 1
        vendors = ["TOYOCOM", "TI", "SAMSUNG", "MURATA", "YAGEO", "INTEL"]

        while rows_created < total_rows:
            cpn = f"00{random.randint(10, 99)}-{random.randint(100, 999)}-{random.randint(100, 999)}"

            # 模拟 RD 列表
            num_rd = random.randint(1, 20)
            rd_list = [f"R{random.randint(100, 9999)}" for _ in range(num_rd)]
            qty = len(rd_list) # 按照要求：Quantity = len(rd)
            rd_str = ", ".join(rd_list[:5]) + ("..." if num_rd > 5 else "")

            # 模拟该 CPN 下的 MP 数量
            num_mp = random.randint(1, 4)
            if rows_created + num_mp > total_rows:
                num_mp = total_rows - rows_created

            for i in range(num_mp):
                vendor = random.choice(vendors)
                mpn = f"MPN-{vendor}-{random.randint(1000, 9999)}"
                # 只有块的第一行标记为 True
                is_first = (i == 0)

                data.append(BomRow(
                    item_counter, cpn, qty, rd_str, vendor, mpn, is_first
                ))

            rows_created += num_mp
            item_counter += 1

        return data

    def on_toggle_header(self, checked):
        self.table.horizontalHeader().setVisible(checked)

    def on_toggle_qty_column(self):
        # 演示如何动态改变显示的列
        current_indices = self.model._visible_indices.copy()
        qty_col_index = 2 # Quantity 在 _column_configs 的索引是 2

        if self.qty_visible:
            if qty_col_index in current_indices:
                current_indices.remove(qty_col_index)
        else:
            if qty_col_index not in current_indices:
                current_indices.insert(2, qty_col_index)

        self.qty_visible = not self.qty_visible
        self.model.update_visible_columns(current_indices)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 设置应用级别的优化（可选）
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)

    demo = BomManagerDemo()
    demo.show()
    sys.exit(app.exec())