import sys
from PyQt6.QtWidgets import (
    QWidget, QApplication, QVBoxLayout, QPushButton, QHBoxLayout, QDialog, QMessageBox,QInputDialog,
    QTextEdit, QGridLayout, QStackedLayout, QFrame,
    QLabel, QCheckBox, QComboBox, QListWidget, QLineEdit,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider
)
from PyQt6.QtGui import *

from PyQt6.QtGui import QIcon, QFont, QPixmap, QMovie, QRegion
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
from datetime import date




global app
global loginWindow
global homeAppWindow
global POAppWindow
global verticalLabelLayout


"""HELPER CLASSES"""
class PandasModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if index.isValid():
            if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
                value = self._data.iloc[index.row(), index.column()]
                return str(value)
        

    def setData(self, index, value, role):
        if role == Qt.ItemDataRole.EditRole:
            self._data.iloc[index.row(), index.column()] = value
            return True
        return False

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])

    def flags(self, index):
        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable



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
            self.unInput.clear()
            self.pwInput.clear()
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

        logoutLayout = QHBoxLayout()
        titleLayout = QHBoxLayout()
        hbox = QHBoxLayout()
        hbox2 = QHBoxLayout()
        vbox = QVBoxLayout()      

        # set window properties
        self.setWindowTitle('PCGS Coin Inventory Tracker')
        self.setWindowIcon(QIcon('assets/coin.ico'))
        self.resize(self.screen().size().width(), self.screen().size().height()-80)

        #Logout Button
        self.logoutButton = QPushButton("Logout",self, clicked = self.logout)
        logoutLayout.addWidget(self.logoutButton)
        logoutLayout.addStretch(5)

        #Title
        self.Title = QLabel('Third Coast \nSupply Company LLC')
        self.Title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titleLayout.addWidget(self.Title)

        # New Invoice
        self.newInvoiceButton = QPushButton(QIcon("assets/coin.ico"), "New Invoice", self)
        self.newInvoiceButton.setGeometry(0, 0, 200, 200)
        self.newInvoiceButton.setIconSize(QSize(100,100))

        # New Purchase Order
        self.newPurchaseOrder = QPushButton(QIcon("assets/coin.ico"), "New Purchase Order", self)
        self.newPurchaseOrder.setGeometry(0, 0, 200, 200)
        self.newPurchaseOrder.setIconSize(QSize(100,100))
        self.newPurchaseOrder.clicked.connect(self.newPO)

        # New Contact
        self.newContact = QPushButton(QIcon("assets/coin.ico"), "New Contact", self)
        self.newContact.setGeometry(0, 0, 200, 200)
        self.newContact.setIconSize(QSize(100,100))
        self.newContact.clicked.connect(self.newContactFunc)
        # Run Report
        self.runReport = QPushButton(QIcon("assets/coin.ico"), "Run Report", self)
        self.runReport.setGeometry(0, 0, 100, 200)
        self.runReport.setIconSize(QSize(100,100))


        #START PAGE LAYOUT

        # add buttons to horizontal layout
        hbox.addWidget(self.newInvoiceButton)
        hbox.addWidget(self.newPurchaseOrder)
        hbox.addWidget(self.newContact)
        hbox.addWidget(self.runReport)

        # add horizontal layout to vertical layout
        vbox.addLayout(logoutLayout)
        vbox.addLayout(titleLayout)
        vbox.addStretch(1)

        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)
        vbox.addStretch(1)

        # set the main layout
        self.setLayout(vbox)


    """Define Functions"""
    def logout(self):
        homeAppWindow.close()
        loginWindow.show()

    def newPO(self):
        homeAppWindow.close()
        POAppWindow.show()
    
    def newContactFunc(self):
        homeAppWindow.close()
        newContactWindow.show()
    

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
        self.topLabel = QLabel('Third Coast\nSupply Company LLC')
        self.topLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)


        #Selector Field
        selectorFieldLayout = QHBoxLayout()

        self.dateFieldLabel = QLabel('Date')
        self.dateFieldLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.dateField = QtWidgets.QDateEdit(calendarPopup=True,date=date.today())

        
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

        selectorFieldLayout.addStretch(1)
        selectorFieldLayout.addWidget(self.dateFieldLabel)
        selectorFieldLayout.addWidget(self.dateField)
        selectorFieldLayout.addWidget(self.poLabel)
        selectorFieldLayout.addWidget(self.poField)
        selectorFieldLayout.addWidget(self.customerLabel)
        selectorFieldLayout.addWidget(self.customerField)
        selectorFieldLayout.addWidget(self.termsLabel)
        selectorFieldLayout.addWidget(self.termsField)
        selectorFieldLayout.addStretch(1)

        #PO TABLE & BUTTONS
        bigHorizontalLayout = QHBoxLayout()
        self.verticalLabelLayout = QVBoxLayout()

        #Begin PO Table
        self.table = QtWidgets.QTableView()
        ### USE HELPER PANDAS CLASS
        self.model = PandasModel(createNewPOfunc())
        self.table.setModel(self.model)
        self.table.setColumnWidth(1,200)
        self.table.setColumnWidth(7,200)
        self.table.setColumnWidth(8,200)

        #Vertical Buttons
        self.saveButton = QPushButton('Save')
        self.saveButton.clicked.connect(self.savePO)
        self.verticalLabelLayout.addWidget(self.saveButton)

        bigHorizontalLayout.addWidget(self.table)
        bigHorizontalLayout.addLayout(self.verticalLabelLayout)



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
        #Clear Data
        try:
            if not self.phoneLabel.isHidden():
                self.phoneLabel.setHidden(not self.phoneLabel.isHidden())
            if not self.addressLabel.isHidden():
                self.addressLabel.setHidden(not self.addressLabel.isHidden())
            if not self.printOneLabelButton.isHidden():
                self.printOneLabelButton.setHidden(not self.printOneLabelButton.isHidden())
        except AttributeError as ae:
            print('Good to go dawg')
        self.model = PandasModel(createNewPOfunc())
        self.table.setModel(self.model)
        
        #Close Window
        POAppWindow.close()
        homeAppWindow.show()

    def savePO(self):

        ## ADD OTHER GUI FUNCTIONAILITY
        self.phoneLabel = QPushButton('Print PO')
        self.verticalLabelLayout.addWidget(self.phoneLabel)

        self.addressLabel = QPushButton('Print Labels')
        self.verticalLabelLayout.addWidget(self.addressLabel)

        self.printOneLabelButton = QPushButton('Print One Label')
        self.verticalLabelLayout.addWidget(self.printOneLabelButton)

        
        

