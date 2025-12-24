from PySide6.QtWidgets import QComboBox
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt, QEvent, Signal

class CheckableComboBox(QComboBox):
    # 【核心修改】定义一个新信号，传参：(index, selected)
    # index: int (变更的行索引)
    # selected: bool (变更后的状态: True选中, False未选中)
    itemToggled = Signal(int, bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)

        self.model = QStandardItemModel(self)
        self.setModel(self.model)

        self.view().viewport().installEventFilter(self)

        self.setFixedHeight(20)
        self.setMinimumWidth(177)

        # 初始显示
        self.update_display_text()

    def eventFilter(self, widget, event):
        """拦截点击事件，立即触发单个变更"""
        if widget == self.view().viewport() and event.type() == QEvent.MouseButtonRelease:
            index_obj = self.view().indexAt(event.pos())
            item = self.model.itemFromIndex(index_obj)

            # 排除无效点击、禁用项（如分割线）
            if item and item.isEnabled() and item.isCheckable():
                # 1. 获取当前行号 (Row Index)
                row_index = index_obj.row()

                # 2. 状态翻转
                old_state = item.checkState()
                new_state = Qt.Checked if old_state == Qt.Unchecked else Qt.Unchecked
                item.setCheckState(new_state)

                # 3. 更新 UI 显示文本
                self.update_display_text()

                # 4. 【关键】立即触发信号，传回 (index, selected)
                is_selected = (new_state == Qt.Checked)
                self.itemToggled.emit(row_index, is_selected)

                return True # 拦截事件，防止下拉框关闭

        return super().eventFilter(widget, event)

    def update_display_text(self):
        """UI 显示逻辑：拼接文本"""
        checked_texts = []
        for i in range(self.model.rowCount()):
            item = self.model.item(i)
            # 跳过分割线
            if item and item.isCheckable() and item.checkState() == Qt.Checked:
                checked_texts.append(item.text())

        text_to_show = ";".join(checked_texts) if checked_texts else "..."
        self.lineEdit().setText(text_to_show)

    def update_data(self, checklist: list, dfm_checklist: list):
        """初始化数据，默认全部不选中"""
        self.model.clear()

        # 添加第一部分
        for text in checklist:
            self._add_checkable_item(text)

        # 添加分割线 (占位 index)
        if checklist and dfm_checklist:
            self.insertSeparator(self.model.rowCount())

        # 添加第二部分
        for text in dfm_checklist:
            self._add_checkable_item(text)

        # 刷新显示
        self.update_display_text()

    def _add_checkable_item(self, text):
        item = QStandardItem(text)
        item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        # 默认为 Unchecked (不选中)
        item.setData(Qt.Unchecked, Qt.CheckStateRole)
        self.model.appendRow(item)