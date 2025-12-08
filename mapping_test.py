import sys
import json
from PySide6.QtWidgets import (QApplication, QWidget, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QHeaderView, QAbstractItemView, QLabel)
from PySide6.QtCore import Qt, QMimeData, QPoint, QRect
from PySide6.QtGui import QDrag, QPixmap, QPainter, QFont, QColor, QCursor


class DragProxy(QWidget):
    """拖拽时显示的卡片代理组件"""

    def __init__(self, text, parent=None):
        super().__init__(parent, Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet("""
            background-color: #f0f0f0;
            border: 1px solid #ccc;
            border-radius: 4px;
        """)
        layout = QVBoxLayout(self)
        self.label = QLabel(text)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        self.adjustSize()  # 自适应内容大小


class MappingTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.dragged_rows = []  # 被拖拽的行索引（仅中间列）
        self.drag_start_pos = QPoint()
        self.drag_proxy = None  # 拖拽卡片代理

    def init_ui(self):
        # 固定3列，禁止修改列数
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(["Destination Stackup", "Mapped Stackup", "Source Stackup"])
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setStretchLastSection(True)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)  # 支持多选
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        # 禁止编辑所有单元格
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def startDrag(self, supported_actions):
        # 收集被拖拽的中间列行索引（只处理中间列的选中项）
        self.dragged_rows = sorted([idx.row() for idx in self.selectedIndexes()
                                    if idx.column() == 1])  # 仅中间列（索引1）
        if not self.dragged_rows:
            return

        # 创建拖拽数据
        mime_data = QMimeData()
        drag = QDrag(self)
        drag.setMimeData(mime_data)

        # 创建拖拽卡片代理（视觉反馈）
        self.create_drag_proxy()

        # 执行拖拽
        result = drag.exec_(supported_actions)
        if self.drag_proxy:
            self.drag_proxy.deleteLater()  # 拖拽结束后删除代理
        self.clearSelection()

    def create_drag_proxy(self):
        """创建拖拽时跟随鼠标的卡片"""
        # 拼接选中项文本（多选中用换行分隔）
        texts = []
        for row in self.dragged_rows:
            item = self.item(row, 1)
            texts.append(item.text() if item else "")
        proxy_text = "\n".join(texts)

        # 创建代理组件
        self.drag_proxy = DragProxy(proxy_text, self.parent())
        # 显示在鼠标初始位置
        self.drag_proxy.move(QCursor.pos() - QPoint(50, 20))  # 偏移调整
        self.drag_proxy.show()

    def dragEnterEvent(self, event):
        # 仅接受自身的拖拽，且来自中间列
        if event.source() == self:
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        # 仅允许在中间列（索引1）内拖拽
        index = self.indexAt(event.position().toPoint())
        if index.isValid() and index.column() == 1:
            event.acceptProposedAction()
            # 更新拖拽卡片位置
            if self.drag_proxy:
                self.drag_proxy.move(QCursor.pos() - QPoint(50, 20))
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.source() != self or not self.dragged_rows:
            event.ignore()
            return

        # 获取目标行（中间列）
        target_index = self.indexAt(event.position().toPoint())
        if not target_index.isValid() or target_index.column() != 1:
            event.ignore()
            return
        target_row = target_index.row()

        # 保存当前中间列数据用于回滚
        current_mapped = [self.item(row, 1).text() if self.item(row, 1) else ""
                          for row in range(self.rowCount())]

        # 执行移动操作（仅中间列）
        self.move_mapped_items(self.dragged_rows, target_row)

        # 验证合法性
        validation_data = self.get_current_data()
        if not self.parent().apply_module_mapping_ok(validation_data):
            # 验证失败，回滚
            self.restore_mapped_data(current_mapped)

        event.acceptProposedAction()

    def move_mapped_items(self, source_rows, target_row):
        """移动中间列的项（仅操作行，不改变列数）"""
        # 过滤无效行索引
        source_rows = [r for r in source_rows if 0 <= r < self.rowCount()]
        if not source_rows or target_row < 0 or target_row >= self.rowCount():
            return

        # 去重并排序
        source_rows = sorted(list(set(source_rows)))
        # 确保目标行不在源行中
        if target_row in source_rows:
            return

        # 提取源行数据
        source_items = [self.takeItem(row, 1) for row in source_rows]

        # 计算调整后的目标行（因删除源行导致的偏移）
        adjust = 0
        for r in source_rows:
            if r < target_row:
                adjust += 1
        new_target = target_row - adjust

        # 插入空白项占位（保持行数不变）
        for i in range(len(source_items)):
            self.insertRow(new_target)
            # 给新行的其他列填充空白（避免影响左右列）
            self.setItem(new_target, 0, QTableWidgetItem(""))
            self.item(new_target, 0).setFlags(Qt.NoItemFlags)  # 不可选中
            self.setItem(new_target, 2, QTableWidgetItem(""))
            self.item(new_target, 2).setFlags(Qt.NoItemFlags)
            # 中间列插入空白（后续替换为源数据）
            self.setItem(new_target, 1, QTableWidgetItem(""))

        # 插入源数据到新位置
        for i, item in enumerate(source_items):
            if new_target + i < self.rowCount():
                self.setItem(new_target + i, 1, item)

        # 删除源行（已提取数据的行）
        # 倒序删除，避免索引混乱
        for row in sorted(source_rows, reverse=True):
            if row < self.rowCount():  # 确保行仍存在
                self.removeRow(row)

    def get_current_data(self):
        """获取当前表格数据（保持原始JSON结构）"""
        data = {
            "Destination Stackup": [],
            "Mapped Stackup": [],
            "Source Stackup": []
        }
        for row in range(self.rowCount()):
            # 左侧列（非空才保留）
            dest_item = self.item(row, 0)
            if dest_item and dest_item.text():
                data["Destination Stackup"].append({"name": dest_item.text()})
            # 中间列（无论是否为空都保留）
            mapped_item = self.item(row, 1)
            data["Mapped Stackup"].append({"name": mapped_item.text() if mapped_item else ""})
            # 右侧列（非空才保留）
            source_item = self.item(row, 2)
            if source_item and source_item.text():
                data["Source Stackup"].append({"name": source_item.text()})
        return data

    def restore_mapped_data(self, mapped_data):
        """回滚中间列数据"""
        # 清空中间列
        for row in range(self.rowCount()):
            self.takeItem(row, 1)
        # 恢复数据（行数不足则补充）
        for row, text in enumerate(mapped_data):
            if row >= self.rowCount():
                self.insertRow(row)
                # 补充左右列空白
                self.setItem(row, 0, QTableWidgetItem(""))
                self.item(row, 0).setFlags(Qt.NoItemFlags)
                self.setItem(row, 2, QTableWidgetItem(""))
                self.item(row, 2).setFlags(Qt.NoItemFlags)
            item = QTableWidgetItem(text)
            self.setItem(row, 1, item)

    def mousePressEvent(self, event):
        # 记录拖拽起点（仅中间列）
        if event.button() == Qt.LeftButton:
            index = self.indexAt(event.position().toPoint())
            if index.isValid() and index.column() == 1:
                self.drag_start_pos = event.position().toPoint()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        # 启动拖拽（超过最小拖拽距离）
        if not (event.buttons() & Qt.LeftButton):
            return
        if (event.position().toPoint() - self.drag_start_pos).manhattanLength() < \
                QApplication.startDragDistance():
            return
        self.startDrag(Qt.MoveAction)


