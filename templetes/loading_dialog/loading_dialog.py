from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Qt

class LoadingDialog(QDialog):
    def __init__(self, parent=None, text="Validating DFM Analysis..."):
        super().__init__(parent)

        # 1. 设置无边框 + 模态 + 顶层窗口
        # FramelessWindowHint: 去掉标题栏
        # WindowStaysOnTopHint: 保证它浮在最上面
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setModal(True)

        # 2. 设置背景样式 (圆角 + 阴影效果通过 QSS 实现)
        self.setStyleSheet("""
            QDialog {
                background-color: #3b3b3b;
                border: 1px solid #CCCCCC;
                border-radius: 2px;
            }
            QLabel {
                font-size: 14px;
                color: #FFFFFF;
                font-weight: bold;
            }
            QProgressBar {
                border: 1px solid #BBBBBB;
                border-radius: 2px;
                text-align: center;
                height: 10px;
            }
            QProgressBar::chunk {
                background-color: #3498db; /* 蓝色进度条 */
                border-radius: px;
            }
        """)

        self.setFixedSize(300, 100) # 固定大小

        # 3. 布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # 4. 提示文字
        self.label = QLabel(text, self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        layout.addSpacing(10)

        # 5. 进度条
        self.progress = QProgressBar(self)
        self.progress.setTextVisible(False) # 不显示百分比文字

        # 【关键点】设置 Range 为 (0, 0) 会触发“忙碌模式”
        # 进度条会显示为一个来回滚动的动画，表示“正在处理但不知道进度”
        self.progress.setRange(0, 0)

        layout.addWidget(self.progress)

    def set_text(self, text):
        """动态修改提示文字"""
        self.label.setText(text)