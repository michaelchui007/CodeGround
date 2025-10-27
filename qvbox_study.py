import sys

from PySide6.QtWidgets import QApplication, QLabel, QWidget

from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QDrag


class DragLabel(QLabel):

    def __init__(self, text, parent):

        super().__init__(text, parent)

        self.setAlignment(Qt.AlignCenter)

        self.setStyleSheet("background-color: yellow;")

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):

        if not (event.buttons() & Qt.LeftButton):
            return

        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return

        drag = QDrag(self)

        mime_data = QMimeData()

        mime_data.setText(self.text())

        drag.setMimeData(mime_data)

        drag.exec_(Qt.CopyAction | Qt.MoveAction)


class DragDropDemo(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setAcceptDrops(True)

        self.setGeometry(300, 300, 300, 200)

        self.setWindowTitle('Drag and Drop')

        self.label = DragLabel('Drag me', self)

        self.label.setGeometry(50, 50, 100, 30)

    def dragEnterEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        position = event.pos()

        self.label.move(position)

        event.setDropAction(Qt.MoveAction)

        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    demo = DragDropDemo()

    demo.show()

    sys.exit(app.exec_())
