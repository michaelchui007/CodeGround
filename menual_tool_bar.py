from PySide6.QtWidgets import (
    QWidget, QApplication, QToolBar, QAction, QHBoxLayout, QFrame
)
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QIcon
from ui_your_file import Ui_Form  # 替换为你的 UI 转换文件名
import os
import sys

class MainView(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)  # 加载 Designer 中的 UI（含 toolbarWidget 和 mapWidget）

        # 关键：给 toolbarWidget 设置水平布局（让图标按钮水平排列）
        self._setup_toolbar_layout()

        # 往 toolbarWidget 中添加 5 个图标 + Action + 分隔线
        self._add_toolbar_actions()

    def _setup_toolbar_layout(self):
        """给 toolbarWidget 设置水平布局，避免图标重叠"""
        # 创建水平布局
        toolbar_layout = QHBoxLayout(self.toolbarWidget)
        toolbar_layout.setContentsMargins(4, 4, 4, 4)  # 内边距（上下左右 4px）
        toolbar_layout.setSpacing(8)  # 按钮之间的间距

    def _add_toolbar_actions(self):
        """创建 5 个图标按钮 + 分隔线，添加到 toolbarWidget"""
        # 1. 创建 ToolBar（绑定到 toolbarWidget）
        self.toolbar = QToolBar("功能工具栏", self.toolbarWidget)
        # 配置 ToolBar 属性
        self.toolbar.setIconSize(Qt.QSize(24, 24))  # 图标尺寸
        self.toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)  # 图标+文本
        self.toolbar.setFloatable(False)  # 禁止浮动
        self.toolbar.setMovable(False)    # 禁止拖动
        # 隐藏 ToolBar 边框（融入 toolbarWidget）
        self.toolbar.setStyleSheet("""
            QToolBar {
                border: none;  /* 取消边框，避免和 toolbarWidget 重复 */
            }
            QToolButton {
                border-radius: 4px;
                padding: 4px 8px;
            }
            QToolButton:hover {
                background-color: #e9ecef;
            }
            QToolButton:pressed {
                background-color: #dee2e6;
            }
            QToolBar::separator {
                background-color: #dee2e6;
                width: 1px;
                margin: 4px 8px;
            }
        """)

        # 2. 加载 5 个图标（替换为你的图标路径）
        icon_dir = os.path.join(os.path.dirname(__file__), "../icons")  # 图标文件夹路径
        icon_info = [
            ("icon1.png", "功能1", "action1"),  # 图标文件、按钮文本、Action 名称
            ("icon2.png", "功能2", "action2"),
            ("icon3.png", "功能3", "action3"),
            ("icon4.png", "功能4", "action4"),
            ("icon5.png", "功能5", "action5")
        ]

        # 3. 创建 Action 并添加到 ToolBar（含分隔线）
        self.toolbar_actions = {}  # 存储 Action，便于后续操作
        for i, (icon_file, text, action_name) in enumerate(icon_info):
            # 拼接图标路径
            icon_path = os.path.join(icon_dir, icon_file)
            # 验证路径（避免图标加载失败）
            if not os.path.exists(icon_path):
                print(f"警告：图标文件不存在 → {icon_path}")
                icon = QIcon()  # 空图标
            else:
                icon = QIcon(icon_path)

            # 创建 Action
            action = QAction(icon, text, self)
            action.setObjectName(action_name)
            self.toolbar_actions[action_name] = action

            # 关键：前3个按钮后插入分隔线（第4个按钮前）
            if i == 3:  # 索引3对应第4个按钮
                self.toolbar.addSeparator()

            # 添加 Action 到 ToolBar
            self.toolbar.addAction(action)

        # 4. 将 ToolBar 加入 toolbarWidget 的水平布局
        self.toolbarWidget.layout().addWidget(self.toolbar)

        # 5. 绑定 Action 点击事件
        self._bind_actions()

    def _bind_actions(self):
        """绑定 5 个 Action 的点击事件"""
        self.toolbar_actions["action1"].triggered.connect(self._on_action1)
        self.toolbar_actions["action2"].triggered.connect(self._on_action2)
        self.toolbar_actions["action3"].triggered.connect(self._on_action3)
        self.toolbar_actions["action4"].triggered.connect(self._on_action4)
        self.toolbar_actions["action5"].triggered.connect(self._on_action5)

    # ------------------- 业务逻辑（按需修改）-------------------
    @Slot()
    def _on_action1(self):
        print("触发功能1（比如添加标记）")
        # 可操作 mapWidget：self.mapWidget.xxx（比如在地图上添加标记）

    @Slot()
    def _on_action2(self):
        print("触发功能2（比如删除标记）")

    @Slot()
    def _on_action3(self):
        print("触发功能3（比如放大地图）")

    @Slot()
    def _on_action4(self):
        print("触发功能4（比如缩小地图）")

    @Slot()
    def _on_action5(self):
        print("触发功能5（比如刷新地图）")

# 测试
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainView()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())

QFrame