# =================================================================
# 1. 子进程代码：这是一个独立的、微型的 Qt 程序
#    注意：这个函数必须定义在全局，不能定义在类里面
# =================================================================
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, \
    QProgressBar


def run_loading_process(text="Loading...", win_title="Please Wait"):
    """
    这是子进程的入口函数。
    它会创建一个全新的 QApplication，拥有独立的事件循环。
    """
    # 子进程需要创建自己的 QApplication
    # 注意：在子进程中 sys.argv 也是可用的
    app = QApplication(sys.argv)

    # 创建 Loading 窗口
    dialog = QDialog()
    dialog.setWindowTitle(win_title)
    dialog.setFixedSize(300, 100)

    # 设置窗口标志：
    # 1. WindowStaysOnTopHint: 确保Loading条总在最上层，挡住那个可能已经卡死的主窗口
    # 2. CustomizeWindowHint | WindowTitleHint: 去掉右上角的关闭按钮，防止用户乱点
    dialog.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint | Qt.WindowTitleHint)

    layout = QVBoxLayout(dialog)

    # 提示文字
    label = QLabel(text)
    label.setAlignment(Qt.AlignCenter)
    layout.addWidget(label)

    # 进度条
    pbar = QProgressBar()
    pbar.setRange(0, 0)
    layout.addWidget(pbar)
    dialog.show()

    # 进入子进程的事件循环
    sys.exit(app.exec())