from PySide6.QtCore import QRect, Qt
from PySide6.QtWidgets import QVBoxLayout, QWidget, QTableView, QMainWindow

class Ui_MainWindow:
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(472, 415)
        self.centralWidget = QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QVBoxLayout(self.centralWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableViewA = QTableView(self.centralWidget)
        self.tableViewA.setObjectName("tableViewA")
        
        self.verticalLayout.addWidget(self.tableViewA)
        
        self.tableViewB = QTableView(self.centralWidget)
        self.tableViewB.setObjectName("tableViewB")

        self.verticalLayout.addWidget(self.tableViewB)
        
        MainWindow.setCentralWidget(self.centralWidget)
        
        self.retranslateUi(MainWindow)
    
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("MainWindow")
