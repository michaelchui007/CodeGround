import sys
import time
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox
from PySide6.QtCore import QThread, Signal

# 引入上面的 Dialog
from loading_dialog import LoadingDialog

# --- 模拟后端任务的线程 ---
class AnalysisWorker(QThread):
    # 定义信号：任务完成时触发
    finished_signal = Signal(dict) # 可以传回结果，比如一个字典

    def run(self):
        """这里写耗时的 C++ / Python 逻辑"""
        print("Backend: 开始生成报告...")
        # 模拟耗时操作 3秒
        time.sleep(3)

        # 模拟生成的结果
        result = {"status": "success", "path": "/tmp/report.pdf"}
        print("Backend: 报告生成完毕")

        # 发送信号通知主线程
        self.finished_signal.emit(result)

# --- 主界面 ---
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(400, 300)

        container = QWidget()
        layout = QVBoxLayout(container)

        self.btn = QPushButton("生成分析报告")
        self.btn.clicked.connect(self.start_analysis)
        layout.addWidget(self.btn)

        self.setCentralWidget(container)

    def start_analysis(self):
        # 1. 实例化 Loading 弹窗
        self.loading_ui = LoadingDialog(self, "正在分析数据，请勿关闭...")

        # 2. 实例化后台线程
        self.worker = AnalysisWorker()

        # 3. 【关键连接】
        # 当线程结束 -> 关闭弹窗
        self.worker.finished_signal.connect(self.on_analysis_finished)

        # 4. 显示弹窗 (使用 open() 或 show()，不要用 exec() 阻塞主线程代码流)
        # 注意：因为是模态窗口，open() 后用户点不动主界面，但代码会继续往下走
        self.loading_ui.show()

        # 5. 启动线程
        self.worker.start()

    def on_analysis_finished(self, result):
        """线程跑完后回调这里"""
        # 1. 关闭 Loading
        if self.loading_ui:
            self.loading_ui.close()
            self.loading_ui = None

        # 2. 处理业务结果
        QMessageBox.information(self, "完成", f"报告已生成！\n路径: {result.get('path')}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())