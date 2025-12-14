# -*- coding: utf-8 -*-
"""
居中图标 + 恢复鼠标悬停选中样式 + 选中状态持久化
"""
import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QToolBar, QToolButton,
                               QMenu, QWidgetAction, QLabel, QWidget, QHBoxLayout)
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt, QSize, QDir, QEvent, Slot
# 引入 functools.partial 用于安全的信号连接
from functools import partial


class PureIconMenuCustomDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        # 【新增】存储当前被选中的 QWidget 实例
        self.current_selected_widget = None
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
        # 使用 MenuButtonPopup 模式，如果需要整个按钮点击弹出菜单，请改为 InstantPopup
        self.tool_btn.setPopupMode(QToolButton.MenuButtonPopup)

        self.menu = QMenu(self.tool_btn)
        self.ICON_SIZE = QSize(24, 24)    # 图标尺寸
        self.ITEM_SIZE = QSize(32, 32)    # 菜单项尺寸
        self.SELECT_COLOR = "#188db1"     # 选中背景色
        self.NORMAL_COLOR = "white"       # 正常背景色
        self.set_menu_style()
        self.add_custom_menu_actions() # 移除参数

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

            /* 【修正点】禁用 QMenu 默认的选中背景色，完全依赖 QWidgetAction 中的自定义样式 */
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

            QLabel {{
                margin: 0px;
                padding: 0px;
            }}
        """
        self.menu.setStyleSheet(menu_qss)

    def set_action_selected(self, action_widget: QWidget):
        """
        设置指定的 action_widget 为选中状态（高亮），并清除之前的选中状态。

        Args:
            action_widget: 要设置高亮的自定义 QWidget 实例。
        """
        # 1. 清除旧的高亮状态
        if self.current_selected_widget and self.current_selected_widget != action_widget:
            self.current_selected_widget.setStyleSheet(
                f"background-color: {self.NORMAL_COLOR}; border-radius: 4px;"
            )

        # 2. 设置新的高亮状态
        action_widget.setStyleSheet(
            f"background-color: {self.SELECT_COLOR}; border-radius: 4px;"
        )

        # 3. 更新状态变量
        self.current_selected_widget = action_widget

        # 4. (可选) 关闭菜单
        # self.menu.hide()

    # 【新增槽函数】处理 Action 点击并调用高亮设置
    def handle_action_click(self, action_widget: QWidget, tooltip: str, checked: bool = False):
        """
        处理 QWidgetAction 被触发的点击事件，并管理选中状态。
        """
        print(f"✅ 点击功能：{tooltip}")

        # 调用状态管理函数
        self.set_action_selected(action_widget)

        # 【关键】执行实际业务功能
        self.action_func(tooltip)

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
                try:
                    pixmap = QPixmap(icon_path)
                    pixmap = pixmap.scaled(self.ICON_SIZE, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    icon = QIcon(pixmap)
                except Exception:
                    print(f"⚠️  警告：图标加载失败 → {icon_path}")
                    icon = QIcon.fromTheme("image-1")

            # 2. 创建自定义widget（带悬停事件）
            item_widget = self.create_hover_widget(icon, tooltip)

            # 3. 创建QWidgetAction
            widget_action = QWidgetAction(self.menu)
            widget_action.setDefaultWidget(item_widget)
            widget_action.setToolTip(tooltip)

            # 4. 【修正点】使用 functools.partial 绑定，将 item_widget 和 tooltip 传给 handle_action_click
            widget_action.triggered.connect(partial(self.handle_action_click, item_widget, tooltip))

            self.menu.addAction(widget_action)

            # 【新增】设置默认选中状态（可选：选中第一个）
            if self.current_selected_widget is None:
                self.set_action_selected(item_widget)

    @Slot(str)
    def action_func(self, tool_tip: str):
        """实际执行业务逻辑的方法"""
        print(f"📢 业务逻辑执行: {tool_tip}")

    def create_hover_widget(self, icon, tooltip):
        """创建带鼠标悬停效果的widget（核心：恢复选中样式）"""
        widget = QWidget()
        widget.setFixedSize(self.ITEM_SIZE)
        widget.setToolTip(tooltip)

        # 初始样式在 set_action_selected 中设置，这里确保其为普通背景色
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
        """事件过滤器：监听widget的鼠标悬停/离开事件，并保护选中状态"""
        # 只处理 QWidget 实例 (即菜单项)
        if isinstance(obj, QWidget):

            if event.type() == QEvent.Enter:
                # 鼠标进入：设置悬停高亮
                obj.setStyleSheet(f"background-color: {self.SELECT_COLOR}; border-radius: 4px;")

            elif event.type() == QEvent.Leave:
                # 鼠标离开：

                # 【修正点】如果该 widget 是当前选中的，则保留选中颜色，否则恢复正常颜色
                if obj == self.current_selected_widget:
                    # 保持 SELECT_COLOR，不进行操作
                    pass
                else:
                    # 恢复正常背景色
                    obj.setStyleSheet(f"background-color: {self.NORMAL_COLOR}; border-radius: 4px;")

        # 必须返回 super().eventFilter 确保事件继续传递
        return super().eventFilter(obj, event)

if __name__ == "__main__":
    QDir.setCurrent(os.path.dirname(os.path.abspath(__file__)))
    app = QApplication(sys.argv)
    window = PureIconMenuCustomDemo()
    window.show()
    sys.exit(app.exec())