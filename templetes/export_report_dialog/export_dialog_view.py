import sys
from PySide6.QtWidgets import QDialog, QApplication, QAbstractItemView, QListWidget, QListWidgetItem
from PySide6.QtCore import Qt

from templetes.export_report_dialog.ui_export_dialog import Ui_ExportDialog


class ExportReportView(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ExportDialog()
        self.ui.setupUi(self)

        self.init_ui_setup()
        self.init_data()
        self.init_connections()

    # ... (init_ui_setup 代码保持不变，此处省略) ...
    def init_ui_setup(self):
        # 保持您原来的布局调整代码
        layout = self.ui.groupBox_columns.layout()
        layout.setColumnStretch(0, 10)
        layout.setColumnStretch(1, 0)
        layout.setColumnStretch(2, 10)
        layout.setColumnStretch(3, 0)

        min_btn_width = 40
        buttons = [self.ui.btn_move_left, self.ui.btn_move_right,
                   self.ui.btn_top, self.ui.btn_up, self.ui.btn_down, self.ui.btn_bottom]
        for btn in buttons:
            btn.setMinimumWidth(min_btn_width)

        self.ui.btn_ok.setFixedSize(80, 30)
        self.ui.btn_cancel.setFixedSize(80, 30)
        self.ui.le_template.setPlaceholderText("模板存放路径")
        self.ui.le_save_path.setPlaceholderText("保存文件路径")
        self.ui.le_project_name.setPlaceholderText("job name")
        self.ui.list_available.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.ui.list_output.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def init_data(self):
        """
        初始化数据：核心在于'同步'左侧的隐藏状态
        """
        self.ui.combo_format.addItems(["Html", "PDF", "Excel"])

        # 1. 定义全量的列名 (按照初始顺序)
        all_columns = [f"选项{i}" for i in range(1, 20)]

        # 2. 定义默认已经在右边的列
        default_selected = ["选项1", "选项2"]

        # 3. 填充左侧列表 (全部填充)
        for col_name in all_columns:
            item = QListWidgetItem(col_name)
            self.ui.list_available.addItem(item)

            # 【关键逻辑】如果这个项默认在右边，左边就得隐藏它
            if col_name in default_selected:
                item.setHidden(True)

        # 4. 填充右侧列表
        self.ui.list_output.addItems(default_selected)

    def init_connections(self):
        self.ui.btn_move_right.clicked.connect(self.on_move_right)
        self.ui.btn_move_left.clicked.connect(self.on_move_left)

        # 排序逻辑复用之前的
        self.ui.btn_top.clicked.connect(lambda: self.on_reorder("top"))
        self.ui.btn_up.clicked.connect(lambda: self.on_reorder("up"))
        self.ui.btn_down.clicked.connect(lambda: self.on_reorder("down"))
        self.ui.btn_bottom.clicked.connect(lambda: self.on_reorder("bottom"))

        self.ui.btn_ok.clicked.connect(self.accept)
        self.ui.btn_cancel.clicked.connect(self.reject)

    # ==========================
    #       修改后的移动逻辑
    # ==========================

    def on_move_right(self):
        """ 左 -> 右：复制 + 隐藏左侧 """
        source_list = self.ui.list_available
        target_list = self.ui.list_output

        selected_items = source_list.selectedItems()
        if not selected_items:
            return

        for item in selected_items:
            # 1. 在右侧创建一个新的 item (副本)
            new_item = QListWidgetItem(item.text())
            target_list.addItem(new_item)

            # 2. 在左侧隐藏该 item，并取消选中状态
            item.setHidden(True)
            item.setSelected(False)

    def on_move_left(self):
        """ 右 -> 左：删除右侧 + 显示左侧 """
        source_list = self.ui.list_output  # 右边
        target_list = self.ui.list_available # 左边

        selected_items = source_list.selectedItems()
        if not selected_items:
            return

        for item in selected_items:
            text = item.text()

            # 1. 在左侧找到对应的 item 并“复活” (Show)
            # findItems 返回的是列表，Qt.MatchExactly 确保全字匹配
            found_items = target_list.findItems(text, Qt.MatchExactly)
            if found_items:
                original_item = found_items[0]
                original_item.setHidden(False)
                # 可选：移回去后自动选中左侧的该项，方便用户知道它回哪儿了
                # original_item.setSelected(True)

            # 2. 从右侧彻底删除
            row = source_list.row(item)
            source_list.takeItem(row)

    # ==========================
    #       排序逻辑 (保持不变)
    # ==========================
    def on_reorder(self, direction: str):
        """右侧列表内部排序，代码逻辑不需要变"""
        list_widget = self.ui.list_output
        selected_items = list_widget.selectedItems()
        if not selected_items: return

        rows = sorted([list_widget.row(item) for item in selected_items])
        items_to_move = [list_widget.item(r) for r in rows]

        if direction == "top":
            for row in reversed(rows): list_widget.takeItem(row)
            for i, item in enumerate(items_to_move):
                list_widget.insertItem(i, item)
                item.setSelected(True)

        elif direction == "bottom":
            for row in reversed(rows): list_widget.takeItem(row)
            for item in items_to_move:
                list_widget.addItem(item)
                item.setSelected(True)

        elif direction == "up":
            if rows[0] == 0: return
            for item in items_to_move:
                row = list_widget.row(item)
                list_widget.takeItem(row)
                list_widget.insertItem(row - 1, item)
                item.setSelected(True)

        elif direction == "down":
            if rows[-1] == list_widget.count() - 1: return
            for item in reversed(items_to_move):
                row = list_widget.row(item)
                list_widget.takeItem(row)
                list_widget.insertItem(row + 1, item)
                item.setSelected(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExportReportView()
    window.show()
    sys.exit(app.exec())