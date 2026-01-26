# =================================================================
# 1. 子进程代码：黑色毛玻璃风格 Loading
# =================================================================
import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (QApplication, QDialog, QVBoxLayout, QLabel,
                               QProgressBar, QFrame, QGraphicsDropShadowEffect)

def run_loading_process(text="Loading...", win_title="Please Wait"):
    app = QApplication(sys.argv)

    # 1. 创建主窗口
    dialog = QDialog()
    dialog.setWindowTitle(win_title)
    dialog.setFixedSize(320, 140) # 稍微加大一点尺寸以适应阴影

    # 2. 核心设置：无边框 + 窗口透明 + 顶层显示
    # Qt.FramelessWindowHint: 去掉标题栏和边框
    # Qt.WindowStaysOnTopHint: 保持在最前
    # Qt.Tool: 通常用于不显示在任务栏的小窗口（可选）
    dialog.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)

    # 设置背景完全透明，把渲染交给内部的 QFrame，这样才能实现圆角
    dialog.setAttribute(Qt.WA_TranslucentBackground)

    # 3. 布局结构：Dialog -> MainLayout -> ContainerFrame -> ContentLayout -> Controls
    # 为了显示阴影，主 Layout 必须留出边距 (Margins)
    main_layout = QVBoxLayout(dialog)
    main_layout.setContentsMargins(10, 10, 10, 10) # 留出空间给阴影

    # 4. 内容容器 (用来承载背景色和圆角)
    container = QFrame()
    container.setObjectName("Container") # 设置ID方便写QSS
    main_layout.addWidget(container)

    # 5. 添加阴影效果 (让黑色卡片有悬浮感)
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(15)
    shadow.setXOffset(0)
    shadow.setYOffset(0)
    shadow.setColor(QColor(0, 0, 0, 180)) # 深黑色阴影
    container.setGraphicsEffect(shadow)

    # 6. 内部控件布局
    content_layout = QVBoxLayout(container)
    content_layout.setAlignment(Qt.AlignCenter)
    content_layout.setSpacing(15) # 控件间距

    # loading 文字
    label = QLabel(text)
    label.setAlignment(Qt.AlignCenter)
    content_layout.addWidget(label)

    # 进度条
    pbar = QProgressBar()
    pbar.setRange(0, 0) # 忙碌模式
    pbar.setFixedHeight(12) # 细条更精致
    pbar.setTextVisible(False) # 不显示百分比文字
    content_layout.addWidget(pbar)

    # 7. 样式表 (QSS) - 黑色毛玻璃风格核心
    # rgba(30, 30, 30, 240): 深灰色背景，240是透明度(0-255)，略微透一点
    # --- QSS 样式表设置 ---
    # 7. 样式表 (QSS)
    # 7. 样式表 (QSS)
    dialog.setStyleSheet("""
                QFrame#Container {
                    background-color: rgba(28, 28, 28, 170); 
                    border: 1px solid rgba(255, 255, 255, 60); 
                    border-radius: 12px;
                }
                QLabel {
                    color: #FFFFFF; 
                    font-size: 14px;
                    font-weight: bold;
                    background-color: transparent;
                }

            """)
    dialog.show()
    sys.exit(app.exec())