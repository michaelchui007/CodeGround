# -*- coding: utf-8 -*-
"""
居中图标 + 恢复鼠标悬停选中样式
"""
import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QToolBar, QToolButton,
                               QMenu, QWidgetAction, QLabel, QWidget, QHBoxLayout)
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt, QSize, QDir, QEvent

class PureIconMenuCustomDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("纯图标 QMenu 居中+选中样式版")
        self.resize(600, 400)

        self.toolbar = QToolBar(self)
        self.toolbar.setFixedHeight(45)
        self.addToolBar(self.toolbar)

        self.create_tool_button()

    def create_tool_button(self):
        self.tool_btn = QToolButton()
        self.tool_btn.setFixedSize(45, 45)
        self.tool_btn.setIconSize(QSize(28, 28))
        self.tool_btn.setIcon(QIcon.fromTheme("edit-select"))
        self.tool_btn.setPopupMode(QToolButton.MenuButtonPopup)

        self.menu = QMenu(self.tool_btn)
        self.ICON_SIZE = QSize(24, 24)    # 图标尺寸
        self.ITEM_SIZE = QSize(32, 32)    # 菜单项尺寸
        self.SELECT_COLOR = "#188db1"     # 选中背景色
        self.NORMAL_COLOR = "white"       # 正常背景色
        self.set_menu_style()
        self.add_custom_menu_actions()

        self.tool_btn.setMenu(self.menu)
        self.toolbar.addWidget(self.tool_btn)

    def set_menu_style(self):
        """基础样式（取消默认干扰，聚焦自定义widget）"""
        menu_qss = f"""
            QMenu::item {{
                padding: 0px;
                margin: 0px;
                min-height: {self.ITEM_SIZE.height()}px;
                min-width: {self.ITEM_SIZE.width()}px;
            }}

            QMenu {{
                padding: 3px;
                border: 1px solid #dddddd;
                border-radius: 6px;
                background-color: white;
            }}

            QLabel {{
                margin: 0px;
                padding: 0px;
            }}
        """
        self.menu.setStyleSheet(menu_qss)

    def add_custom_menu_actions(self):
        """添加带选中样式的居中图标"""
        icon_paths = [
            r"C:\Users\user1\Pictures\michael图片\npi_graphic\MRA_results\Third\auto_zoom.png",
            r"C:\Users\user1\Pictures\michael图片\npi_graphic\MRA_results\Third\pan_only.png",
            r"C:\Users\user1\Pictures\michael图片\npi_graphic\MRA_results\Third\no_zoom.png"
        ]
        tooltips = ["自动缩放", "仅平移", "禁止缩放"]

        for icon_path, tooltip in zip(icon_paths, tooltips):
            # 1. 加载图标
            if not os.path.exists(icon_path):
                print(f"⚠️  警告：图标路径不存在 → {icon_path}")
                icon = QIcon.fromTheme("image-1")
            else:
                pixmap = QPixmap(icon_path)
                if pixmap.isNull():
                    print(f"⚠️  警告：图标加载失败 → {icon_path}")
                    icon = QIcon.fromTheme("image-1")
                else:
                    pixmap = pixmap.scaled(self.ICON_SIZE, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    icon = QIcon(pixmap)

            # 2. 创建自定义widget（带悬停事件）
            item_widget = self.create_hover_widget(icon, tooltip)

            # 3. 创建QWidgetAction
            widget_action = QWidgetAction(self.menu)
            widget_action.setDefaultWidget(item_widget)
            widget_action.setToolTip(tooltip)

            # 绑定点击事件
            widget_action.triggered.connect(lambda _, t=tooltip: print(f"✅ 点击功能：{t}"))

            self.menu.addAction(widget_action)

    def create_hover_widget(self, icon, tooltip):
        """创建带鼠标悬停效果的widget（核心：恢复选中样式）"""
        widget = QWidget()
        widget.setFixedSize(self.ITEM_SIZE)
        widget.setToolTip(tooltip)
        widget.setStyleSheet(f"background-color: {self.NORMAL_COLOR}; border-radius: 4px;")

        # 绑定鼠标悬停/离开事件
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

    def eventFilter(self, obj, event):
        """事件过滤器：监听widget的鼠标悬停/离开事件"""
        # 只处理菜单项的widget
        if obj.parent() == self.menu or (obj.parent() and obj.parent().parent() == self.menu):
            if event.type() == QEvent.Enter:
                # 鼠标进入：设置选中背景色
                obj.setStyleSheet(f"background-color: {self.SELECT_COLOR}; border-radius: 4px;")
            elif event.type() == QEvent.Leave:
                # 鼠标离开：恢复正常背景色
                obj.setStyleSheet(f"background-color: {self.NORMAL_COLOR}; border-radius: 4px;")
        return super().eventFilter(obj, event)

if __name__ == "__main__":
    QDir.setCurrent(os.path.dirname(os.path.abspath(__file__)))
    app = QApplication(sys.argv)
    window = PureIconMenuCustomDemo()
    window.show()
    sys.exit(app.exec())