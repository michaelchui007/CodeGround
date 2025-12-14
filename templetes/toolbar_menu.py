import sys
from typing import Tuple, Dict, List # 明确类型提示
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QToolButton,
    QMenu, QWidgetAction, QWidget, QHBoxLayout,
    QCheckBox, QComboBox
)
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QIcon, QAction # 引入 QAction
from PySide6.QtWidgets import QStyle

# --- 1. FilterItemWidget 类 (保持不变) ---
class FilterItemWidget(QWidget):
    filter_changed = Signal()

    def __init__(self, key: str, options: List[str], parent: QWidget = None):
        super().__init__(parent)
        self.key = key

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(5, 2, 5, 2)
        self.layout.setSpacing(5)

        self.checkbox = QCheckBox()
        self.layout.addWidget(self.checkbox)

        self.combo = QComboBox()
        self.combo.addItems(options)
        self.layout.addWidget(self.combo)

        self.layout.setStretch(0, 0)
        self.layout.setStretch(1, 1)

        self.checkbox.stateChanged.connect(self.on_user_interaction)
        self.combo.currentIndexChanged.connect(self.on_user_interaction)

    @Slot()
    def on_user_interaction(self) -> None:
        sender = self.sender()
        if sender == self.checkbox:
            self.filter_changed.emit()
        elif sender == self.combo:
            if self.checkbox.isChecked():
                self.filter_changed.emit()

    def get_filter_data(self) -> Tuple[str, bool, str]:
        return self.key, self.checkbox.isChecked(), self.combo.currentText()

    def reset(self) -> None:
        """将复选框重置为未选中状态。"""
        self.checkbox.setChecked(False)


# --- 2. DemoMainWindow 类 (实现图标切换逻辑和清除按钮) ---

class DemoMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 极简筛选菜单 Demo (图标切换和清除)")
        self.resize(500, 300)

        self.toolbar = QToolBar("Filter Toolbar")
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)

        self.toolbar.addAction("保存")
        self.toolbar.addAction("设置")

        self.filter_configs = [
            {"key": "status",  "options": ["Viewed", "Not Viewed"]},
            {"key": "priority", "options": ["High", "Medium", "Low"]},
            {"key": "user", "options": ["Alice", "Bob", "Charlie"]},
        ]

        self.filter_widgets: List[FilterItemWidget] = []

        self.setup_filter_button()
        self.populate_filter_menu()

        self.update_filter_icon_state(0)

    def setup_filter_button(self):
        """创建带图标和菜单的 QToolButton，并定义两个图标"""
        self.icon_default = self.style().standardIcon(QStyle.SP_FileDialogDetailedView)
        self.icon_active = self.style().standardIcon(QStyle.SP_DialogApplyButton)

        self.filter_btn = QToolButton(self)
        self.filter_btn.setIcon(self.icon_default)
        self.filter_btn.setToolTip("筛选设置")

        self.filter_btn.setPopupMode(QToolButton.InstantPopup)

        self.filter_menu = QMenu(self)
        self.filter_btn.setMenu(self.filter_menu)

        self.toolbar.addWidget(self.filter_btn)

    def populate_filter_menu(self):
        """
        填充菜单，包括顶部的“清除筛选”按钮。
        """
        # 1. 【新增】创建并添加“清除筛选” QAction
        clear_action = QAction("清除筛选", self)
        # 使用 QStyle.SP_DialogResetButton 作为图标，表示重置/清除
        clear_action.setIcon(self.style().standardIcon(QStyle.SP_DialogResetButton))

        # 连接到新的槽函数
        clear_action.triggered.connect(self.clear_all_filters)
        self.filter_menu.addAction(clear_action)

        # 添加分隔符，与下面的动态筛选控件区分开
        self.filter_menu.addSeparator()

        # 2. 填充动态筛选控件
        for config in self.filter_configs:
            item_widget = FilterItemWidget(config["key"], config["options"])

            item_widget.filter_changed.connect(self.perform_realtime_filter)
            self.filter_widgets.append(item_widget)

            action = QWidgetAction(self.filter_menu)
            action.setDefaultWidget(item_widget)

            self.filter_menu.addAction(action)

    @Slot()
    def clear_all_filters(self):
        """
        【新增】清除所有筛选条件，重置所有复选框并触发筛选逻辑。
        """
        print("\n--- 执行清除筛选操作 ---")

        # 1. 遍历并重置所有 FilterItemWidget 的复选框状态
        for widget in self.filter_widgets:
            widget.reset() # 调用 FilterItemWidget 中新增的 reset 方法

        # 2. 触发一次筛选更新 (这也会更新工具栏图标)
        self.perform_realtime_filter()

        print("--- 筛选已清除，显示全部数据 ---")


    @Slot()
    def perform_realtime_filter(self):
        """
        实时执行筛选逻辑，并统计活动的筛选器数量以更新图标
        """
        print("\n--- 筛选条件变更，执行实时查询 ---")
        query_params: Dict[str, str] = {}
        active_count: int = 0

        for widget in self.filter_widgets:
            key, is_active, value = widget.get_filter_data()

            if is_active:
                query_params[key] = value
                active_count += 1

        print(f"  >>> 最终查询参数: {query_params}")

        self.update_filter_icon_state(active_count)

    def update_filter_icon_state(self, count: int):
        """
        根据活动的筛选器数量设置工具栏图标
        """
        if count > 0:
            self.filter_btn.setIcon(self.icon_active)
            print(f"  >>> 筛选器已激活 ({count} 个)，切换到 Icon2")
        else:
            self.filter_btn.setIcon(self.icon_default)
            print("  >>> 筛选器已清空，切换回默认 Icon1")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DemoMainWindow()
    window.show()
    sys.exit(app.exec())