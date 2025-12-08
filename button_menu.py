from PySide6.QtWidgets import (QApplication, QWidget, QToolBar, QToolButton,
                               QMenu, QVBoxLayout)
from PySide6.QtCore import Qt

class PopupModeDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("QToolButton 弹出模式对比")
        self.resize(600, 200)

        layout = QVBoxLayout(self)

        # 1. DelayedPopup 模式（长按弹出）
        toolbar1 = QToolBar("DelayedPopup 模式")
        btn1 = QToolButton()
        btn1.setText("长按弹出")
        btn1.setPopupMode(QToolButton.DelayedPopup)
        self.add_menu(btn1)
        btn1.clicked.connect(lambda: print("DelayedPopup：单击不会触发"))
        toolbar1.addWidget(btn1)

        # 2. InstantPopup 模式（单击立即弹出，无默认命令）
        toolbar2 = QToolBar("InstantPopup 模式")
        btn2 = QToolButton()
        btn2.setText("单击弹出")
        btn2.setPopupMode(QToolButton.InstantPopup)
        self.add_menu(btn2)
        btn2.clicked.connect(lambda: print("InstantPopup：不会触发（只弹菜单）"))  # 这句不会执行
        toolbar2.addWidget(btn2)

        # 3. MenuButtonPopup 模式（图标+箭头分离）
        toolbar3 = QToolBar("MenuButtonPopup 模式")
        btn3 = QToolButton()
        btn3.setText("图标+箭头")
        btn3.setPopupMode(QToolButton.MenuButtonPopup)  # 显示箭头
        self.add_menu(btn3)
        btn3.clicked.connect(lambda: print("MenuButtonPopup：单击图标触发默认命令"))
        toolbar3.addWidget(btn3)

        # 添加到布局
        layout.addWidget(toolbar1)
        layout.addWidget(toolbar2)
        layout.addWidget(toolbar3)

    def add_menu(self, btn):
        """给按钮添加测试菜单"""
        menu = QMenu()
        menu.addAction("选项1", lambda: print("选中选项1"))
        menu.addAction("选项2", lambda: print("选中选项2"))
        btn.setMenu(menu)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = PopupModeDemo()
    window.show()
    sys.exit(app.exec())