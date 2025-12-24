from PySide6.QtWidgets import QComboBox


def add_combo_to_toolbar(self)-> None:
    """为toolbar增加Combobox"""
    self.combo = QComboBox()
    self.combo.addItems(["..."])
    self.combo.setFixedHeight(20)
    self.combo.setMinimumwidth(177)
    self.combo.currentIndexChanged.connect(self.on_combo_select)
    self.ui.toolbarwidget1.addwidget(self.combo)