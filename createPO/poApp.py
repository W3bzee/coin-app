import sys
from PyQt6.QtWidgets import (
    QWidget, QApplication, QVBoxLayout, QPushButton, QHBoxLayout, 
    QTextEdit, QGridLayout, QStackedLayout, QFrame,
    QLabel, QCheckBox, QComboBox, QListWidget, QLineEdit,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider
)
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt

from PyQt6.QtCore import QSize
#from findPCGS import pcgsCoinLookup

class purchaseOrderWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PCGS Coin Inventory Tracker')
        self.setWindowIcon(QIcon('assets\coin.ico'))
        self.resize(self.screen().size().width(), self.screen().size().height()-80)

        #Set window layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        """BEGIN WIDGITS"""
        #Back Button
        backButton = QPushButton(QIcon("assets\FreeWebToolkit_1677391325.ico"),"", self)
        backButton.setGeometry(0, 0, 100, 100)
        backButton.setIconSize(QSize(80,80))
        backButton.clicked.connect(self.returnHomeScreen)

        #Top Label
        self.topLabel = QLabel('Third Coast \nSupply Company LLC')
        self.topLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)


        layout.addWidget(backButton)
        layout.addWidget(self.topLabel)

    def returnHomeScreen(self):
        window.close()
        #sys.path.insert(0, './homeScreen')
        import homeScreen.homeApp as homeApp
        


"""CALL APPLICATION"""
#app = QApplication(sys.argv)
window = purchaseOrderWindow()
window.show()
#app.exec()

