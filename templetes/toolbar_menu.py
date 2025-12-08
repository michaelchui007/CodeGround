import sys
from typing import Tuple

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QToolButton,
    QMenu, QWidgetAction, QWidget, QHBoxLayout,
    QCheckBox, QComboBox
)
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QStyle

# --- 1. FilterItemWidget 类 (保持不变) ---
class FilterItemWidget(QWidget):
    filter_changed = Signal()

    def __init__(self, key, options, parent=None):
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
    def on_user_interaction(self):
        sender = self.sender()
        if sender == self.checkbox:
            self.filter_changed.emit()
        elif sender == self.combo:
            if self.checkbox.isChecked():
                self.filter_changed.emit()

    def get_filter_data(self) -> Tuple[str, bool, str]:
        """
        获取筛选数据
        Returns:
            key, 是否选中， 选中文本
        """
        return self.key, self.checkbox.isChecked(), self.combo.currentText()


# --- 2. DemoMainWindow 类 (实现图标切换逻辑) ---

class DemoMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 极简筛选菜单 Demo (图标切换)")
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

        self.filter_widgets = []

        # 必须先设置按钮和图标
        self.setup_filter_button()
        self.populate_filter_menu()

        # 确保启动时图标状态正确（虽然默认都是未勾选）
        self.update_filter_icon_state(0)

    def setup_filter_button(self):
        """创建带图标和菜单的 QToolButton，并定义两个图标"""

        # 定义两个图标（使用 Qt 标准图标替代你的 custom icon1 和 icon2）
        # Icon1: 默认/未激活状态
        self.icon_default = self.style().standardIcon(QStyle.SP_FileDialogDetailedView)
        # Icon2: 激活状态 (这里使用了一个明显不同的图标)
        self.icon_active = self.style().standardIcon(QStyle.SP_DialogApplyButton)
        # 实际项目中，你可以用 QIcon("path/to/icon1.png") 和 QIcon("path/to/icon2.png") 替换

        self.filter_btn = QToolButton(self)
        self.filter_btn.setIcon(self.icon_default) # 初始设置为默认图标
        self.filter_btn.setToolTip("筛选设置")

        self.filter_btn.setPopupMode(QToolButton.InstantPopup)

        self.filter_menu = QMenu(self)
        self.filter_btn.setMenu(self.filter_menu)

        self.toolbar.addWidget(self.filter_btn)

    def populate_filter_menu(self):
        """填充菜单并连接信号"""
        for config in self.filter_configs:
            item_widget = FilterItemWidget(config["key"], config["options"])

            # 连接子 Widget 的信号到主窗口的 Slot
            item_widget.filter_changed.connect(self.perform_realtime_filter)
            self.filter_widgets.append(item_widget)

            action = QWidgetAction(self.filter_menu)
            action.setDefaultWidget(item_widget)

            self.filter_menu.addAction(action)

    @Slot()
    def perform_realtime_filter(self):
        """
        实时执行筛选逻辑，并统计活动的筛选器数量以更新图标
        """
        print("\n--- 筛选条件变更，执行实时查询 ---")
        query_params = {}
        active_count = 0 # <-- 新增：计数器

        for widget in self.filter_widgets:
            key, is_active, value = widget.get_filter_data()

            if is_active:
                query_params[key] = value
                active_count += 1 # <-- 计数

        print(f"  >>> 最终查询参数: {query_params}")

        # 调用图标更新逻辑
        self.update_filter_icon_state(active_count)

    def update_filter_icon_state(self, count):
        """
        根据活动的筛选器数量设置工具栏图标
        """
        if count > 0:
            # 至少有一个筛选器被激活，显示 icon2
            self.filter_btn.setIcon(self.icon_active)
            print(f"  >>> 筛选器已激活 ({count} 个)，切换到 Icon2")
        else:
            # 没有筛选器被激活，显示默认 icon1
            self.filter_btn.setIcon(self.icon_default)
            print("  >>> 筛选器已清空，切换回默认 Icon1")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DemoMainWindow()
    window.show()
    sys.exit(app.exec())