class newContactApp(QWidget):
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

        #Customer Label & Info
        customerBoxLayout = QHBoxLayout()
        emailBoxLayout = QHBoxLayout()
        phoneBoxLayout = QHBoxLayout()
        AddressBoxLayout = QHBoxLayout()
        verticalLayout = QVBoxLayout()

        #Customer
        self.customerLabel = QLabel('Customer:')
        self.customerLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.customerEntry = QLineEdit()
        customerBoxLayout.addWidget(self.customerLabel)
        customerBoxLayout.addWidget(self.customerEntry)

        #Email
        self.emailLabel = QLabel('Email:')
        self.emailLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.emailEntry = QLineEdit()
        emailBoxLayout.addWidget(self.emailLabel)
        emailBoxLayout.addWidget(self.emailEntry)

        #Phone
        self.phoneLabel = QLabel('Phone:')
        self.phoneLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.phoneEntry = QLineEdit()
        phoneBoxLayout.addWidget(self.phoneLabel)
        phoneBoxLayout.addWidget(self.phoneEntry)

        #Address
        self.addressLabel = QLabel('Address:')
        self.addressLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.addressEntry = QLineEdit()
        AddressBoxLayout.addWidget(self.addressLabel)
        AddressBoxLayout.addWidget(self.addressEntry)  

        #Vertical Entries
        verticalLayout.addLayout(customerBoxLayout)
        verticalLayout.addLayout(emailBoxLayout)
        verticalLayout.addLayout(phoneBoxLayout)
        verticalLayout.addLayout(AddressBoxLayout)

        #Save & Close Buttons
        newContactButtonsLayout = QHBoxLayout()

        self.saveNewContactButton = QPushButton('Save')

        newContactButtonsLayout.addStretch(1)
        newContactButtonsLayout.addWidget(self.saveNewContactButton)
        newContactButtonsLayout.addStretch(1)

        #Set top layout
        topLayout = QHBoxLayout()
        topLayout.addWidget(backButton)
        topLayout.addStretch(1)

        #Begin page layout
        pageLayout = QVBoxLayout()
        pageLayout.addLayout(topLayout)
        pageLayout.addWidget(self.topLabel)
        pageLayout.addStretch(1)
        pageLayout.addLayout(verticalLayout)
        pageLayout.addLayout(newContactButtonsLayout)

        pageLayout.addStretch(5)
        self.setLayout(pageLayout)


    """BEGIN FUNCTIONS"""
    def returnHomeScreen(self):
        self.customerEntry.setText('')
        self.emailEntry.setText('')
        self.phoneEntry.setText('')
        self.addressEntry.setText('')
        newContactWindow.close()
        homeAppWindow.show()



"""CALL APPLICATION"""

app = QApplication([])
with open("stylesContactApp.css","r") as file:
    app.setStyleSheet(file.read())

loginWindow = loginScreen()
homeAppWindow = homeApp()
POAppWindow = POApp()
newContactWindow = newContactApp()

loginWindow.show()
#homeAppWindow.show()
#POAppWindow.show()
#newContactWindow.show()

app.exec()

print('DID YOU TRY TURNING IT OFF & ON AGAIN')

"""
HELPFUL LINKS:

For Structure: https://www.pythonguis.com/tutorials/pyqt6-layouts/

For CSS Styling with PyQt6: https://doc.qt.io/qtforpython/overviews/stylesheet-examples.html#style-sheet-usage

All Qt Modules: https://doc.qt.io/qtforpython/modules.html

"""