class MappingWidget(QWidget):
    def __init__(self, data):
        super().__init__()
        self.original_data = data
        self.init_ui()
        self.populate_table()

    def init_ui(self):
        self.setWindowTitle("Stackup Mapping")
        self.setGeometry(100, 100, 1000, 500)
        layout = QVBoxLayout(self)
        self.table = MappingTableWidget(self)
        layout.addWidget(self.table)

    def populate_table(self):
        """初始化表格数据（行数取左右列的最大值）"""
        dest = self.original_data["Destination Stackup"]
        mapped = self.original_data["Mapped Stackup"]
        source = self.original_data["Source Stackup"]

        # 行数 = 左侧和右侧的最大长度
        row_count = max(len(dest), len(source))
        self.table.setRowCount(row_count)

        # 填充左侧列（靠上，不足留空）
        for row, item_data in enumerate(dest):
            item = QTableWidgetItem(item_data["name"])
            item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 0, item)

        # 填充中间列（按原始数据，空值也保留）
        for row, item_data in enumerate(mapped):
            # 若中间列数据超过行数，扩展行
            if row >= row_count:
                self.table.insertRow(row)
            item = QTableWidgetItem(item_data["name"])
            item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 1, item)

        # 填充右侧列（靠上，不足留空）
        for row, item_data in enumerate(source):
            item = QTableWidgetItem(item_data["name"])
            item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 2, item)

    def apply_module_mapping_ok(self, json_data):
        """验证拖拽后位置是否合法（示例规则）"""
        print("\n验证映射合法性：")
        print(json.dumps(json_data, indent=2, ensure_ascii=False))

        # 示例规则：中间列非空项不能超过左侧列数量
        mapped_non_empty = sum(1 for item in json_data["Mapped Stackup"] if item["name"])
        if mapped_non_empty > len(json_data["Destination Stackup"]):
            print("❌ 验证失败：中间列非空项超过左侧列数量")
            return False

        print("✅ 验证通过")
        return True


if __name__ == "__main__":
    # 测试数据
    json_data = {
        "Destination Stackup": [
            {"name": "Destination Stackup1"},
            {"name": "Destination Stackup2"},
            {"name": "Destination Stackup3"},
            {"name": "Destination Stackup4"},
        ],
        "Mapped Stackup": [
            {"name": "Mapped Stackup1"},
            {"name": "Mapped Stackup2"},
            {"name": "Mapped Stackup3"},
            {"name": "Mapped Stackup4"},
            {"name": ""},
            {"name": ""},
        ],
        "Source Stackup": [
            {"name": "Source Stackup1"},
            {"name": "Source Stackup2"},
            {"name": "Source Stackup3"},
            {"name": "Source Stackup4"},
            {"name": "Source Stackup5"},
            {"name": "Source Stackup6"},
        ],
    }

    app = QApplication(sys.argv)
    window = MappingWidget(json_data)
    window.show()
    sys.exit(app.exec())