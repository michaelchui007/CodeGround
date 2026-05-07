# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'r_ui_bom_searce_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_RSearchDialog(object):
    def setupUi(self, RSearchDialog):
        if not RSearchDialog.objectName():
            RSearchDialog.setObjectName(u"RSearchDialog")
        RSearchDialog.resize(420, 140)
        self.verticalLayout = QVBoxLayout(RSearchDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_top = QHBoxLayout()
        self.horizontalLayout_top.setObjectName(u"horizontalLayout_top")
        self.label = QLabel(RSearchDialog)
        self.label.setObjectName(u"label")

        self.horizontalLayout_top.addWidget(self.label)

        self.searchLineEdit = QLineEdit(RSearchDialog)
        self.searchLineEdit.setObjectName(u"searchLineEdit")
        self.searchLineEdit.setMinimumSize(QSize(200, 0))

        self.horizontalLayout_top.addWidget(self.searchLineEdit)

        self.prevButton = QPushButton(RSearchDialog)
        self.prevButton.setObjectName(u"prevButton")
        self.prevButton.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_top.addWidget(self.prevButton)

        self.nextButton = QPushButton(RSearchDialog)
        self.nextButton.setObjectName(u"nextButton")
        self.nextButton.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_top.addWidget(self.nextButton)


        self.verticalLayout.addLayout(self.horizontalLayout_top)

        self.caseSensitiveCheckBox = QCheckBox(RSearchDialog)
        self.caseSensitiveCheckBox.setObjectName(u"caseSensitiveCheckBox")

        self.verticalLayout.addWidget(self.caseSensitiveCheckBox)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout_bottom = QHBoxLayout()
        self.horizontalLayout_bottom.setObjectName(u"horizontalLayout_bottom")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_bottom.addItem(self.horizontalSpacer)

        self.cancelButton = QPushButton(RSearchDialog)
        self.cancelButton.setObjectName(u"cancelButton")

        self.horizontalLayout_bottom.addWidget(self.cancelButton)


        self.verticalLayout.addLayout(self.horizontalLayout_bottom)


        self.retranslateUi(RSearchDialog)

        QMetaObject.connectSlotsByName(RSearchDialog)
    # setupUi

    def retranslateUi(self, RSearchDialog):
        RSearchDialog.setWindowTitle(QCoreApplication.translate("RSearchDialog", u"Search", None))
        self.label.setText(QCoreApplication.translate("RSearchDialog", u"Search Pattern:", None))
        self.prevButton.setText(QCoreApplication.translate("RSearchDialog", u"<", None))
        self.nextButton.setText(QCoreApplication.translate("RSearchDialog", u">", None))
        self.caseSensitiveCheckBox.setText(QCoreApplication.translate("RSearchDialog", u"Case Sensitive", None))
        self.cancelButton.setText(QCoreApplication.translate("RSearchDialog", u"Cancel", None))
    # retranslateUi

