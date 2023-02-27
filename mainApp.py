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
from PyQt6.QtCore import QSize

import pandas as pd
from PyQt6.QtCore import QAbstractTableModel, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableView

from dotenv import load_dotenv
load_dotenv()
unpws = os.getenv('REGISTER')
unpwFilepath = './assets/unpw.csv'


from createNewPO import *

import sys
from PyQt6 import QtCore, QtGui, QtWidgets

import pandas as pd


global app
global loginWindow
global homeAppWindow
global POAppWindow


"""HELPER CLASSES"""
class PandasModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(PandasModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Orientation.Vertical:

                return str(self._data.index[section])


"""BEGIN APP"""

class loginScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PCGS Coin Inventory Tracker')
        self.setWindowIcon(QIcon('assets/coin.ico'))
        self.resize(self.screen().size().width(), self.screen().size().height()-80) # width,height

        """BEGIN WIDGITS"""
        self.title = QLabel("Third Coast \nSupply Company LLC")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
        self.user = QLabel("Login Form:")    
        self.user.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.pwd = QLabel("Password")
        self.pwd.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        self.unInput = QLineEdit()

        self.pwInput = QLineEdit()
        self.pwInput.setEchoMode(QLineEdit.EchoMode.Password)

        self.button1 = QPushButton('Register')
        self.button1.clicked.connect(self.register)

        self.button2 = QPushButton("Login")
        self.button2.clicked.connect(self.login)

        #Set window layout
        layout = QVBoxLayout()
        hbox = QHBoxLayout()

        layout.addStretch(1)
        hbox.addWidget(self.title)
        layout.addLayout(hbox)
        loginLayout = QGridLayout()
        loginLayout.addWidget(self.user, 1, 0)
        loginLayout.addWidget(self.pwd, 2, 0)
        loginLayout.addWidget(self.unInput, 1, 1, 1, 2)
        loginLayout.addWidget(self.pwInput, 2, 1, 1, 2)
        loginLayout.addWidget(self.button1, 3, 1)
        loginLayout.addWidget(self.button2, 3, 2)
        loginLayout.setContentsMargins(30,30,30,30)
        loginLayout.setSpacing(10)
        
        layout.addLayout(loginLayout)
        layout.addStretch(1)
        self.setLayout(layout)

    """DEFINE FUNCTIONS"""
    def login(self):
        username = self.unInput.text()
        pw = self.pwInput.text()
        if (username in [row for row in pd.read_csv(unpwFilepath)['un']]) and (pw in [row for row in pd.read_csv(unpwFilepath)['pw']]):
            loginWindow.close()
            homeAppWindow.show()
            with open("styles.css","r") as file:
                app.setStyleSheet(file.read())
             
            
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


class homeApp(QWidget):
    def __init__(self):
        super().__init__()


        # set window properties
        self.setWindowTitle('PCGS Coin Inventory Tracker')
        self.setWindowIcon(QIcon('assets/coin.ico'))
        self.resize(self.screen().size().width(), self.screen().size().height()-80)


        # New Invoice
        newInvoiceButton = QPushButton(QIcon("assets/coin.ico"), "New Invoice", self)
        newInvoiceButton.setGeometry(0, 0, 200, 200)
        newInvoiceButton.setIconSize(QSize(100,100))

        # New Purchase Order
        self.newPurchaseOrder = QPushButton(QIcon("assets/coin.ico"), "New Purchase Order", self)
        self.newPurchaseOrder.setGeometry(0, 0, 200, 200)
        self.newPurchaseOrder.setIconSize(QSize(100,100))
        self.newPurchaseOrder.clicked.connect(self.newPO)

        # New Contact
        newContact = QPushButton(QIcon("assets/coin.ico"), "New Contact", self)
        newContact.setGeometry(0, 0, 200, 200)
        newContact.setIconSize(QSize(100,100))

        # Run Report
        runReport = QPushButton(QIcon("assets/coin.ico"), "Run Report", self)
        runReport.setGeometry(0, 0, 100, 200)
        runReport.setIconSize(QSize(100,100))


        # create horizontal and vertical layout
        hbox = QHBoxLayout()
        hbox2 = QHBoxLayout()
        vbox = QVBoxLayout()

        # add buttons to horizontal layout
        hbox.addWidget(newInvoiceButton)
        hbox.addWidget(self.newPurchaseOrder)
        hbox.addWidget(newContact)
        hbox.addWidget(runReport)

        # add horizontal layout to vertical layout
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)
        vbox.addStretch(1)

        # set the main layout
        self.setLayout(vbox)


    """Define Functions"""
    def newPO(self):
        homeAppWindow.close()
        POAppWindow.show()


class POApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PCGS Coin Inventory Tracker')
        self.setWindowIcon(QIcon('assets\coin.ico'))
        self.resize(self.screen().size().width(), self.screen().size().height()-80)


        """BEGIN WIDGITS"""
        #Back Button
        backButton = QPushButton(QIcon("assets\FreeWebToolkit_1677391325.ico"),"", self)
        backButton.setGeometry(0, 0, 75, 100)
        backButton.setIconSize(QSize(80,80))
        backButton.clicked.connect(self.returnHomeScreen)
        

        #Top Label
        self.topLabel = QLabel('Third Coast \nSupply Company LLC')
        self.topLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)


        #Selector Field
        selectorFieldLayout = QHBoxLayout()

        self.dateFieldLabel = QLabel('Date')
        self.dateFieldLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.dateField = QtWidgets.QDateEdit(calendarPopup=True)
        self.dateField.setDateTime(QtCore.QDateTime.currentDateTime())
        
        self.poLabel = QLabel('PO')
        self.poLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.poField = QComboBox()
        self.poField.addItems(['100','101','102'])

        self.customerLabel = QLabel('Customer')
        self.customerLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.customerField = QComboBox()
        self.customerField.addItems(['Ricky Cardi','Nathan Lebherz','Anthony Cardi'])

        self.termsLabel = QLabel('Terms')
        self.termsLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.termsField = QComboBox()
        self.termsField.addItems(['Consignment','Sold','Split'])

        selectorFieldLayout.addWidget(self.dateFieldLabel)
        selectorFieldLayout.addWidget(self.dateField)
        selectorFieldLayout.addWidget(self.poLabel)
        selectorFieldLayout.addWidget(self.poField)
        selectorFieldLayout.addWidget(self.customerLabel)
        selectorFieldLayout.addWidget(self.customerField)
        selectorFieldLayout.addWidget(self.termsLabel)
        selectorFieldLayout.addWidget(self.termsField)

        #PO TABLE & BUTTONS
        bigHorizontalLayout = QHBoxLayout()
        verticalButtonLayout = QVBoxLayout()

        #Begin PO Table
        self.table = QtWidgets.QTableView()
        #data = createNewPOfunc()
        data = pd.DataFrame([
          [1, 9, 2],
          [1, 0, -1],
          [3, 5, 2],
          [3, 3, 2],
          [5, 8, 9]], 
          columns = ['A', 'B', 'C'], index=['Row 1', 'Row 2', 'Row 3', 'Row 4', 'Row 5'])
        ### USE HELPER PANDAS CLASS
        self.model = PandasModel(data)
        print(self.model)
        self.table.setModel(self.model)
        

        #Vertical Buttons
        self.saveButton = QPushButton('Save')
        verticalButtonLayout.addWidget(self.saveButton)

        self.closeButton = QPushButton('Close')
        verticalButtonLayout.addWidget(self.closeButton)

        self.printPOButton = QPushButton('Print PO')
        verticalButtonLayout.addWidget(self.printPOButton)

        self.printLabelsButton = QPushButton('Print Labels')
        verticalButtonLayout.addWidget(self.printLabelsButton)

        self.printOneLabelButton = QPushButton('Print One Label')
        verticalButtonLayout.addWidget(self.printOneLabelButton)

        bigHorizontalLayout.addWidget(self.table)
        bigHorizontalLayout.addLayout(verticalButtonLayout)



        #Set window layout
        pageLayout = QVBoxLayout()
        topLayout = QHBoxLayout()




        topLayout.addWidget(backButton)
        topLayout.addStretch(1)

        #Begin page layout
        pageLayout.addLayout(topLayout)
        pageLayout.addWidget(self.topLabel)
        pageLayout.addStretch(1)
        pageLayout.addLayout(selectorFieldLayout)
        pageLayout.addLayout(bigHorizontalLayout)


        pageLayout.addStretch(5)
        self.setLayout(pageLayout)




    """BEGIN FUNCTIONS"""
    def returnHomeScreen(self):
        POAppWindow.close()
        homeAppWindow.show()
        





"""CALL APPLICATION"""

app = QApplication([])
with open("styles.css","r") as file:
    app.setStyleSheet(file.read())
loginWindow = loginScreen()
homeAppWindow = homeApp()
POAppWindow = POApp()
loginWindow.show()
#POAppWindow.show()
app.exec()

print('DID YOU TRY TURNING IT OFF & ON AGAIN')

"""
HELPFUL LINKS:

For Structure: https://www.pythonguis.com/tutorials/pyqt6-layouts/

For CSS Styling with PyQt6: https://doc.qt.io/qtforpython/overviews/stylesheet-examples.html#style-sheet-usage

"""