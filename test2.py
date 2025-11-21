# -*- coding: utf-8 -*-
"""
直接用 QPushButton 承载图片（100% 填充按钮）
功能：图片充满 177×22 按钮，点击打印信息
"""
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PySide6.QtGui import QPixmap, QPalette
from PySide6.QtCore import Qt

class ImageButtonDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("图片按钮最终生效版")
        self.resize(400, 300)

        # 1. 窗口加布局（确保按钮正常显示）
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setAlignment(Qt.AlignTop)  # 按钮靠顶部显示（模拟 ToolBar 位置）

        # 2. 创建 QPushButton（直接承载图片，比 QToolButton 更稳定）
        self.image_btn = QPushButton(self)
        # 按钮固定尺寸（你的需求：177×22）
        self.image_btn.setFixedSize(177, 22)
        # 去掉按钮边框（可选，更像纯图片按钮）
        self.image_btn.setStyleSheet("border: none;")
        self.image_btn.setToolTip("点击自动缩放图片")

        # 3. 加载图片并设置为按钮背景（强制填充）
        icon_path = ("C:/Users/user1/Pictures/michael图片/npi_graphic"
                     "/MRA_results/select_box.png")
        self.set_button_background(icon_path)

        # 4. 绑定点击事件
        self.image_btn.clicked.connect(self.on_button_click)

        # 5. 按钮加入布局
        main_layout.addWidget(self.image_btn)

    def set_button_background(self, image_path):
        """设置图片为按钮背景，强制填充整个按钮"""
        # 加载图片
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            print(f"警告：图片路径错误，无法加载图片！路径：{image_path}")
            return

        # 缩放图片到按钮尺寸（强制拉伸填充）
        scaled_pixmap = pixmap.scaled(
            self.image_btn.size(),
            Qt.IgnoreAspectRatio,  # 忽略宽高比，完全填充
            Qt.SmoothTransformation  # 平滑缩放，画质不模糊
        )

        # 设置为按钮背景
        palette = self.image_btn.palette()
        # 背景图片居中、不重复、拉伸填充
        palette.setBrush(QPalette.Button, scaled_pixmap)
        self.image_btn.setPalette(palette)
        # 取消按钮文本（纯图片按钮）
        self.image_btn.setText("")
        # 确保背景图片随按钮尺寸变化
        self.image_btn.setAutoFillBackground(True)

    def on_button_click(self):
        print("图片按钮被点击了！")

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = ImageButtonDemo()
    window.show()
    sys.exit(app.exec())