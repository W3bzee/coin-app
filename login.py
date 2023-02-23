import sys
from PyQt6.QtWidgets import (
    QWidget, QApplication, QVBoxLayout, QPushButton, QHBoxLayout, QDialog, QMessageBox,QInputDialog,
    QTextEdit, QGridLayout, QStackedLayout, QFrame,
    QLabel, QCheckBox, QComboBox, QListWidget, QLineEdit,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider
)
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt
import os
import pandas as pd

from dotenv import load_dotenv
load_dotenv()
unpws = os.getenv('REGISTER')
unpwFilepath = './assets/unpw.csv'


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PCGS Coin Inventory Tracker')
        self.setWindowIcon(QIcon('assets/coin.ico'))
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

        self.unInput = QLineEdit()
        layout.addWidget(self.unInput, 1, 1, 1, 2)

        self.pwInput = QLineEdit()
        self.pwInput.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.pwInput, 2, 1, 1, 2)

        self.button1 = QPushButton('Register')
        self.button1.clicked.connect(self.register)
        layout.addWidget(self.button1, 3, 1)

        self.button2 = QPushButton("Login")
        self.button2.clicked.connect(self.login)
        layout.addWidget(self.button2, 3, 2)

        

    """DEFINE FUNCTIONS"""
    def login(self):
        username = self.unInput.text()
        pw = self.pwInput.text()
        if (username in [row for row in pd.read_csv(unpwFilepath)['un']]) and (pw in [row for row in pd.read_csv(unpwFilepath)['pw']]):
            window.close()
            import homeScreen.homeApp as homeApp
        else:
            self.noLoginPopup = QMessageBox(self)
            self.noLoginPopup.setWindowTitle('Incorrect Login or Password')
            self.noLoginPopup.setText('Incorrect login or password. Please try again. \
                                      \n\nIf this is your first time logging in, \
                                      \nplease click the register button. ')
            self.noLoginPopup.setIcon(QMessageBox.Icon.Warning)
            self.noLoginPopup.setStyleSheet('''QLabel {
            border: 2px solid rgb(11, 11, 11);
            border-radius: 4px;
            padding: 2px;
            color: rgb(255, 42, 0);
            max-width: 2000%;
            }''')
            self.noLoginPopup.exec()

    def register(self):
        self.registerKey, ok = QInputDialog.getText(self,'User Register Account Key', 'Please Enter The Registration Key')
        if ok and (self.registerKey == unpws):
            unpwDF = pd.read_csv(unpwFilepath).append({'un':self.unInput.text(),'pw':self.pwInput.text()},ignore_index=True)
            unpwDF.to_csv(unpwFilepath,index=False)
            self.registerPopup = QMessageBox(self)
            self.registerPopup.setWindowTitle('Success')
            self.registerPopup.setText('User {} succesfully added!\
                                      \nAttempt to Login Now'.format(self.unInput.text()))
            self.registerPopup.setIcon(QMessageBox.Icon.Information)
            self.registerPopup.exec()
        else:
            self.failRegisterPopup = QMessageBox(self)
            self.failRegisterPopup.setWindowTitle('Registration Unsuccessful.')
            self.failRegisterPopup.setText('Incorrect Login. Please try again.')
            self.failRegisterPopup.setIcon(QMessageBox.Icon.Critical)
            self.failRegisterPopup.exec()

    


"""CALL APPLICATION"""
app = QApplication(sys.argv)
with open("createPO\styles.css","r") as file:
    app.setStyleSheet(file.read())
window = MyApp()
window.show()
app.exec()



"""
HELPFUL LINKS:

For Structure: https://www.pythonguis.com/tutorials/pyqt6-layouts/

For CSS Styling with PyQt6: https://doc.qt.io/qtforpython/overviews/stylesheet-examples.html#style-sheet-usage

"""