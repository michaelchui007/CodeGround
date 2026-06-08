from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import QPoint, QRect, Qt
from PySide6.QtGui import QIntValidator, QPixmap, QValidator
from PySide6.QtWidgets import QApplication, QDialog, QMessageBox, QPushButton, QToolTip, QVBoxLayout, QWidget

from ui_message_dialog import Ui_RMessageDialog
from ui_resize_feature_dialog import Ui_ResizeFeatureDialog


ASSETS_DIR = Path(__file__).resolve().parent / "assets"
INTEGER_ONLY_MESSAGE = "Only integers are allowed"
INTEGER_ONLY_TIP_DURATION_MS = 2000


def asset_path(file_name: str) -> str:
    return str(ASSETS_DIR / file_name)


class FramelessDialogMixin:
    def _setup_frameless_dialog(self) -> None:
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
        self._drag_position: QPoint | None = None

        self.ui.titleCloseButton.clicked.connect(self.reject)
        self.ui.titleMinimizeButton.clicked.connect(self.showMinimized)
        self.ui.titleMaximizeButton.setEnabled(False)
        self.ui.titleBar.mousePressEvent = self._title_mouse_press_event
        self.ui.titleBar.mouseMoveEvent = self._title_mouse_move_event
        self.ui.titleBar.mouseReleaseEvent = self._title_mouse_release_event

    def _title_mouse_press_event(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def _title_mouse_move_event(self, event) -> None:
        if self._drag_position is not None and event.buttons() & Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_position)
            event.accept()

    def _title_mouse_release_event(self, event) -> None:
        self._drag_position = None
        event.accept()


class ResizeFeatureDialog(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_ResizeFeatureDialog()
        self.ui.setupUi(self)
        self.ui.sizeLineEdit.setValidator(QIntValidator(0, 2147483647, self.ui.sizeLineEdit))
        self.ui.sizeLineEdit.inputRejected.connect(self.show_integer_input_tip)

        self.ui.applyButton.clicked.connect(self.apply_size)
        self.ui.okButton.clicked.connect(self.accept_if_valid)
        self.ui.closeButton.clicked.connect(self.reject)
        self.ui.helpButton.clicked.connect(self.show_help)

    def is_size_valid(self) -> bool:
        validator = self.ui.sizeLineEdit.validator()
        state, _, _ = validator.validate(self.ui.sizeLineEdit.text(), 0)
        return state == QValidator.State.Acceptable

    def show_integer_input_tip(self) -> None:
        line_edit = self.ui.sizeLineEdit
        tip_position = line_edit.mapToGlobal(line_edit.rect().bottomLeft())
        QToolTip.showText(tip_position, INTEGER_ONLY_MESSAGE, line_edit, QRect(), INTEGER_ONLY_TIP_DURATION_MS)
        line_edit.setFocus()

    def apply_size(self) -> None:
        if not self.is_size_valid():
            self.show_integer_input_tip()
            return
        print(f"Apply size: {self.ui.sizeLineEdit.text()} ml")

    def accept_if_valid(self) -> None:
        if not self.is_size_valid():
            self.show_integer_input_tip()
            return
        self.accept()

    def show_help(self) -> None:
        QMessageBox.information(self, "Help", "Input the resize value in ml.")


class RMessageDialog(QDialog, FramelessDialogMixin):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_RMessageDialog()
        self.ui.setupUi(self)
        self.ui.logoLabel.setPixmap(QPixmap(asset_path("logo_node.png")))
        self.ui.warningIconLabel.setPixmap(QPixmap(asset_path("warning.svg")))
        self._setup_frameless_dialog()

        self.ui.okButton.clicked.connect(self.accept)
        self.ui.cancelButton.clicked.connect(self.reject)


class DemoWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Figma Qt Dialog Demo")

        layout = QVBoxLayout(self)
        resize_button = QPushButton("Open Resize Feature Dialog")
        message_button = QPushButton("Open Message Dialog")
        layout.addWidget(resize_button)
        layout.addWidget(message_button)

        resize_button.clicked.connect(self.open_resize_dialog)
        message_button.clicked.connect(self.open_message_dialog)

    def open_resize_dialog(self) -> None:
        ResizeFeatureDialog(self).exec()

    def open_message_dialog(self) -> None:
        RMessageDialog(self).exec()


def main() -> int:
    app = QApplication(sys.argv)
    window = DemoWindow()
    window.resize(280, 100)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
