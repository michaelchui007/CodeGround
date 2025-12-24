import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar, QWidget, QVBoxLayout, \
    QPushButton, QToolButton, QStyle
from PySide6.QtCore import Qt, Slot

# 引入您定义的组件
# 确保 checkable_combox.py 在同一目录下
from checkable_combox import CheckableComboBox

class TestMain(QMainWindow):
    def __init__(self):
        super().__init__()

        # 1. 窗口基础设置
        self.setWindowTitle("PySide6 Checkbox Test")
        self.resize(500, 300)
        # 状态标志，仅用于测试数据切换
        self._toggle_state = False
        # 2. 模拟 UI 环境
        # 因为测试环境没有加载 .ui 文件，我们手动创建一个 Toolbar
        self.toolbar = QToolBar("Main Toolbar", self)
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)

        # 3. 初始化 Combobox 逻辑
        self.combo = None
        self.add_combo_to_toolbar()
        # 3. 添加分隔符 (视觉美观)
        self.toolbar.addSeparator()
        # 4. 初始化 更新按钮
        self.add_update_tool_button()

    def get_checklist(self):
        """模拟后端数据接口"""
        # 返回两个列表，用于测试分割线和拼接逻辑
        list1 = ["Apple", "Banana", "Cherry"]
        list2 = ["Dog", "Elephant"]
        return list1, list2

    def add_combo_to_toolbar(self) -> None:
        self.combo = CheckableComboBox()

        # 初始化数据
        list1, list2 = self.get_checklist()
        self.combo.update_data(list1, list2)

        # 连接“单项触发”信号
        self.combo.itemToggled.connect(self.on_single_filter_change)

        # 【模拟】将控件添加到工具栏
        # 在您的实际项目中是 self.ui.toolbarwidget1.addWidget(self.combo)
        self.toolbar.addWidget(self.combo)

    def add_update_tool_button(self) -> None:
        """增加一个更新按钮"""
        update_button = QToolButton()

        # 1. 设置标准图标 (使用 Qt 内置的刷新图标)
        # 也可以加载本地图标: QIcon("path/to/icon.png")
        icon = self.style().standardIcon(QStyle.SP_BrowserReload)
        update_button.setIcon(icon)

        # 2. 设置提示文本 (鼠标悬停时显示)
        update_button.setToolTip("更新列表数据")

        # 3. 连接点击信号 -> 触发更新逻辑
        update_button.clicked.connect(self.on_refresh_clicked)

        self.toolbar.addWidget(update_button)

    def on_refresh_clicked(self):
        """
        槽函数：处理点击更新按钮
        """
        print("--- 正在更新数据 ---")

        # 1. 切换模拟数据状态
        self._toggle_state = not self._toggle_state

        # 2. 再次调用获取数据接口
        new_list1, new_list2 = self.get_checklist()
        print(f"获取到新数据: {new_list1} | {new_list2}")

        # 3. 调用 Combobox 的更新接口
        # 您的 update_data 方法里已经写了 self.model.clear()，所以这里直接调就行，很安全
        self.combo.update_data(new_list1, new_list2)

        print("--- 更新完毕 ---")

    @Slot(int, bool)
    def on_single_filter_change(self, index: int, selected: bool):
        """
        响应用户的每一次点击
        """
        print(f"User Action -> Index: {index}, Selected: {selected}")

        # 模拟调用后端 C++ 接口
        # cpp_backend.update_filter_item(index, selected)


if __name__ == '__main__':
    # 1. 创建 QApplication (Qt 程序的必要核心)
    app = QApplication(sys.argv)

    # 2. 创建并显示主窗口
    window = TestMain()
    window.show()

    # 3. 进入事件循环 (Event Loop)
    # 只有执行了这一步，程序才会响应鼠标点击、重绘等事件
    sys.exit(app.exec())