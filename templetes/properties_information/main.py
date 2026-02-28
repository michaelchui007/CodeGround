import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel,
                               QTextEdit, QSpacerItem, QSizePolicy, QPushButton, QHBoxLayout)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

# ============================================================================
# 1. 核心组件封装：FeatureInfoWidget
# ============================================================================
class FeatureInfoWidget(QWidget):
    """
    这是你要集成到项目中的核心 Widget。
    它自包含布局、样式和自适应逻辑。
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        # 1. 设置窗口基本属性
        self.setWindowTitle("Feature Information")
        self.resize(350, 600)

        # 2. 初始化布局 (设置为顶级布局)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(10)
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        # 3. 初始化控件列表
        self.display_widgets = []

        # 4. 循环创建 4 组 标题+内容
        # 这样写比 UI 文件更灵活，以后要加第 5 组改数字就行
        for i in range(4):
            # 标题
            lbl = QLabel()
            lbl.setFont(QFont("Arial", 10, QFont.Bold))
            self.main_layout.addWidget(lbl)
            self.display_widgets.append(lbl)

            # 内容框
            txt = QTextEdit()
            txt.setReadOnly(True)
            txt.setFont(QFont("Courier New", 10)) # 等宽字体
            txt.setFrameShape(QTextEdit.NoFrame)  # 可选：去掉边框让它看起来更像纯文本
            # 这里的策略是：垂直方向尽可能压扁(Maximum)，依靠内容撑开
            txt.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
            self.main_layout.addWidget(txt)
            self.display_widgets.append(txt)

        # 5. 【关键】添加底部弹簧
        # 这会将所有控件顶上去，防止最后一个控件莫名其妙被拉长
        self.spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.main_layout.addItem(self.spacer)

    def update_content(self, data_list):
        """外部调用的接口，传入字符串列表"""
        if len(data_list) != 8:
            print("Error: Data list length must be 8")
            return

        for i, text in enumerate(data_list):
            widget = self.display_widgets[i]

            if isinstance(widget, QLabel):
                widget.setText(text)
            elif isinstance(widget, QTextEdit):
                widget.setPlainText(text)
                # 内容更新后，立即计算高度
                self.adjust_height(widget)

    def adjust_height(self, text_edit):
        """根据内容自动调整 TextEdit 高度"""
        doc = text_edit.document()
        layout = doc.documentLayout()
        layout.setPaintDevice(text_edit.viewport())

        # 1. 强制设定宽度计算高度
        doc.setTextWidth(text_edit.viewport().width())
        doc_height = doc.size().height()

        # 2. 边距补偿
        # 如果去掉了边框(NoFrame)，margin 可以设小一点
        total_height = int(doc_height + 10)

        # 3. 高度策略
        # 如果内容少于 150px，完全自适应（不显示滚动条）
        if total_height < 150:
            text_edit.setFixedHeight(total_height)
            text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        else:
            # 内容太多，给个限制，出滚动条
            text_edit.setFixedHeight(200) # 或者使用 setMinimumHeight(100) + setMaximumHeight(300)
            text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    def resizeEvent(self, event):
        """窗口大小改变时，重新计算高度（处理换行变化）"""
        super().resizeEvent(event)
        for widget in self.display_widgets:
            if isinstance(widget, QTextEdit):
                self.adjust_height(widget)

    # 模拟 Close 事件，方便你调试
    def closeEvent(self, event):
        print("FeatureInfoWidget: 检测到关闭事件，资源已释放 (模拟)")
        super().closeEvent(event)


# ============================================================================
# 2. 调试控制台：DebugControlWindow
# ============================================================================
class DebugControlWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Debugger Console")
        self.resize(300, 200)
        self.move(100, 100) # 让它出现在屏幕左侧

        layout = QVBoxLayout(self)

        # 实例化我们要测试的 Widget
        # 注意：这里没有给 parent，意味着它是独立的顶级窗口（Floating Window）
        self.target_widget = FeatureInfoWidget()

        # 按钮 1: 显示
        self.btn_show = QPushButton("1. Show Widget")
        self.btn_show.clicked.connect(self.on_show_clicked)
        layout.addWidget(self.btn_show)

        # 按钮 2: 更新数据 (短)
        self.btn_data_short = QPushButton("2. Load Short Data")
        self.btn_data_short.clicked.connect(self.load_short_data)
        layout.addWidget(self.btn_data_short)

        # 按钮 3: 更新数据 (长)
        self.btn_data_long = QPushButton("3. Load Long Data")
        self.btn_data_long.clicked.connect(self.load_long_data)
        layout.addWidget(self.btn_data_long)

        # 按钮 4: 关闭
        self.btn_close = QPushButton("4. Close Widget")
        self.btn_close.clicked.connect(self.on_close_clicked)
        layout.addWidget(self.btn_close)

        # 状态标签
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

    def on_show_clicked(self):
        # 调试 show()
        self.target_widget.show()
        # 如果窗口被最小化了，这句可以把它拉到最前
        self.target_widget.raise_()
        self.target_widget.activateWindow()
        self.status_label.setText("Widget Shown")

    def on_close_clicked(self):
        # 调试 close()
        # close() 只是隐藏窗口，只有设置了 WA_DeleteOnClose 才会销毁
        # 对于这种工具窗口，通常只是隐藏，下次再 show 出来
        self.target_widget.close()
        self.status_label.setText("Widget Closed")

    def load_short_data(self):
        data = [
            "Layer : smt", "Pad #974\nX=2.4",
            "Geometry", "smd603",
            "Net Info", "No Net",
            "Extra", "None"
        ]
        self.target_widget.update_content(data)
        self.status_label.setText("Short Data Loaded")

    def load_long_data(self):
        long_text = "Line 1\nLine 2\nLine 3\n" * 10
        data = [
            "Layer : smt", "Pad #974\nDetailed Info...",
            "Geometry", "Complex Geometry Data\nWith Multiple Lines",
            "Net Info", "Net-GND\nNet-VCC\nNet-SIG1",
            "Extra Logs", long_text
        ]
        self.target_widget.update_content(data)
        self.status_label.setText("Long Data Loaded")

    def closeEvent(self, event):
        # 当调试窗口关闭时，把目标窗口也关了，防止僵尸进程
        self.target_widget.close()
        super().closeEvent(event)

# ============================================================================
# 3. 程序入口
# ============================================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 启动调试窗口
    debugger = DebugControlWindow()
    debugger.show()

    sys.exit(app.exec())