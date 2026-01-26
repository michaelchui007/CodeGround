import sys
import time
from multiprocessing import Process
from PySide6.QtWidgets import (QApplication, QDialog, QLabel,
                               QVBoxLayout, QPushButton, QProgressBar, QWidget)
from PySide6.QtCore import Qt

from templetes.demo_loading.util import run_loading_process


# =================================================================
# 2. 主进程代码：您的现有业务
# =================================================================
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("主程序 (单进程模式)")
        self.resize(400, 200)

        self.btn_export = QPushButton("导出报告 (点击测试)", self)
        self.btn_export.clicked.connect(self.on_export_clicked)

        layout = QVBoxLayout(self)
        layout.addWidget(self.btn_export)

    def on_export_clicked(self):
        """
        这里模拟点击 OK 后的操作流程
        """
        # target 指向上面全局函数
        # args 用来传参
        self.loading_proc = Process(target=run_loading_process, args=(
            "Please Wait...",
            "Exporting"
        ))

        self.loading_proc.start()
        # 可选：稍微等一下，确保子进程窗口弹出来了再开始干活
        # 防止主进程瞬间卡死导致子进程启动指令没发出去（极少见，但为了稳妥）
        time.sleep(0.5)
        try:
            # 调用的相关业务逻辑写在这里
            self.call_backend_interface()

        finally:
            # 无论业务成功还是报错，都要确保把 Loading 窗口关掉
            if self.loading_proc.is_alive():
                self.loading_proc.terminate() # 暴力终止子进程
                self.loading_proc.join()      # 回收子进程资源

    def call_backend_interface(self):
        # 模拟一个耗时 5 秒的阻塞操作
        # 在这 5 秒内，MainWindow 是无法拖动和点击的
        # 但是屏幕中央的 Loading 窗口依然流畅转动
        time.sleep(10)

# =================================================================
# 3. 程序入口 (必须加这个保护！)
# =================================================================
if __name__ == "__main__":
    # Windows 下使用 multiprocessing 必须放在 if __name__ == "__main__": 下
    # 否则会无限循环启动进程导致报错
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())