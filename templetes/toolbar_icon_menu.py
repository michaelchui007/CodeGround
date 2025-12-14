# -*- coding: utf-8 -*-
"""
封装纯图标 QMenu 按钮：实现选中状态隔离、业务逻辑注入、图标和 Tooltip 同步替换
"""
import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QToolBar, QToolButton,
                               QMenu, QWidgetAction, QLabel, QWidget, QHBoxLayout)
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt, QSize, QDir, QEvent, Slot, Signal
from functools import partial
from typing import List, Tuple, Callable, Dict

# --- 1. 可重用的公共组件类 ---

class ExclusiveIconMenuButton(QToolButton):
    """
    一个带下拉菜单的 QToolButton，其菜单项为纯图标，且具有互斥的选中高亮状态。

    点击菜单项后，外部按钮图标和 Tooltip 会被替换成选中项的图标和 Tooltip。
    """
    action_triggered = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        # 状态管理
        self.current_selected_widget: QWidget = None
        self._action_callbacks: Dict[QWidget, Callable] = {} # 存储业务函数
        self._action_icons: Dict[QWidget, QIcon] = {}        # 存储图标实例
        # 【新增】存储 Tooltip 文本
        self._action_tooltips: Dict[QWidget, str] = {}

        # 初始化常量
        self.ICON_SIZE = QSize(24, 24)
        self.ITEM_SIZE = QSize(32, 32)
        self.SELECT_COLOR = "#188db1"
        self.NORMAL_COLOR = "white"

        # UI 初始化
        self.menu = QMenu(self)
        self.setMenu(self.menu)
        self.set_menu_style()

        self.setFixedSize(45, 45)
        self.setIconSize(QSize(28, 28))
        self.setIcon(QIcon.fromTheme("edit-select")) # 初始默认图标
        # 初始默认 Tooltip
        self.setToolTip("默认功能选择")
        self.setPopupMode(QToolButton.MenuButtonPopup)

    def set_menu_style(self):
        """设置菜单的基础 QSS 样式，并添加 QToolTip 样式。"""
        menu_qss = f"""
            QMenu::item {{
                padding: 0px;
                margin: 0px;
                min-height: {self.ITEM_SIZE.height()}px;
                min-width: {self.ITEM_SIZE.width()}px;
            }}

            QMenu::item:selected {{
                background-color: transparent; 
                border: 0px;
            }}

            QMenu {{
                padding: 3px;
                border: 1px solid #dddddd;
                border-radius: 6px;
                background-color: white;
            }}

            QToolTip {{
                border: 1px solid #76797C; 
                background-color: #262626; 
                color: white; 
                padding: 4px;
                border-radius: 4px;
                opacity: 255; 
            }}

            QLabel {{
                margin: 0px;
                padding: 0px;
            }}
        """
        self.menu.setStyleSheet(menu_qss)

    def configure_actions(self, configs: List[Tuple[str, str, Callable]]):
        """
        公共接口：根据传入的配置列表添加菜单项。

        Args:
            configs: [(icon_path, tooltip, callback_func), ...] 的列表
        """
        for icon_path, tooltip, callback in configs:
            # 1. 加载图标
            icon = self._load_icon(icon_path)

            # 2. 创建自定义widget（带悬停事件）
            item_widget = self._create_hover_widget(icon, tooltip)

            # 3. 创建QWidgetAction
            widget_action = QWidgetAction(self.menu)
            widget_action.setDefaultWidget(item_widget)
            widget_action.setToolTip(tooltip)

            # 4. 存储回调函数、图标和 Tooltip 文本
            self._action_callbacks[item_widget] = callback
            self._action_icons[item_widget] = icon
            self._action_tooltips[item_widget] = tooltip # 【修改点】存储 Tooltip 文本

            # 5. 绑定点击事件
            widget_action.triggered.connect(partial(self.handle_action_click, item_widget))

            self.menu.addAction(widget_action)

        # 6. 初始化默认选中第一个 Action，并设置外部图标和 Tooltip
        if self.menu.actions():
            first_action = self.menu.actions()[0]
            first_widget = first_action.defaultWidget()
            # if first_widget:
            #     self.set_action_selected(first_widget)

    def _load_icon(self, icon_path: str) -> QIcon:
        """加载图标文件，如果失败则使用主题图标。"""
        if not os.path.exists(icon_path):
            print(f"⚠️  警告：图标路径不存在 → {icon_path}")
            return QIcon.fromTheme("image-1")

        pixmap = QPixmap(icon_path)
        if pixmap.isNull():
            print(f"⚠️  警告：图标加载失败 → {icon_path}")
            return QIcon.fromTheme("image-1")

        pixmap = pixmap.scaled(self.ICON_SIZE, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        return QIcon(pixmap)

    def _create_hover_widget(self, icon: QIcon, tooltip: str) -> QWidget:
        """创建带鼠标悬停效果和居中图标的 QWidget。"""
        widget = QWidget()
        widget.setFixedSize(self.ITEM_SIZE)
        widget.setToolTip(tooltip)
        widget.setStyleSheet(f"background-color: {self.NORMAL_COLOR}; border-radius: 4px;")

        # 绑定鼠标悬停/离开事件到本类的 eventFilter
        widget.installEventFilter(self)

        # 居中布局
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)

        # 图标标签
        icon_label = QLabel()
        icon_label.setPixmap(icon.pixmap(self.ICON_SIZE))

        layout.addWidget(icon_label)
        return widget

    def set_action_selected(self, action_widget: QWidget):
        """设置指定的 action_widget 为选中状态，清除旧状态，同时替换外部按钮图标和 Tooltip。"""
        # 1. 清除旧的高亮状态
        if self.current_selected_widget and self.current_selected_widget != action_widget:
            self.current_selected_widget.setStyleSheet(
                f"background-color: {self.NORMAL_COLOR}; border-radius: 4px;"
            )

        # 2. 设置新的高亮状态
        action_widget.setStyleSheet(
            f"background-color: {self.SELECT_COLOR}; border-radius: 4px;"
        )

        # 3. 替换外部按钮图标和 Tooltip 【核心修改点】
        selected_icon = self._action_icons.get(action_widget)
        selected_tooltip = self._action_tooltips.get(action_widget)

        if selected_icon:
            self.setIcon(selected_icon)

        if selected_tooltip:
            self.setToolTip(selected_tooltip) # 更新主按钮的 Tooltip

        # 4. 更新状态变量
        self.current_selected_widget = action_widget

        # 5. 隐藏菜单
        self.menu.hide()

    def handle_action_click(self, action_widget: QWidget, checked: bool = False):
        """处理 QWidgetAction 被触发的点击事件，执行业务逻辑并管理选中状态。"""

        # 1. 管理选中状态和外部 UI 替换
        self.set_action_selected(action_widget)

        # 2. 执行对应 action 的业务逻辑
        callback = self._action_callbacks.get(action_widget)
        tooltip = action_widget.toolTip()

        if callback:
            print(f"✅ 点击功能：{tooltip} - 触发专属业务逻辑。")
            callback(tooltip)

            # 3. 通过信号通知外部调用者
        self.action_triggered.emit(tooltip)


    def eventFilter(self, obj, event):
        """事件过滤器：监听widget的鼠标悬停/离开事件，并保护选中状态。"""
        if isinstance(obj, QWidget):

            if event.type() == QEvent.Enter:
                # 鼠标进入：设置悬停高亮
                obj.setStyleSheet(f"background-color: {self.SELECT_COLOR}; border-radius: 4px;")

            elif event.type() == QEvent.Leave:
                # 鼠标离开：
                if obj == self.current_selected_widget:
                    pass
                else:
                    obj.setStyleSheet(f"background-color: {self.NORMAL_COLOR}; border-radius: 4px;")

        return super().eventFilter(obj, event)


    # --- 2. 主窗口 Demo 类 (调用公共组件) ---

class DemoMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("纯图标 QMenu 居中+选中样式版 (调用公共组件)")
        self.resize(600, 400)

        self.toolbar = QToolBar(self)
        self.toolbar.setFixedHeight(45)
        self.addToolBar(self.toolbar)

        self.create_buttons()

    # 业务逻辑函数示例
    @Slot(str)
    def handle_zoom_auto(self, action_name: str):
        print(f"🔴 业务逻辑: 设置为 [自动缩放]。")

    @Slot(str)
    def handle_zoom_pan(self, action_name: str):
        print(f"🔴 业务逻辑: 设置为 [仅平移]。")

    @Slot(str)
    def handle_view_grid(self, action_name: str):
        print(f"🟢 业务逻辑: 视图切换到 [显示网格]。")

    @Slot(str)
    def handle_view_label(self, action_name: str):
        print(f"🟢 业务逻辑: 视图切换到 [显示标签]。")


    def create_buttons(self):
        """在 Toolbar 中创建两个独立的 ExclusiveIconMenuButton 实例。"""
        # 占位符路径
        path = r"C:\Users\user1\Pictures\michael图片\npi_graphic\MRA_results\Third"

        # 1. Zoom 控件配置
        configs_zoom = [
            (os.path.join(path, "auto_zoom.png"), "自动缩放", self.handle_zoom_auto),
            (os.path.join(path, "pan_only.png"), "仅平移", self.handle_zoom_pan),
            (os.path.join(path, "no_zoom.png"), "禁止缩放", lambda name: print(f"🔴 业务逻辑: 设置为 [禁止缩放]。"))
        ]

        # 2. 创建第一个菜单按钮 (Zoom Control)
        self.zoom_btn = ExclusiveIconMenuButton(self)
        self.zoom_btn.configure_actions(configs_zoom)
        self.toolbar.addWidget(self.zoom_btn)

        self.toolbar.addSeparator()

        # 3. View 控件配置
        configs_view = [
            (os.path.join(path, "auto_zoom.png"), "显示网格", self.handle_view_grid),
            (os.path.join(path, "pan_only.png"), "显示标签", self.handle_view_label),
        ]

        # 4. 创建第二个菜单按钮 (View Mode)
        self.view_btn = ExclusiveIconMenuButton(self)
        self.view_btn.configure_actions(configs_view)
        self.view_btn.setIcon(QIcon.fromTheme("view-refresh"))
        self.view_btn.setToolTip("视图模式切换") # 初始默认 Tooltip
        self.toolbar.addWidget(self.view_btn)


if __name__ == "__main__":
    QDir.setCurrent(os.path.dirname(os.path.abspath(__file__)))
    app = QApplication(sys.argv)
    window = DemoMainWindow()
    window.show()
    sys.exit(app.exec())