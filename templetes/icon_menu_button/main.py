# -*- coding: utf-8 -*-
import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar
from PySide6.QtCore import QDir, Slot

# 【关键】导入刚才分离的 Widget 类
# 假设 icon_menu_button.py 在同级目录
from icon_menu_button import ExclusiveIconMenuButton

global_tooltip_qss = """
        QToolTip {
            background-color: white; /* 设置白色背景 */
            color: black;          /* 设置黑色文本，确保可见性 */
            border: 1px solid #C0C0C0; /* 可选：设置一个浅灰色边框 */
            padding: 4px;
            border-radius: 4px;
            opacity: 255; 
        }
        """

class DemoMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("分离式调用 Demo")
        self.resize(600, 400)

        self.toolbar = QToolBar(self)
        self.toolbar.setFixedHeight(45)
        self.addToolBar(self.toolbar)

        # 初始化按钮逻辑
        self.setup_logic()



    # --- 业务逻辑回调函数 ---
    def on_zoom_auto(self, name):
        print(f"执行业务: [自动缩放]")

    def on_zoom_pan(self, name):
        print(f"执行业务: [仅平移]")

    def on_view_grid(self, name):
        print(f"执行业务: [显示网格]")

    def on_view_label(self, name):
        print(f"执行业务: [显示标签]")

    def setup_logic(self):
        # 模拟图标路径 (请根据实际情况修改)
        base_path = r"C:\Users\user1\Pictures\michael图片\npi_graphic\MRA_results\Third"

        # === 按钮 1：Zoom 控制 ===
        # 需求演示：设置了 Action，同时【启用】默认选中高亮
        configs_zoom = [
            (os.path.join(base_path, "auto_zoom.png"), "自动缩放", self.on_zoom_auto),
            (os.path.join(base_path, "pan_only.png"), "仅平移", self.on_zoom_pan),
            (os.path.join(base_path, "no_zoom.png"), "禁止缩放", lambda x: print("禁止缩放")),
        ]

        self.zoom_btn = ExclusiveIconMenuButton(self)
        self.zoom_btn.configure_actions(configs_zoom)

        # 【关键调用】这里调用了 select_first_item()
        # 效果：主图标是第一个，且打开菜单时，第一个项是蓝色的（选中状态）
        self.zoom_btn.select_first_item()

        self.toolbar.addWidget(self.zoom_btn)

        self.toolbar.addSeparator()

        # === 按钮 2：View 控制 ===
        # 需求演示：设置了 Action，但【不调用】select_first_item
        # 效果：主图标是第一个（因为configure_actions里设置了），
        # 但打开菜单时，所有项都是白色的（没有选中状态），直到用户手动点击
        configs_view = [
            (os.path.join(base_path, "auto_zoom.png"), "显示网格", self.on_view_grid),
            (os.path.join(base_path, "pan_only.png"), "显示标签", self.on_view_label),
        ]

        self.view_btn = ExclusiveIconMenuButton(self)
        self.view_btn.configure_actions(configs_view)
        # 注意：这里没有调用 select_first_item()

        self.toolbar.addWidget(self.view_btn)

if __name__ == "__main__":
    QDir.setCurrent(os.path.dirname(os.path.abspath(__file__)))
    app = QApplication(sys.argv)
    app.setStyleSheet(global_tooltip_qss)
    window = DemoMainWindow()
    window.show()
    sys.exit(app.exec())