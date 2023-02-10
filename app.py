import sys
from PyQt6.QtWidgets import (
    QWidget, QApplication, QVBoxLayout, QPushButton,
    QTextEdit, QGridLayout, QStackedLayout, QFrame,
    QLabel, QCheckBox, QComboBox, QListWidget, QLineEdit,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider
)
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PCGS Coin Inventory Tracker')
        self.setWindowIcon(QIcon('coin.ico'))
        self.resize(800, 650) # width,height

        #Set window layout
        layout = QGridLayout()
        self.setLayout(layout)

        """BEGIN WIDGITS"""
        #Top Label
        self.topLabel = QLabel('Coin Tracker Inventory System')
        self.topLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        #Bar-Code Input Field
        self.BarCodeInput = QLineEdit()
        self.BarCodeInput.setMaxLength(17)
        self.BarCodeInput.setAlignment(Qt.AlignmentFlag.AlignCenter)

        #Run Button
        runButton = QPushButton('&Run', clicked=self.run)
        self.outputField = QTextEdit()

        """BEGIN LAYOUT"""
        #layout
        layout.addWidget(self.topLabel)
        layout.addWidget(self.BarCodeInput)
        layout.addWidget(runButton)
        layout.addWidget(self.outputField)

    """DEFINE FUNCTIONS"""
    def run(self):
        barCode = self.BarCodeInput.text()
        self.outputField.setText('{0}'.format(barCode))




"""CALL APPLICATION"""
app = QApplication(sys.argv)
with open("styles.css","r") as file:
    app.setStyleSheet(file.read())
window = MyApp()
window.show()
app.exec()



"""
HELPFUL LINKS:

For Structure: https://www.pythonguis.com/tutorials/pyqt6-layouts/



"""