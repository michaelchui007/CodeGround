# -*- coding: utf-8 -*-
"""
极简版 QToolBar 图标按钮点击 Demo
功能：仅 1 个图标按钮，点击打印信息，零兼容问题
"""
from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar, QWidget, \
    QToolButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize


class ToolBarMinimalDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 窗口基础设置
        self.setWindowTitle("极简图标按钮 Demo")
        self.resize(400, 300)

        # 1. 创建 ToolBar
        toolbar = QToolBar(self)
        toolbar.setIconSize(QSize(24, 24))  # 图标尺寸


        # 2. 创建图标（用 PySide6 内置图标，零依赖）
        # 方式：直接用 Qt 内置颜色图标（100% 兼容所有平台）
        icon_path = ("C:/Users/user1/Pictures/michael图片/npi_graphic"
                     "/MRA_results/select_box.png")
        icon = QIcon(icon_path)  # 信息图标（跨平台支持）

        select_btn = QToolButton()
        select_btn.setIcon(icon)
        select_btn.setIconSize(QSize(177, 22))
        select_btn.setFixedSize(177, 22)
        select_btn.setToolTip("点击自动缩放图片")
        toolbar.addWidget(select_btn)


        # 3. 创建 Action 并添加到 ToolBar
        # action = toolbar.addAction(icon, "")  # 无文本，仅图标

        # 4. 绑定点击事件（点击打印信息）
        select_btn.clicked.connect(self.on_button_click)

    def on_button_click(self):
        # 点击后仅打印信息
        print("图标按钮被点击了！")

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = ToolBarMinimalDemo()
    window.show()
    sys.exit(app.exec())