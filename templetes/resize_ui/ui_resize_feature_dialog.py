# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'resize_feature_dialog.ui'
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
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QToolButton, QVBoxLayout, QWidget)

class Ui_ResizeFeatureDialog(object):
    def setupUi(self, ResizeFeatureDialog):
        if not ResizeFeatureDialog.objectName():
            ResizeFeatureDialog.setObjectName(u"ResizeFeatureDialog")
        ResizeFeatureDialog.resize(330, 150)
        ResizeFeatureDialog.setMinimumSize(QSize(330, 150))
        ResizeFeatureDialog.setMaximumSize(QSize(330, 150))
        ResizeFeatureDialog.setStyleSheet(u"QDialog#ResizeFeatureDialog {\n"
"    background-color: #2c2c2c;\n"
"    border-radius: 4px;\n"
"}\n"
"QLabel {\n"
"    color: #ffffff;\n"
"    font-family: \"Source Han Sans CN\", \"Microsoft YaHei\", Arial;\n"
"    font-size: 10px;\n"
"}\n"
"QFrame#contentFrame {\n"
"    background-color: #3b3b3b;\n"
"    border: 1px solid #7b7b7b;\n"
"}\n"
"QLineEdit#sizeLineEdit {\n"
"    background-color: #454545;\n"
"    border: 1px solid #7b7b7b;\n"
"    border-radius: 4px;\n"
"    color: #ffffff;\n"
"    padding-left: 8px;\n"
"    padding-right: 8px;\n"
"    font-family: \"Source Han Sans CN\", \"Microsoft YaHei\", Arial;\n"
"    font-size: 10px;\n"
"    min-height: 20px;\n"
"    max-height: 20px;\n"
"}\n"
"QToolButton#helpButton {\n"
"    background-color: #5f5f5f;\n"
"    border: none;\n"
"    border-radius: 10px;\n"
"    color: #ffffff;\n"
"    font-family: Arial;\n"
"    font-size: 13px;\n"
"    font-weight: 700;\n"
"}\n"
"QPushButton {\n"
"    background-color: #535353;\n"
"    border: 1px solid #7b7b7b;\n"
"    b"
                        "order-radius: 4px;\n"
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
        self.rootLayout = QVBoxLayout(ResizeFeatureDialog)
        self.rootLayout.setSpacing(0)
        self.rootLayout.setObjectName(u"rootLayout")
        self.rootLayout.setContentsMargins(0, 0, 0, 10)
        self.contentContainer = QWidget(ResizeFeatureDialog)
        self.contentContainer.setObjectName(u"contentContainer")
        self.contentContainer.setMinimumSize(QSize(0, 120))
        self.contentContainer.setMaximumSize(QSize(16777215, 120))
        self.contentLayout = QVBoxLayout(self.contentContainer)
        self.contentLayout.setSpacing(0)
        self.contentLayout.setObjectName(u"contentLayout")
        self.contentLayout.setContentsMargins(10, 10, 10, 10)
        self.contentFrame = QFrame(self.contentContainer)
        self.contentFrame.setObjectName(u"contentFrame")
        self.contentFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.contentFrame.setFrameShadow(QFrame.Shadow.Plain)
        self.sizeLabel = QLabel(self.contentFrame)
        self.sizeLabel.setObjectName(u"sizeLabel")
        self.sizeLabel.setGeometry(QRect(9, 17, 104, 20))
        self.sizeLabel.setAlignment(Qt.AlignmentFlag.AlignVCenter|Qt.AlignmentFlag.AlignLeft)
        self.sizeLineEdit = QLineEdit(self.contentFrame)
        self.sizeLineEdit.setObjectName(u"sizeLineEdit")
        self.sizeLineEdit.setGeometry(QRect(113, 17, 120, 20))
        self.sizeLineEdit.setFrame(True)
        self.unitLabel = QLabel(self.contentFrame)
        self.unitLabel.setObjectName(u"unitLabel")
        self.unitLabel.setGeometry(QRect(237, 17, 46, 20))
        self.unitLabel.setAlignment(Qt.AlignmentFlag.AlignVCenter|Qt.AlignmentFlag.AlignLeft)

        self.contentLayout.addWidget(self.contentFrame)


        self.rootLayout.addWidget(self.contentContainer)

        self.bottomBar = QFrame(ResizeFeatureDialog)
        self.bottomBar.setObjectName(u"bottomBar")
        self.bottomBar.setMinimumSize(QSize(0, 20))
        self.bottomBar.setMaximumSize(QSize(16777215, 20))
        self.bottomBar.setFrameShape(QFrame.Shape.NoFrame)
        self.bottomLayout = QHBoxLayout(self.bottomBar)
        self.bottomLayout.setSpacing(0)
        self.bottomLayout.setObjectName(u"bottomLayout")
        self.bottomLayout.setContentsMargins(10, 0, 10, 0)
        self.helpButton = QToolButton(self.bottomBar)
        self.helpButton.setObjectName(u"helpButton")
        self.helpButton.setMinimumSize(QSize(20, 20))
        self.helpButton.setMaximumSize(QSize(20, 20))

        self.bottomLayout.addWidget(self.helpButton)

        self.bottomSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.bottomLayout.addItem(self.bottomSpacer)

        self.buttonContainer = QWidget(self.bottomBar)
        self.buttonContainer.setObjectName(u"buttonContainer")
        self.buttonLayout = QHBoxLayout(self.buttonContainer)
        self.buttonLayout.setSpacing(10)
        self.buttonLayout.setObjectName(u"buttonLayout")
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        self.applyButton = QPushButton(self.buttonContainer)
        self.applyButton.setObjectName(u"applyButton")
        self.applyButton.setMinimumSize(QSize(68, 20))
        self.applyButton.setMaximumSize(QSize(68, 20))

        self.buttonLayout.addWidget(self.applyButton)

        self.okButton = QPushButton(self.buttonContainer)
        self.okButton.setObjectName(u"okButton")
        self.okButton.setMinimumSize(QSize(68, 20))
        self.okButton.setMaximumSize(QSize(68, 20))

        self.buttonLayout.addWidget(self.okButton)

        self.closeButton = QPushButton(self.buttonContainer)
        self.closeButton.setObjectName(u"closeButton")
        self.closeButton.setMinimumSize(QSize(68, 20))
        self.closeButton.setMaximumSize(QSize(68, 20))

        self.buttonLayout.addWidget(self.closeButton)


        self.bottomLayout.addWidget(self.buttonContainer)


        self.rootLayout.addWidget(self.bottomBar)


        self.retranslateUi(ResizeFeatureDialog)

        QMetaObject.connectSlotsByName(ResizeFeatureDialog)
    # setupUi

    def retranslateUi(self, ResizeFeatureDialog):
        ResizeFeatureDialog.setWindowTitle(QCoreApplication.translate("ResizeFeatureDialog", u"Resize Featu...", None))
        self.sizeLabel.setText(QCoreApplication.translate("ResizeFeatureDialog", u"Size:", None))
        self.sizeLineEdit.setText(QCoreApplication.translate("ResizeFeatureDialog", u"10", None))
        self.unitLabel.setText(QCoreApplication.translate("ResizeFeatureDialog", u"ml", None))
        self.helpButton.setText(QCoreApplication.translate("ResizeFeatureDialog", u"?", None))
        self.applyButton.setText(QCoreApplication.translate("ResizeFeatureDialog", u"Apply", None))
        self.okButton.setText(QCoreApplication.translate("ResizeFeatureDialog", u"OK", None))
        self.closeButton.setText(QCoreApplication.translate("ResizeFeatureDialog", u"Close", None))
    # retranslateUi

