import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QListWidget,
                               QListWidgetItem, QWidget, QVBoxLayout)
from PySide6.QtCore import Qt  # PySide6 中 Qt 常量从 QtCore 导入


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Qt.UserRole 基础用法")
        self.resize(400, 300)

        # 1. 创建 QListWidget 控件
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)
        self.setCentralWidget(central_widget)

        # 2. 给列表项绑定数据（显示文本 + 自定义数据）
        for i in range(1, 6):  # 创建 5 个列表项
            item = QListWidgetItem(f"Item {i}")  # 显示文本（用户可见）

            # 绑定自定义数据：Qt.UserRole 存 ID，Qt.UserRole+1 存用户名
            item.setData(Qt.UserRole, i)  # 数据1：ID（整数）
            item.setData(Qt.UserRole + 1, f"Qter {i}")  # 数据2：用户名（字符串）

            self.list_widget.addItem(item)

        # 3. 绑定点击事件：点击项时获取自定义数据
        self.list_widget.itemClicked.connect(self.on_item_clicked)

    def on_item_clicked(self, item):
        """点击列表项时，获取绑定的自定义数据"""
        item_id = item.data(Qt.UserRole)  # 获取 ID
        item_name = item.data(Qt.UserRole + 1)  # 获取用户名
        # 打印结果
        print("-" * 20)
        print(f"点击前")
        print(f"UserRole（ID）: {item_id}")
        print(f"UserRole+1（用户名）: {item_name}")
        item.setData(Qt.UserRole, item_id)
        print(f"点击前")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())  # PySide6 中 app.exec() 与 PyQt5 一致（部分旧版本用 exec_()，现统一为 exec()）