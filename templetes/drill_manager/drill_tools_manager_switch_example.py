from PySide6.QtWidgets import QDialog

from ui_drill_tools_manager import Ui_DrillToolsManagerDialog


class DrillToolsManagerDialog(QDialog, Ui_DrillToolsManagerDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.modeToggleCheckBox.toggled.connect(self.on_mode_toggled)
        self.basicCloseButton.clicked.connect(self.close)
        self.fullCloseButton.clicked.connect(self.close)

        self.on_mode_toggled(self.modeToggleCheckBox.isChecked())

    def on_mode_toggled(self, checked: bool) -> None:
        mode_index = 1 if checked else 0
        self.topOptionsStackedWidget.setCurrentIndex(mode_index)
        self.bodyStackedWidget.setCurrentIndex(mode_index)
        self.modeToggleCheckBox.setText("Full / Basic" if checked else "Basic / Full")
