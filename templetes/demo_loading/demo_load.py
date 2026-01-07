import sys
import time
from PySide6.QtWidgets import (QApplication, QDialog, QVBoxLayout,
                               QLabel, QProgressBar, QPushButton, QMessageBox, QWidget)
from PySide6.QtCore import Qt, QThread, Signal, Slot

# ========================================================
# 1. 加载中弹窗 (LoadingDialog)
# ========================================================
class LoadingDialog(QDialog):
    def __init__(self, parent=None, text="正在处理，请稍候..."):
        super().__init__(parent)
        self.setWindowTitle("处理中")
        self.setFixedSize(300, 100)

        # 去掉问号，甚至可以去掉关闭按钮，强制用户等待
        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        # 设为模态，阻止用户操作主界面
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        layout = QVBoxLayout(self)

        # 提示文字
        self.lbl_message = QLabel(text)
        self.lbl_message.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.lbl_message)

        # 进度条
        self.pbar = QProgressBar()
        # 设置为“繁忙”模式（来回滚动），因为有时候不知道具体进度
        # 如果 range 设为 0, 0，进度条就会变成跑马灯效果
        self.pbar.setRange(0, 0)
        self.pbar.setTextVisible(False)
        layout.addWidget(self.pbar)

    def closeEvent(self, event):
        # 阻止用户通过 Alt+F4 关闭，必须等任务结束
        event.ignore()

# ========================================================
# 2. 业务工作线程 (Worker Thread)
# ========================================================
class ExportWorker(QThread):
    # 定义信号：任务结束信号 (成功/失败, 返回消息)
    finished_signal = Signal(bool, str)

    def __init__(self, params):
        super().__init__()
        self.params = params

    def run(self):
        """
        这里运行耗时的后端接口代码
        """
        try:
            print(f"线程开始工作，参数: {self.params}")

            # --- 模拟调用后端接口 (耗时 3 秒) ---
            time.sleep(3)

            # 模拟：如果您需要把 params 传给 ctypes 接口，在这里做
            # result = my_backend.call(self.params)

            # 发送成功信号
            self.finished_signal.emit(True, "导出成功！文件已保存。")

        except Exception as e:
            # 发送失败信号
            self.finished_signal.emit(False, f"导出失败: {str(e)}")

# ========================================================
# 3. 您的导出界面 (模拟)
# ========================================================
class ExportView(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("导出设置")
        self.resize(400, 200)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("请点击 OK 模拟导出过程"))

        self.btn_ok = QPushButton("OK")
        layout.addWidget(self.btn_ok)

        self.btn_ok.clicked.connect(self.on_ok_clicked)

        # 占位变量，防止线程被垃圾回收
        self.worker = None
        self.loading_ui = None

    def on_ok_clicked(self):
        # 1. 获取参数 (模拟)
        params = {"path": "C:/test", "user": "admin"}

        # 2. 实例化 加载弹窗
        self.loading_ui = LoadingDialog(self, "正在导出报告，请勿关闭...")

        # 3. 实例化 工作线程
        self.worker = ExportWorker(params)

        # 4. 【核心】连接信号与槽
        # 当线程结束时 -> 关闭 Loading 弹窗
        self.worker.finished_signal.connect(self.on_worker_finished)

        # 5. 启动线程
        self.worker.start()

        # 6. 显示 Loading 弹窗 (exec 会阻塞在这里，直到 self.loading_ui.accept() 被调用)
        # 注意：虽然代码阻塞在这行，但因为 exec() 内部有事件循环，所以进度条动画会动
        self.loading_ui.exec()

    @Slot(bool, str)
    def on_worker_finished(self, success, message):
        """
        线程执行完后会自动调用这里
        """
        # 1. 无论成功失败，先关闭 Loading 弹窗
        if self.loading_ui:
            self.loading_ui.accept() # 这会让上面的 exec() 返回，代码继续往下走

        # 2. 根据结果处理业务
        if success:
            QMessageBox.information(self, "成功", message)
            self.accept() # 关闭导出设置窗口 (View)
        else:
            QMessageBox.critical(self, "错误", message)
            # 失败了就不关闭导出窗口，让用户重试

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExportView()
    window.show()
    sys.exit(app.exec())