# -*- coding: utf-8 -*-
import os
from functools import partial
from typing import List, Tuple, Callable, Dict, Optional

from PySide6.QtCore import Qt, QSize, QEvent, Signal, Slot
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (QToolButton, QMenu, QWidgetAction,
                               QLabel, QWidget, QHBoxLayout)

class ExclusiveIconMenuButton(QToolButton):
    """
    自定义组件：带下拉菜单的图标按钮。
    特点：
    1. 菜单项互斥高亮。
    2. 主按钮图标跟随选中项变化。
    3. 支持业务逻辑回调注入。
    """
    action_triggered = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        # 状态管理
        self.current_selected_widget: Optional[QWidget] = None
        self._action_callbacks: Dict[QWidget, Callable] = {}
        self._action_icons: Dict[QWidget, QIcon] = {}
        self._action_tooltips: Dict[QWidget, str] = {}

        # 常量配置
        self.ICON_SIZE = QSize(24, 24)
        self.ITEM_SIZE = QSize(32, 32)
        self.SELECT_COLOR = "#188db1"
        self.NORMAL_COLOR = "white"

        # UI 初始化
        self.menu = QMenu(self)
        self.setMenu(self.menu)
        self._init_menu_style()

        # self.setFixedSize(45, 45)
        self.setIconSize(QSize(26, 26))
        self.setPopupMode(QToolButton.MenuButtonPopup)

        self.clicked.connect(self._on_main_button_clicked)

    def _init_menu_style(self):
        """设置菜单样式"""
        menu_qss = f"""
            QMenu::item {{
                padding: 0px; margin: 0px;
                min-height: {self.ITEM_SIZE.height()}px;
                min-width: {self.ITEM_SIZE.width()}px;
            }}
            QMenu::item:selected {{
                background-color: transparent; border: 0px;
            }}
            QMenu {{
                padding: 3px; border: 1px solid #dddddd;
                border-radius: 6px; background-color: white;
            }}
            QToolTip {{
                border: 1px solid #76797C; background-color: #262626; 
                color: white; padding: 4px; border-radius: 4px; opacity: 255; 
            }}
        """
        self.menu.setStyleSheet(menu_qss)

    def configure_actions(self, configs: List[Tuple[str, str, Callable]]):
        """
        配置菜单项。
        逻辑：配置完成后，主按钮图标默认显示为第一个项，但菜单内部不显示高亮选中。
        """
        for icon_path, tooltip, callback in configs:
            icon = self._load_icon(icon_path)
            item_widget = self._create_hover_widget(icon, tooltip)

            widget_action = QWidgetAction(self.menu)
            widget_action.setDefaultWidget(item_widget)
            widget_action.setToolTip(tooltip)

            # 存储数据
            self._action_callbacks[item_widget] = callback
            self._action_icons[item_widget] = icon
            self._action_tooltips[item_widget] = tooltip

            # 绑定点击
            widget_action.triggered.connect(partial(self.handle_action_click, item_widget))


            self.menu.addAction(widget_action)

        # 【核心修改】：初始化时，只替换外面的主图标和Tooltip，不触发内部选中高亮
        if self.menu.actions():
            first_widget = self.menu.actions()[0].defaultWidget()
            if first_widget:
                # 手动设置主按钮外观
                initial_icon = self._action_icons.get(first_widget)
                initial_tip = self._action_tooltips.get(first_widget)
                if initial_icon: self.setIcon(initial_icon)
                if initial_tip: self.setToolTip(initial_tip)

    def select_first_item(self):
        """
        【单独接口】：调用此方法后，将菜单中的第一个项设置为默认选中（高亮）状态。
        """
        if self.menu.actions():
            first_widget = self.menu.actions()[0].defaultWidget()
            if first_widget:
                self.set_action_selected(first_widget)

    def set_action_selected(self, action_widget: QWidget):
        """设置指定项为高亮选中，并同步更新外部图标"""
        # 1. 清除旧高亮
        if self.current_selected_widget and self.current_selected_widget != action_widget:
            self.current_selected_widget.setStyleSheet(
                f"background-color: {self.NORMAL_COLOR}; border-radius: 4px;"
            )

        # 2. 设置新高亮
        action_widget.setStyleSheet(
            f"background-color: {self.SELECT_COLOR}; border-radius: 4px;"
        )

        # 3. 同步外部图标和Tooltip
        selected_icon = self._action_icons.get(action_widget)
        selected_tooltip = self._action_tooltips.get(action_widget)

        if selected_icon: self.setIcon(selected_icon)
        if selected_tooltip: self.setToolTip(selected_tooltip)

        # 4. 更新状态
        self.current_selected_widget = action_widget
        self.menu.hide()

    def handle_action_click(self, action_widget: QWidget, checked: bool = False):
        """处理点击事件"""
        # 1. 设置选中状态
        self.set_action_selected(action_widget)

        # 2. 执行回调
        callback = self._action_callbacks.get(action_widget)
        tooltip = action_widget.toolTip()

        if callback:
            callback(tooltip)

        self.action_triggered.emit(tooltip)

    def _load_icon(self, icon_path: str) -> QIcon:
        if not os.path.exists(icon_path):
            return QIcon.fromTheme("image-1")
        pixmap = QPixmap(icon_path)
        if pixmap.isNull():
            return QIcon.fromTheme("image-1")
        return QIcon(pixmap.scaled(self.ICON_SIZE, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def _create_hover_widget(self, icon: QIcon, tooltip: str) -> QWidget:
        widget = QWidget()
        widget.setFixedSize(self.ITEM_SIZE)
        widget.setToolTip(tooltip)
        widget.setStyleSheet(f"background-color: {self.NORMAL_COLOR}; border-radius: 4px;")
        widget.installEventFilter(self)

        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)

        label = QLabel()
        label.setPixmap(icon.pixmap(self.ICON_SIZE))
        layout.addWidget(label)
        return widget

    def eventFilter(self, obj, event):
        if isinstance(obj, QWidget):
            if event.type() == QEvent.Enter:
                obj.setStyleSheet(f"background-color: {self.SELECT_COLOR}; border-radius: 4px;")
            elif event.type() == QEvent.Leave:
                if obj == self.current_selected_widget:
                    pass
                else:
                    obj.setStyleSheet(f"background-color: {self.NORMAL_COLOR}; border-radius: 4px;")
        return super().eventFilter(obj, event)

    @Slot()
    def _on_main_button_clicked(self):
        """
        处理主按钮区域的点击事件
        """
        target_widget = self.current_selected_widget

        # 如果当前没有选中项（例如：view_btn 未调用 select_first_item），
        # 但菜单列表不为空，且主按钮显示的是第一个图标，
        # 则点击主按钮时默认触发第一个项的逻辑（所见即所得）。
        if target_widget is None and self.menu.actions():
            first_action = self.menu.actions()[0]
            target_widget = first_action.defaultWidget()

        if target_widget:
            # 复用 handle_action_click，它会负责执行回调、发射信号并更新选中状态
            self.handle_action_click(target_widget)