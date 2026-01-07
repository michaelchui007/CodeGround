import sys
from PySide6.QtWidgets import (QApplication, QTableView, QHeaderView,
                               QAbstractItemView, QWidget, QVBoxLayout)
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, QRect
from PySide6.QtGui import QStandardItemModel, QStandardItem, QColor

class FrozenTableView(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)

        # --- 1. 初始化主视图 ---
        self.frozen_row_count = 2  # 设置冻结前几行

        # --- 2. 创建冻结视图 (作为主视图的子控件) ---
        self.frozen_view = QTableView(self)

        # 配置冻结视图的外观，使其看起来和主视图融为一体
        self.frozen_view.setFocusPolicy(Qt.NoFocus) # 冻结视图不抢焦点
        self.frozen_view.verticalHeader().hide()    # 隐藏垂直表头(稍后通过布局对齐)
        self.frozen_view.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)

        # 隐藏滚动条，因为我们通过代码同步滚动
        self.frozen_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.frozen_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 将冻结视图置于顶层
        self.frozen_view.show()

        # --- 3. 信号连接与同步 ---
        # 同步水平表头 (调整列宽时同步)
        self.horizontalHeader().sectionResized.connect(self.update_frozen_section_width)
        self.verticalHeader().sectionResized.connect(self.update_frozen_geometry)

        # 同步水平滚动 (主视图横向滚动时，冻结视图也要跟着动)
        self.horizontalScrollBar().valueChanged.connect(self.frozen_view.horizontalScrollBar().setValue)

    def setModel(self, model):
        """重写 setModel，确保两个视图共享同一个数据模型"""
        super().setModel(model)
        self.frozen_view.setModel(model)

        # 共享选择模型：在一个视图选中单元格，另一个也会高亮
        self.frozen_view.setSelectionModel(self.selectionModel())

        # 初始化冻结视图的列宽与主视图一致
        for col in range(model.columnCount()):
            self.frozen_view.setColumnWidth(col, self.columnWidth(col))

        self.update_frozen_geometry()

    def update_frozen_section_width(self, logical_index, old_size, new_size):
        """当主视图列宽改变时，同步给冻结视图"""
        self.frozen_view.setColumnWidth(logical_index, new_size)
        self.update_frozen_geometry()

    def update_frozen_geometry(self):
        """核心逻辑：计算并设置冻结视图的位置和大小"""
        # 1. 计算冻结区域的高度 (前N行的高度总和)
        total_height = 0
        for row in range(self.frozen_row_count):
            total_height += self.rowHeight(row)

        # 如果还要显示网格线，可能需要微调像素，这里保持简单

        # 2. 设置冻结视图的位置
        # 它应该位于主视图的视口(viewport)坐标系内
        # x: 0 (紧贴左侧)
        # y: 0 (紧贴顶部)
        # w: 主视图视口的宽度
        # h: 计算出的冻结高度
        self.frozen_view.setGeometry(
            self.verticalHeader().width() + self.frameWidth(), # X: 偏移垂直表头宽度
            self.frameWidth() + self.horizontalHeader().height(), # Y: 偏移水平表头高度
            self.viewport().width(), # Width
            total_height # Height
        )

    def resizeEvent(self, event):
        """当窗口大小改变时，重新计算冻结视图大小"""
        super().resizeEvent(event)
        self.update_frozen_geometry()

    def moveCursor(self, cursor_action, modifiers):
        """
        处理键盘导航。
        当从冻结区域向下移动光标时，确保主视图正确滚动。
        """
        current = super().moveCursor(cursor_action, modifiers)

        # 如果移动到了非冻结区，且被冻结区遮挡了，需要手动滚出来
        if (cursor_action == QAbstractItemView.MoveDown and
                current.row() > self.frozen_row_count and
                self.visualRect(current).top() < self.frozen_view.height()):

            self.scrollTo(current, QAbstractItemView.EnsureVisible)

        return current

    def scrollTo(self, index, hint=QAbstractItemView.EnsureVisible):
        """
        重写滚动逻辑。
        防止主视图自动滚动时，目标行被冻结视图遮挡。
        """
        if index.row() < self.frozen_row_count:
            return # 冻结行不需要滚动

        super().scrollTo(index, hint)

# --- 下面是测试用的 Demo 代码 ---

class DemoWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 冻结前两行示例")
        self.resize(800, 600)

        layout = QVBoxLayout(self)

        # 1. 创建数据模型
        self.model = QStandardItemModel(50, 10) # 50行，10列

        # 2. 填充测试数据
        for row in range(50):
            for col in range(10):
                item = QStandardItem(f"Row {row+1}, Col {col+1}")
                # 给前两行加个背景色，方便区分
                if row < 2:
                    item.setBackground(QColor("#ffebcd")) # 浅黄色背景
                    item.setForeground(QColor("red"))
                    item.setText(item.text() + " (冻结)")
                self.model.setItem(row, col, item)

        # 3. 使用自定义的 FrozenTableView
        self.table = FrozenTableView()
        self.table.setModel(self.model)

        layout.addWidget(self.table)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DemoWindow()
    window.show()
    sys.exit(app.exec())