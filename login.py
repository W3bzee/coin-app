import sys
from PyQt6.QtWidgets import (
    QWidget, QApplication, QVBoxLayout, QPushButton, QHBoxLayout,
    QTextEdit, QGridLayout, QStackedLayout, QFrame,
    QLabel, QCheckBox, QComboBox, QListWidget, QLineEdit,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider
)
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt
import os

from dotenv import load_dotenv
load_dotenv()
logins = os.getenv('LOGIN')
print(logins.split(':')[1])



class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PCGS Coin Inventory Tracker')
        self.setWindowIcon(QIcon('coin.ico'))
        #self.resize(800, 650) # width,height

        #Set window layout
        layout = QGridLayout()
        layout.setContentsMargins(30,30,30,30)
        layout.setSpacing(10)
        self.setLayout(layout)

        """BEGIN WIDGITS"""
        self.title = QLabel("Login Form:")
        layout.addWidget(self.title, 0, 1, 1, 3, Qt.AlignmentFlag.AlignCenter)

        self.user = QLabel("Login Form:")
        layout.addWidget(self.user, 1, 0)

        self.pwd = QLabel("Password")
        layout.addWidget(self.pwd, 2, 0)

        self.input1 = QLineEdit()
        layout.addWidget(self.input1, 1, 1, 1, 2)

        self.input2 = QLineEdit()
        self.input2.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.input2, 2, 1, 1, 2)

        self.button1 = QPushButton('Register')
        layout.addWidget(self.button1, 3, 1)

        self.button2 = QPushButton("Login")
        self.button2.clicked.connect(self.login)
        layout.addWidget(self.button2, 3, 2)

    """DEFINE FUNCTIONS"""
    def login(self):
        username = self.input2.text()
        pw = self.input1.text()
        print(username,pw)
        window.close()
        import mainApp






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

For CSS Styling with PyQt6: https://doc.qt.io/qtforpython/overviews/stylesheet-examples.html#style-sheet-usage

"""