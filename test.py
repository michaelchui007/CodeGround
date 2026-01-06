import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar, QWidget, QSizePolicy
from PySide6.QtCore import Qt, QSize

class NativeToolbarDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QMainWindow Toolbar 布局调试")
        self.resize(800, 200)

        # =========================================================
        # 1. 创建三个 Toolbar
        # =========================================================
        self.tb_top = QToolBar("Top Bar")
        self.tb_mid = QToolBar("Mid Bar")
        self.tb_bot = QToolBar("Bot Bar")

        # 【关键步骤 1】设置 ObjectName，用于 QSS 精准控制
        self.tb_top.setObjectName("tb_top")
        self.tb_mid.setObjectName("tb_mid")
        self.tb_bot.setObjectName("tb_bot")

        # 【关键步骤 2】禁止拖动 (Movable = False)
        # 如果不禁止，Qt 会在工具栏之间预留“拖动手柄”的空间，导致无法严丝合缝
        self.tb_top.setMovable(False)
        self.tb_mid.setMovable(False)
        self.tb_bot.setMovable(False)

        # =========================================================
        # 2. 使用 addToolBar 添加 (模拟您的真实环境)
        # =========================================================
        # 添加第一行
        self.addToolBar(Qt.TopToolBarArea, self.tb_top)

        # 【关键步骤 3】强制换行！
        # 这会让下一个 Toolbar 跑到下一行，而不是挤在右边
        self.addToolBarBreak(Qt.TopToolBarArea)

        # 添加第二行
        self.addToolBar(Qt.TopToolBarArea, self.tb_mid)

        # 再次强制换行
        self.addToolBarBreak(Qt.TopToolBarArea)

        # 添加第三行
        self.addToolBar(Qt.TopToolBarArea, self.tb_bot)

        # =========================================================
        # 3. 填充测试数据
        # =========================================================
        self.populate(self.tb_top, "Top")
        self.populate(self.tb_mid, "Mid")
        self.populate(self.tb_bot, "Bot")

        # =========================================================
        # 4. QSS 样式表 (核心魔法)
        # =========================================================
        self.setStyleSheet("""
            /* 全局设定：白底黑字 */
            QMainWindow {
                background-color: #ffffff;
            }

            /* --- QToolBar 通用设置 --- */
            QToolBar {
                background-color: #ffffff;
                border: none;      /* 去掉系统默认边框 */
                spacing: 10px;     /* 图标横向间距 */
                min-height: 36px;  /* 统一高度 */
            }

            /* 隐藏 QMainWindow 管理的工具栏分隔符 
               (就是两个工具栏中间那条看不见的缝) 
            */
            QMainWindow::separator {
                width: 0px;
                height: 0px;
                margin: 0px;
                padding: 0px;
            }

            /* =========================================
               TOP Toolbar: 只加底边框
            ========================================= */
            QToolBar#tb_top {
                border-bottom: 1px solid #000000;
                /* padding-bottom 稍微留一点，别切到字，但不要太多 */
                padding-bottom: 2px;
            }
            /* Top 的分割线：为了美观，留点上下边距 */
            QToolBar#tb_top::separator {
                background-color: #000000;
                width: 1px;
                margin-top: 5px;
                margin-bottom: 5px;
            }

            /* =========================================
               MIDDLE Toolbar: 您的痛点修复区
            ========================================= */
            QToolBar#tb_mid {
                /* 【核心】必须把内边距设为0，图标区才能贴紧上下的线 */
                padding-top: 0px;
                padding-bottom: 0px;

                /* 为了视觉平衡，可以把 spacing 设小一点 */
                spacing: 5px; 
            }

            /* 【核心】中间的分割线：margin 设为 0，让它顶天立地 */
            QToolBar#tb_mid::separator {
                background-color: #000000;
                width: 1px;
                margin-top: 0px;    /* 顶住 tb_top 的底边 */
                margin-bottom: 0px; /* 顶住 tb_bot 的顶边 */
            }

            /* =========================================
               BOTTOM Toolbar: 只加顶边框
            ========================================= */
            QToolBar#tb_bot {
                border-top: 1px solid #000000;
                padding-top: 2px;
            }
            QToolBar#tb_bot::separator {
                background-color: #000000;
                width: 1px;
                margin-top: 5px;
                margin-bottom: 5px;
            }
        """)

    def populate(self, toolbar, text):
        toolbar.addAction(f"{text} 1")
        toolbar.addAction(f"{text} 2")
        toolbar.addSeparator() # 添加分割线
        toolbar.addAction(f"{text} A")
        toolbar.addSeparator() # 添加分割线

        # 加一个撑开的 Widget 看看效果
        spacer = QWidget()
        spacer.setFixedWidth(50)
        # 调试用的虚线框，不需要可删除
        # spacer.setStyleSheet("border: 1px dashed #ccc;")
        toolbar.addWidget(spacer)

        toolbar.addAction("End")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NativeToolbarDemo()
    window.show()
    sys.exit(app.exec())