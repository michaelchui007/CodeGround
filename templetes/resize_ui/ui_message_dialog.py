# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'message_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QToolButton, QVBoxLayout, QWidget)

class Ui_RMessageDialog(object):
    def setupUi(self, RMessageDialog):
        if not RMessageDialog.objectName():
            RMessageDialog.setObjectName(u"RMessageDialog")
        RMessageDialog.resize(320, 140)
        RMessageDialog.setMinimumSize(QSize(320, 140))
        RMessageDialog.setMaximumSize(QSize(320, 140))
        RMessageDialog.setStyleSheet(u"QDialog#RMessageDialog {\n"
"    background-color: #2c2c2c;\n"
"    border-radius: 4px;\n"
"}\n"
"QLabel {\n"
"    color: #ffffff;\n"
"    font-family: \"Source Han Sans CN\", \"Microsoft YaHei\", Arial;\n"
"    font-size: 10px;\n"
"}\n"
"QFrame#titleBar {\n"
"    background-color: #ffffff;\n"
"    border-top-left-radius: 4px;\n"
"    border-top-right-radius: 4px;\n"
"}\n"
"QLabel#logoLabel {\n"
"    color: #c5161d;\n"
"    font-size: 6px;\n"
"    font-weight: 700;\n"
"    line-height: 7px;\n"
"}\n"
"QLabel#titleLabel {\n"
"    color: #000000;\n"
"    font-size: 10px;\n"
"    font-weight: 500;\n"
"}\n"
"QToolButton#titleMinimizeButton,\n"
"QToolButton#titleMaximizeButton,\n"
"QToolButton#titleCloseButton {\n"
"    background: transparent;\n"
"    border: none;\n"
"    color: #1f1f1f;\n"
"    font-size: 16px;\n"
"    font-weight: 400;\n"
"}\n"
"QToolButton#titleMinimizeButton:hover,\n"
"QToolButton#titleMaximizeButton:hover {\n"
"    background-color: #ededed;\n"
"}\n"
"QToolButton#titleCloseButton:hover {\n"
""
                        "    background-color: #e81123;\n"
"    color: #ffffff;\n"
"}\n"
"QPushButton {\n"
"    background-color: #535353;\n"
"    border: 1px solid #7b7b7b;\n"
"    border-radius: 4px;\n"
"    color: #ffffff;\n"
"    font-family: \"Source Han Sans CN\", \"Microsoft YaHei\", Arial;\n"
"    font-size: 10px;\n"
"    min-height: 20px;\n"
"    max-height: 20px;\n"
"    padding: 0 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #606060;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #484848;\n"
"}")
        self.rootLayout = QVBoxLayout(RMessageDialog)
        self.rootLayout.setSpacing(0)
        self.rootLayout.setObjectName(u"rootLayout")
        self.rootLayout.setContentsMargins(0, 0, 0, 8)
        self.titleBar = QFrame(RMessageDialog)
        self.titleBar.setObjectName(u"titleBar")
        self.titleBar.setMinimumSize(QSize(0, 28))
        self.titleBar.setMaximumSize(QSize(16777215, 28))
        self.titleBar.setFrameShape(QFrame.Shape.NoFrame)
        self.titleLayout = QHBoxLayout(self.titleBar)
        self.titleLayout.setSpacing(6)
        self.titleLayout.setObjectName(u"titleLayout")
        self.titleLayout.setContentsMargins(8, 0, 8, 0)
        self.logoLabel = QLabel(self.titleBar)
        self.logoLabel.setObjectName(u"logoLabel")
        self.logoLabel.setMinimumSize(QSize(26, 26))
        self.logoLabel.setMaximumSize(QSize(26, 26))
        self.logoLabel.setScaledContents(True)
        self.logoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.titleLayout.addWidget(self.logoLabel)

        self.titleLabel = QLabel(self.titleBar)
        self.titleLabel.setObjectName(u"titleLabel")
        self.titleLabel.setMinimumSize(QSize(0, 20))
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignVCenter|Qt.AlignmentFlag.AlignLeft)

        self.titleLayout.addWidget(self.titleLabel)

        self.titleMinimizeButton = QToolButton(self.titleBar)
        self.titleMinimizeButton.setObjectName(u"titleMinimizeButton")
        self.titleMinimizeButton.setMinimumSize(QSize(16, 16))
        self.titleMinimizeButton.setMaximumSize(QSize(16, 16))
        self.titleMinimizeButton.setAutoRaise(True)

        self.titleLayout.addWidget(self.titleMinimizeButton)

        self.titleMaximizeButton = QToolButton(self.titleBar)
        self.titleMaximizeButton.setObjectName(u"titleMaximizeButton")
        self.titleMaximizeButton.setMinimumSize(QSize(16, 16))
        self.titleMaximizeButton.setMaximumSize(QSize(16, 16))
        self.titleMaximizeButton.setAutoRaise(True)

        self.titleLayout.addWidget(self.titleMaximizeButton)

        self.titleCloseButton = QToolButton(self.titleBar)
        self.titleCloseButton.setObjectName(u"titleCloseButton")
        self.titleCloseButton.setMinimumSize(QSize(16, 16))
        self.titleCloseButton.setMaximumSize(QSize(16, 16))
        self.titleCloseButton.setAutoRaise(True)

        self.titleLayout.addWidget(self.titleCloseButton)


        self.rootLayout.addWidget(self.titleBar)

        self.contentContainer = QWidget(RMessageDialog)
        self.contentContainer.setObjectName(u"contentContainer")
        self.contentContainer.setMinimumSize(QSize(0, 84))
        self.contentContainer.setMaximumSize(QSize(16777215, 84))
        self.messageLayout = QHBoxLayout(self.contentContainer)
        self.messageLayout.setSpacing(16)
        self.messageLayout.setObjectName(u"messageLayout")
        self.messageLayout.setContentsMargins(30, 22, 30, 22)
        self.warningIconLabel = QLabel(self.contentContainer)
        self.warningIconLabel.setObjectName(u"warningIconLabel")
        self.warningIconLabel.setMinimumSize(QSize(40, 40))
        self.warningIconLabel.setMaximumSize(QSize(40, 40))
        self.warningIconLabel.setScaledContents(True)
        self.warningIconLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.messageLayout.addWidget(self.warningIconLabel)

        self.messageLabel = QLabel(self.contentContainer)
        self.messageLabel.setObjectName(u"messageLabel")
        self.messageLabel.setMinimumSize(QSize(204, 40))
        self.messageLabel.setMaximumSize(QSize(204, 40))
        self.messageLabel.setWordWrap(True)
        self.messageLabel.setAlignment(Qt.AlignmentFlag.AlignVCenter|Qt.AlignmentFlag.AlignLeft)

        self.messageLayout.addWidget(self.messageLabel)


        self.rootLayout.addWidget(self.contentContainer)

        self.bottomBar = QFrame(RMessageDialog)
        self.bottomBar.setObjectName(u"bottomBar")
        self.bottomBar.setMinimumSize(QSize(0, 20))
        self.bottomBar.setMaximumSize(QSize(16777215, 20))
        self.bottomBar.setFrameShape(QFrame.Shape.NoFrame)
        self.bottomLayout = QHBoxLayout(self.bottomBar)
        self.bottomLayout.setSpacing(10)
        self.bottomLayout.setObjectName(u"bottomLayout")
        self.bottomLayout.setContentsMargins(0, 0, 8, 0)
        self.buttonSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.bottomLayout.addItem(self.buttonSpacer)

        self.okButton = QPushButton(self.bottomBar)
        self.okButton.setObjectName(u"okButton")
        self.okButton.setMinimumSize(QSize(68, 20))
        self.okButton.setMaximumSize(QSize(68, 20))

        self.bottomLayout.addWidget(self.okButton)

        self.cancelButton = QPushButton(self.bottomBar)
        self.cancelButton.setObjectName(u"cancelButton")
        self.cancelButton.setMinimumSize(QSize(68, 20))
        self.cancelButton.setMaximumSize(QSize(68, 20))

        self.bottomLayout.addWidget(self.cancelButton)


        self.rootLayout.addWidget(self.bottomBar)


        self.retranslateUi(RMessageDialog)

        QMetaObject.connectSlotsByName(RMessageDialog)
    # setupUi

    def retranslateUi(self, RMessageDialog):
        RMessageDialog.setWindowTitle(QCoreApplication.translate("RMessageDialog", u"Dialog Box", None))
        self.logoLabel.setText("")
        self.titleLabel.setText(QCoreApplication.translate("RMessageDialog", u"Dialog Box", None))
        self.titleMinimizeButton.setText(QCoreApplication.translate("RMessageDialog", u"-", None))
        self.titleMaximizeButton.setText(QCoreApplication.translate("RMessageDialog", u"\u25a1", None))
        self.titleCloseButton.setText(QCoreApplication.translate("RMessageDialog", u"X", None))
        self.warningIconLabel.setText("")
        self.messageLabel.setText(QCoreApplication.translate("RMessageDialog", u"Operation will be performed on ALL features. Continue?", None))
        self.okButton.setText(QCoreApplication.translate("RMessageDialog", u"OK", None))
        self.cancelButton.setText(QCoreApplication.translate("RMessageDialog", u"Cancel", None))
    # retranslateUi

