# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'export_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QSpacerItem, QTextEdit, QToolButton,
    QVBoxLayout, QWidget)

class Ui_ExportDialog(object):
    def setupUi(self, ExportDialog):
        if not ExportDialog.objectName():
            ExportDialog.setObjectName(u"ExportDialog")
        ExportDialog.resize(850, 550)
        self.verticalLayout_main = QVBoxLayout(ExportDialog)
        self.verticalLayout_main.setObjectName(u"verticalLayout_main")
        self.horizontalLayout_content = QHBoxLayout()
        self.horizontalLayout_content.setObjectName(u"horizontalLayout_content")
        self.verticalLayout_left = QVBoxLayout()
        self.verticalLayout_left.setObjectName(u"verticalLayout_left")
        self.gridLayout_form = QGridLayout()
        self.gridLayout_form.setObjectName(u"gridLayout_form")
        self.label_format = QLabel(ExportDialog)
        self.label_format.setObjectName(u"label_format")

        self.gridLayout_form.addWidget(self.label_format, 0, 0, 1, 1)

        self.combo_format = QComboBox(ExportDialog)
        self.combo_format.setObjectName(u"combo_format")

        self.gridLayout_form.addWidget(self.combo_format, 0, 1, 1, 2)

        self.label_template = QLabel(ExportDialog)
        self.label_template.setObjectName(u"label_template")

        self.gridLayout_form.addWidget(self.label_template, 1, 0, 1, 1)

        self.le_template = QLineEdit(ExportDialog)
        self.le_template.setObjectName(u"le_template")

        self.gridLayout_form.addWidget(self.le_template, 1, 1, 1, 1)

        self.btn_template_browse = QToolButton(ExportDialog)
        self.btn_template_browse.setObjectName(u"btn_template_browse")

        self.gridLayout_form.addWidget(self.btn_template_browse, 1, 2, 1, 1)

        self.label_save_path = QLabel(ExportDialog)
        self.label_save_path.setObjectName(u"label_save_path")

        self.gridLayout_form.addWidget(self.label_save_path, 2, 0, 1, 1)

        self.le_save_path = QLineEdit(ExportDialog)
        self.le_save_path.setObjectName(u"le_save_path")

        self.gridLayout_form.addWidget(self.le_save_path, 2, 1, 1, 1)

        self.btn_save_path_browse = QToolButton(ExportDialog)
        self.btn_save_path_browse.setObjectName(u"btn_save_path_browse")

        self.gridLayout_form.addWidget(self.btn_save_path_browse, 2, 2, 1, 1)


        self.verticalLayout_left.addLayout(self.gridLayout_form)

        self.groupBox_project = QGroupBox(ExportDialog)
        self.groupBox_project.setObjectName(u"groupBox_project")
        self.gridLayout_project = QGridLayout(self.groupBox_project)
        self.gridLayout_project.setObjectName(u"gridLayout_project")
        self.label_project_name = QLabel(self.groupBox_project)
        self.label_project_name.setObjectName(u"label_project_name")

        self.gridLayout_project.addWidget(self.label_project_name, 0, 0, 1, 1)

        self.le_project_name = QLineEdit(self.groupBox_project)
        self.le_project_name.setObjectName(u"le_project_name")

        self.gridLayout_project.addWidget(self.le_project_name, 0, 1, 1, 1)

        self.label_prepared = QLabel(self.groupBox_project)
        self.label_prepared.setObjectName(u"label_prepared")

        self.gridLayout_project.addWidget(self.label_prepared, 1, 0, 1, 1)

        self.le_prepared_by = QLineEdit(self.groupBox_project)
        self.le_prepared_by.setObjectName(u"le_prepared_by")

        self.gridLayout_project.addWidget(self.le_prepared_by, 1, 1, 1, 1)

        self.label_desc = QLabel(self.groupBox_project)
        self.label_desc.setObjectName(u"label_desc")
        self.label_desc.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.gridLayout_project.addWidget(self.label_desc, 2, 0, 1, 1)

        self.te_description = QTextEdit(self.groupBox_project)
        self.te_description.setObjectName(u"te_description")

        self.gridLayout_project.addWidget(self.te_description, 2, 1, 1, 1)


        self.verticalLayout_left.addWidget(self.groupBox_project)

        self.horizontalLayout_checkboxes = QHBoxLayout()
        self.horizontalLayout_checkboxes.setObjectName(u"horizontalLayout_checkboxes")
        self.chk_top_image = QCheckBox(ExportDialog)
        self.chk_top_image.setObjectName(u"chk_top_image")

        self.horizontalLayout_checkboxes.addWidget(self.chk_top_image)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_checkboxes.addItem(self.horizontalSpacer)

        self.chk_bottom_image = QCheckBox(ExportDialog)
        self.chk_bottom_image.setObjectName(u"chk_bottom_image")

        self.horizontalLayout_checkboxes.addWidget(self.chk_bottom_image)


        self.verticalLayout_left.addLayout(self.horizontalLayout_checkboxes)


        self.horizontalLayout_content.addLayout(self.verticalLayout_left)

        self.groupBox_columns = QGroupBox(ExportDialog)
        self.groupBox_columns.setObjectName(u"groupBox_columns")
        self.gridLayout_cols = QGridLayout(self.groupBox_columns)
        self.gridLayout_cols.setObjectName(u"gridLayout_cols")
        self.label_avail = QLabel(self.groupBox_columns)
        self.label_avail.setObjectName(u"label_avail")

        self.gridLayout_cols.addWidget(self.label_avail, 0, 0, 1, 1)

        self.label_output = QLabel(self.groupBox_columns)
        self.label_output.setObjectName(u"label_output")

        self.gridLayout_cols.addWidget(self.label_output, 0, 2, 1, 1)

        self.list_available = QListWidget(self.groupBox_columns)
        self.list_available.setObjectName(u"list_available")

        self.gridLayout_cols.addWidget(self.list_available, 1, 0, 1, 1)

        self.verticalLayout_mid_btns = QVBoxLayout()
        self.verticalLayout_mid_btns.setObjectName(u"verticalLayout_mid_btns")
        self.verticalSpacer_1 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_mid_btns.addItem(self.verticalSpacer_1)

        self.btn_move_right = QPushButton(self.groupBox_columns)
        self.btn_move_right.setObjectName(u"btn_move_right")

        self.verticalLayout_mid_btns.addWidget(self.btn_move_right)

        self.btn_move_left = QPushButton(self.groupBox_columns)
        self.btn_move_left.setObjectName(u"btn_move_left")

        self.verticalLayout_mid_btns.addWidget(self.btn_move_left)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_mid_btns.addItem(self.verticalSpacer_2)


        self.gridLayout_cols.addLayout(self.verticalLayout_mid_btns, 1, 1, 1, 1)

        self.list_output = QListWidget(self.groupBox_columns)
        self.list_output.setObjectName(u"list_output")

        self.gridLayout_cols.addWidget(self.list_output, 1, 2, 1, 1)

        self.verticalLayout_right_btns = QVBoxLayout()
        self.verticalLayout_right_btns.setObjectName(u"verticalLayout_right_btns")
        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_right_btns.addItem(self.verticalSpacer_3)

        self.btn_top = QPushButton(self.groupBox_columns)
        self.btn_top.setObjectName(u"btn_top")

        self.verticalLayout_right_btns.addWidget(self.btn_top)

        self.btn_up = QPushButton(self.groupBox_columns)
        self.btn_up.setObjectName(u"btn_up")

        self.verticalLayout_right_btns.addWidget(self.btn_up)

        self.btn_down = QPushButton(self.groupBox_columns)
        self.btn_down.setObjectName(u"btn_down")

        self.verticalLayout_right_btns.addWidget(self.btn_down)

        self.btn_bottom = QPushButton(self.groupBox_columns)
        self.btn_bottom.setObjectName(u"btn_bottom")

        self.verticalLayout_right_btns.addWidget(self.btn_bottom)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_right_btns.addItem(self.verticalSpacer_4)


        self.gridLayout_cols.addLayout(self.verticalLayout_right_btns, 1, 3, 1, 1)


        self.horizontalLayout_content.addWidget(self.groupBox_columns)


        self.verticalLayout_main.addLayout(self.horizontalLayout_content)

        self.horizontalLayout_bottom = QHBoxLayout()
        self.horizontalLayout_bottom.setObjectName(u"horizontalLayout_bottom")
        self.horizontalSpacer_bottom = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_bottom.addItem(self.horizontalSpacer_bottom)

        self.btn_ok = QPushButton(ExportDialog)
        self.btn_ok.setObjectName(u"btn_ok")

        self.horizontalLayout_bottom.addWidget(self.btn_ok)

        self.btn_cancel = QPushButton(ExportDialog)
        self.btn_cancel.setObjectName(u"btn_cancel")

        self.horizontalLayout_bottom.addWidget(self.btn_cancel)


        self.verticalLayout_main.addLayout(self.horizontalLayout_bottom)


        self.retranslateUi(ExportDialog)

        QMetaObject.connectSlotsByName(ExportDialog)
    # setupUi

    def retranslateUi(self, ExportDialog):
        ExportDialog.setWindowTitle(QCoreApplication.translate("ExportDialog", u"Export Report", None))
        self.label_format.setText(QCoreApplication.translate("ExportDialog", u"Output Format", None))
        self.label_template.setText(QCoreApplication.translate("ExportDialog", u"Template", None))
        self.btn_template_browse.setText(QCoreApplication.translate("ExportDialog", u"...", None))
        self.label_save_path.setText(QCoreApplication.translate("ExportDialog", u"Save Path", None))
        self.btn_save_path_browse.setText(QCoreApplication.translate("ExportDialog", u"...", None))
        self.groupBox_project.setTitle(QCoreApplication.translate("ExportDialog", u"Project Information", None))
        self.label_project_name.setText(QCoreApplication.translate("ExportDialog", u"Project Name", None))
        self.label_prepared.setText(QCoreApplication.translate("ExportDialog", u"Prepared by", None))
        self.label_desc.setText(QCoreApplication.translate("ExportDialog", u"Job Description", None))
        self.chk_top_image.setText(QCoreApplication.translate("ExportDialog", u"top side image", None))
        self.chk_bottom_image.setText(QCoreApplication.translate("ExportDialog", u"bottom side image", None))
        self.groupBox_columns.setTitle(QCoreApplication.translate("ExportDialog", u"Output Columns", None))
        self.label_avail.setText(QCoreApplication.translate("ExportDialog", u"Available Columns", None))
        self.label_output.setText(QCoreApplication.translate("ExportDialog", u"Output Columns", None))
        self.btn_move_right.setText(QCoreApplication.translate("ExportDialog", u">", None))
        self.btn_move_left.setText(QCoreApplication.translate("ExportDialog", u"<", None))
        self.btn_top.setText(QCoreApplication.translate("ExportDialog", u"\u21c8", None))
        self.btn_up.setText(QCoreApplication.translate("ExportDialog", u"\u2191", None))
        self.btn_down.setText(QCoreApplication.translate("ExportDialog", u"\u2193", None))
        self.btn_bottom.setText(QCoreApplication.translate("ExportDialog", u"\u21ca", None))
        self.btn_ok.setText(QCoreApplication.translate("ExportDialog", u"OK", None))
        self.btn_cancel.setText(QCoreApplication.translate("ExportDialog", u"Cancel", None))
    # retranslateUi

