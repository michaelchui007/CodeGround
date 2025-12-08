import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMenu, QPushButton, QVBoxLayout, QWidget
)
# 核心改动：QAction 必须从 QtGui 导入！
from PySide6.QtGui import QAction
from PySide6.QtCore import Slot


class DynamicMenuDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 动态二级菜单 Demo")
        self.resize(500, 300)

        # 模拟应用当前可删除的项列表
        self.available_items = ["Analysis A", "Assembly X"]

        # 1. 初始化菜单栏
        self._setup_menu_bar()

        # 2. 设置中央 Widget 和数据刷新按钮
        self._setup_ui()

    def _setup_menu_bar(self):
        menu_bar = self.menuBar()

        # 1. 创建顶级菜单 Results
        menu_results = menu_bar.addMenu("&Results")

        # 2. 创建二级菜单 'Delete Checklist and Results'
        # 这依然是一个 QMenu 实例
        menu_delete = menu_results.addMenu("Delete Checklist and Results")

        # 3. 【修正点 1】不再创建额外的 QMenu 实例，直接使用 menu_delete 作为动态菜单的容器
        self.dynamic_submenu = menu_delete # <-- 将引用指向同一个 QMenu 实例

        # 初始时加载菜单内容
        self.refresh_dynamic_menu()

    def _setup_ui(self):
        """设置界面，用于模拟外部数据源变化"""
        container = QWidget()
        layout = QVBoxLayout(container)

        # 按钮：模拟数据源新增项
        add_btn = QPushButton("模拟：新增 'Test Data'")
        add_btn.clicked.connect(self._simulate_data_change)
        layout.addWidget(add_btn)

        # 按钮：模拟数据源清空
        clear_btn = QPushButton("模拟：清空所有数据")
        clear_btn.clicked.connect(self._simulate_data_clear)
        layout.addWidget(clear_btn)

        self.setCentralWidget(container)

    @Slot()
    def _simulate_data_change(self):
        """模拟外部系统更新数据"""
        new_item = f"Test Data {len(self.available_items) - 1}"
        self.available_items.append(new_item)
        print(f"\n--- 数据源新增: '{new_item}' ---")
        self.refresh_dynamic_menu() # 数据变化后，立即刷新菜单

    @Slot()
    def _simulate_data_clear(self):
        """模拟清空数据"""
        self.available_items = []
        print("\n--- 数据源已清空 ---")
        self.refresh_dynamic_menu() # 数据变化后，立即刷新菜单

    @Slot(str)
    def handle_delete_item(self, item_name):
        """
        槽函数：处理用户点击动态菜单项的事件
        """
        print(f"\n✅ 成功处理删除请求: {item_name}")
        # 实际业务中，这里会调用你的后端逻辑，执行删除操作，
        # 然后你需要从 self.available_items 中移除该项并再次调用 self.refresh_dynamic_menu() 刷新。

    def refresh_dynamic_menu(self):
        """
        核心逻辑：清空旧 Action，根据当前数据重新生成 Action
        """

        # 1. 【关键步骤】清空所有旧的 QAction
        self.dynamic_submenu.clear()
        print(f"菜单清空完毕，准备加载 {len(self.available_items)} 个新项。")

        if not self.available_items:
            # 如果没有数据，添加一个不可用的提示 Action
            no_data_action = QAction("（没有可删除的项）", self)
            no_data_action.setEnabled(False)
            self.dynamic_submenu.addAction(no_data_action)
            return

        # 2. 遍历数据源，创建并连接新的 Action
        for item in self.available_items:
            action = QAction(item, self)

            # 3. 【关键步骤】使用 lambda 传递参数
            # 必须使用 item=item 这种方式捕获循环变量，
            # 否则所有 Action 都会触发并传递最后一次循环的 item 值。
            action.triggered.connect(lambda checked, name=item: self.handle_delete_item(name))

            self.dynamic_submenu.addAction(action)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DynamicMenuDemo()
    window.show()
    sys.exit(app.exec())