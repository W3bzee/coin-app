from PyQt6.QtWidgets import (
    QWidget, QApplication, QVBoxLayout, QPushButton, QHBoxLayout, QDialog, QMessageBox,QInputDialog,
    QTextEdit, QGridLayout, QStackedLayout, QFrame,
    QLabel, QCheckBox, QComboBox, QListWidget, QLineEdit,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider, QTableWidget
)
from PyQt6.QtGui import *
from PyQt6 import QtCore, QtWidgets

from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize

"""Import Python Modules"""
import sys
import os
from datetime import datetime, date
import pandas as pd

from dotenv import load_dotenv
load_dotenv()
unpws = os.getenv('REGISTER')
unpwFilepath = './assets/unpw.csv'

"""Import Functions for Database"""
from Database.createNewPO import *
from Database.getCoinData import *
from Database.updatePOTable import *
#Serial Functions
from Database.updatePOTableSerial import *
from Database.getCoinDataSerial import *

import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from win32com.client import Dispatch



global app
global loginWindow
global homeAppWindow
global POAppWindow
global verticalLabelLayout

eventList = ['Type.ChildPolished',
'Type.StyleChange',
'Type.ParentChange',
'Type.Polish',
'Type.DynamicPropertyChange',
'Type.FontChange',
'Type.PaletteChange',
'Type.ChildPolished',
'Type.ChildPolished',
'Type.PolishRequest',
'Type.MetaCall',
'Type.Resize',
'Type.Timer',
'Type.MetaCall',
'Type.Timer',
'Type.Timer',
'Type.PaletteChange',
'Type.FontChange',
'Type.ToolTip',
'Type.FontChange',
'Type.PaletteChange',
'Type.StyleChange',
'Type.PaletteChange',
'Type.FontChange',
'Type.FontChange',
'Type.PaletteChange',
'Type.StyleChange',
'Type.Timer',
'Type.PaletteChange',
'Type.FontChange',
'Type.FontChange',
'Type.PaletteChange',
'Type.StyleChange',
'Type.ContentsRectChange',
'Type.PaletteChange',
'Type.FontChange',
'Type.FontChange',
'Type.PaletteChange',
'Type.StyleChange',
'Type.Move',
'Type.Wheel'
'Type.Resize',
'Type.Show',
'Type.ShowToParent',
'Type.WindowActivate',
'Type.Paint',
'Type.MetaCall',
'Type.LayoutRequest',
'Type.Timer',
'Type.UpdateLater',
'Type.Paint',
'Type.Enter',
'Type.Paint',
'Type.Paint',
'Type.ChildAdded',
'Type.InputMethodQuery',
'Type.FocusIn',
'Type.InputMethodQuery',
'Type.InputMethodQuery',
'Type.Paint',
'Type.Timer',
'Type.Paint',
'Type.Leave',
'Type.FocusAboutToChange',
'Type.FocusAboutToChange',
'Type.WindowDeactivate',
'Type.FocusOut',
'Type.Paint',
'Type.KeyPress',
'Type.KeyRelease',
'Type.ShortcutOverride',
'Type.ChildRemoved',
'Type.Hide',
'Type.WindowBlocked',
'Type.WindowUnblocked',]


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

        self.pwd = QLabel("Password:")
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
        #loginLayout.setContentsMargins(30,30,30,30)
        loginLayout.setSpacing(10)
        
        layout.addLayout(loginLayout)
        layout.addStretch(1)
        self.setLayout(layout)


        self.installEventFilter(self)


    """DEFINE FUNCTIONS"""
    def login(self):
        username = self.unInput.text()
        pw = self.pwInput.text()
        if (username in [row for row in pd.read_csv(unpwFilepath)['un']]) and (pw in [row for row in pd.read_csv(unpwFilepath)['pw']]):
            self.unInput.clear()
            self.pwInput.clear()
            loginWindow.close()
            with open("stylesheets\homeStyles.css","r") as file:
                app.setStyleSheet(file.read())
            homeAppWindow.show()

             
            
        else:
            self.noLoginPopup = QMessageBox(self)
            self.noLoginPopup.setWindowTitle('Incorrect Login or Password')
            self.noLoginPopup.setText('Incorrect login or password. Please try again. \
                                      \n\nIf this is your first time logging in, \
                                      \nplease click the register button. ')
            self.noLoginPopup.setIcon(QMessageBox.Icon.Warning)
            self.noLoginPopup.setStyleSheet('''QLabel {
            border: 2px solid red;
            padding: 2px;
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
            self.registerPopup.setStyleSheet('''QLabel {
            border: 2px solid red;
            padding: 2px;
            max-width: 2000%;
            }''')
            self.registerPopup.exec()
        else:
            self.failRegisterPopup = QMessageBox(self)
            self.failRegisterPopup.setWindowTitle('Registration Unsuccessful.')
            self.failRegisterPopup.setText('Incorrect Login. Please try again.')
            self.failRegisterPopup.setIcon(QMessageBox.Icon.Critical)
            self.failRegisterPopup.setStyleSheet('''QLabel {
            border: 2px solid red;
            padding: 2px;
            max-width: 2000%;
            }''')
            self.failRegisterPopup.exec()

    """BEGIN EVENT FILTER"""    
    def eventFilter(self, source, event):
        if event.type() == QKeyEvent.Type.KeyPress and event.key() == 16777220: 
           self.login() 
        return super().eventFilter(source,event)


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
        self.Title.setStyleSheet("""
        border: 2px solid rgb(189, 186, 186)
        """) 
        titleLayout.addWidget(self.Title)


        # New Invoice
        self.newInvoiceButton = QPushButton(QIcon("assets/newInvoice.ico"), "", self)
        self.newInvoiceButton.setGeometry(0, 0, 200, 200)
        self.newInvoiceButton.setIconSize(QSize(100,100))
        self.newInvoiceButton.clicked.connect(self.newInvoice)

        # New Invoice Label
        self.newInvoiceLabel = QLabel('New Invoice')
        self.newInvoiceLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # New Purchase Order
        self.newPurchaseOrder = QPushButton(QIcon("assets/newPO.ico"), "", self)
        self.newPurchaseOrder.setGeometry(0, 0, 200, 200)
        self.newPurchaseOrder.setIconSize(QSize(100,100))
        self.newPurchaseOrder.clicked.connect(self.newPO)

        # New Purchase Label
        self.newPurchaseOrderLabel = QLabel('New Purchase Order')
        self.newPurchaseOrderLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # New Contact
        self.newContact = QPushButton(QIcon("assets/newContact.ico"), "", self)
        self.newContact.setGeometry(0, 0, 200, 200)
        self.newContact.setIconSize(QSize(100,100))
        self.newContact.clicked.connect(self.newContactFunc)

        # New Contact Label
        self.newContactLabel = QLabel('New Contact')
        self.newContactLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Run Report
        self.runReport = QPushButton(QIcon("assets/runReport.ico"), "", self)
        self.runReport.setGeometry(0, 0, 100, 200)
        self.runReport.setIconSize(QSize(100,100))

        # Run Report Label
        self.runReportLabel = QLabel('Run Report')
        self.runReportLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Scanner Test Page
        self.Test = QPushButton("Scanner Test", self)
        self.Test.setGeometry(0, 0, 100, 200)
        self.Test.setIconSize(QSize(100,100))
        self.Test.clicked.connect(self.testerFunc)

        # Printer Test Page
        self.PrinterTest = QPushButton("Printer Test", self)
        self.PrinterTest.setGeometry(0, 0, 100, 200)
        self.PrinterTest.setIconSize(QSize(100,100))
        self.PrinterTest.clicked.connect(self.printerTesterFunc)

        #START PAGE LAYOUT

        # add buttons to horizontal layout
        hbox.addWidget(self.newInvoiceButton)
        hbox.addWidget(self.newPurchaseOrder)
        hbox.addWidget(self.newContact)
        hbox.addWidget(self.runReport)

        hbox2.addWidget(self.newInvoiceLabel)
        hbox2.addWidget(self.newPurchaseOrderLabel)
        hbox2.addWidget(self.newContactLabel)
        hbox2.addWidget(self.runReportLabel)

        # add horizontal layout to vertical layout
        vbox.addLayout(logoutLayout)
        vbox.addLayout(titleLayout)
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)
        vbox.addStretch(1)
        hbox3 = QHBoxLayout()
        hbox4 = QHBoxLayout()
        hbox3.addWidget(self.Test)
        hbox4.addWidget(self.PrinterTest)
        hbox3.addStretch(4)
        hbox4.addStretch(4)
        vbox.addLayout(hbox3)
        vbox.addSpacing(10)
        vbox.addLayout(hbox4)
        vbox.addStretch(1)

        # set the main layout
        self.setLayout(vbox)


    """Define Functions"""
    def logout(self):
        homeAppWindow.close()
        with open("stylesheets\loginStyles.css","r") as file:
            app.setStyleSheet(file.read())
        loginWindow.show()

    def newInvoice(self):
        homeAppWindow.close()
        with open("stylesheets\poStyles.css","r") as file:
            app.setStyleSheet(file.read())
        newInvoiceWindow.show()
        
    def newPO(self):
        homeAppWindow.close()
        with open("stylesheets\poStyles.css","r") as file:
            app.setStyleSheet(file.read())
        POAppWindow.show()
    
    def newContactFunc(self):
        homeAppWindow.close()
        with open("stylesheets\contactStyles.css","r") as file:
            app.setStyleSheet(file.read())
        newContactWindow.show()

    def testerFunc(self):
        homeAppWindow.close()
        scannerTesterWindow.show()

    def printerTesterFunc(self):
        homeAppWindow.close()
        PrinterTesterWindow.show()


class newInvoiceApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('New Invoice')
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
        self.topLabel.setStyleSheet("""
        border: 2px solid rgb(189, 186, 186)
        """)

        #Selector Field
        selectorFieldLayout = QHBoxLayout()

        self.dateFieldLabel = QLabel('Date')
        self.dateFieldLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.dateField = QtWidgets.QDateEdit(calendarPopup=True,date=date.today())

        self.poLabel = QLabel('Inv #')
        self.poLabel.setAlignment(Qt.AlignmentFlag.AlignRight)        
        self.poField = QComboBox()
        df = pd.read_csv('Database\Data\invoices.csv')
        listPOs = [x for x in pd.read_csv('Database\Data\invoices.csv')['Invoice'].values]
        listPOs = listPOs + [pd.read_csv('Database\Data\invoices.csv')['Invoice'].iloc[-1]+1]
        listPOs = sorted(listPOs, reverse=True)
        self.poField.addItems(list(map(str, listPOs)))

        self.customerLabel = QLabel('Customer')
        self.customerLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.customerField = QComboBox()
        self.customerField.addItems([str(x) for x in pd.read_csv('Database\Data\contacts.csv')['customer']])

        self.termsLabel = QLabel('Terms')
        self.termsLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.termsField = QComboBox()
        self.termsField.addItems(['Immediate', 'Approval' , 'Time to Pay'])

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
        self.table.installEventFilter(self)
        self.table.setColumnWidth(1,300)
        self.table.setColumnWidth(4,30)
        self.table.setColumnWidth(7,200)
        self.table.setColumnWidth(8,200)

        #Vertical Buttons
        self.saveButton = QPushButton('Save')
        self.saveButton.clicked.connect(self.saveInvoice)
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

    """BEGIN EVENT FILTER"""
    def eventFilter(self, source, event):
        if source == self.table and event.type() == QKeyEvent.Type.KeyPress and event.key() == 16777220:  #If you are in the table, and click Enter
            try:
                tableEntry = self.model._data['PCGS #'].iloc[-1]
                newDF = updateTable(pd.DataFrame(self.model._data),tableEntry)
                newDF = pd.concat([newDF, createNewPOfunc()])
                newIndex = ['{:03d}'.format(i) for i in range(1, len(newDF)+1)]
                newDF.index = newIndex
                self.model = PandasModel(newDF)
                self.table.setModel(self.model)
                self.table.installEventFilter(self)
                self.table.setColumnWidth(1,200)
                self.table.setColumnWidth(7,200)
                self.table.setColumnWidth(8,200)

            except IndexError:
                print(IndexError)
            except ValueError:
                print(ValueError)
        return super().eventFilter(source,event)

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
            print('HANDLED: {}'.format(ae))
        self.model = PandasModel(createNewPOfunc())
        self.table.setModel(self.model)
        listPOs = [x for x in pd.read_csv('Database\Data\invoices.csv')['Invoice'].values]
        listPOs = listPOs + [pd.read_csv('Database\Data\invoices.csv')['Invoice'].iloc[-1]+1]
        listPOs = sorted(listPOs, reverse=True)
        self.poField.clear()
        self.poField.addItems(list(map(str, listPOs)))
        self.saveButton.setEnabled(True)
       
        
        #Close Window
        newInvoiceWindow.close()
        with open("stylesheets/homeStyles.css","r") as file:
            app.setStyleSheet(file.read())
        homeAppWindow.show()


    def saveInvoice(self):
        ##Cleanup data for DB
        #dataToPush = self.model._data[:-1]
        #uniqueIDs = ['{}-{}'.format(self.poField.currentText(),x) for x in dataToPush.index]
        #dataToPush['Unique ID'] = uniqueIDs
        #print('\nPushing data to Invoice Database...\n\n{}'.format(dataToPush))
        ##Save Invoice Data to Invoices Database
        #dataToPush.to_csv('Database\Data\invoices.csv', index=False, header=not os.path.exists('Database\Data\invoices.csv'), mode='a')

        ##Remove PO Metadata
        #pd.DataFrame(data=[[datetime.now(),self.poField.currentText(),self.customerField.currentText(),self.termsField.currentText(),uniqueIDs]],columns=['Date', 'PO', 'Customer', 'Terms', 'UniqueIDs']).to_csv('Database\Data\purchaseOrders.csv', index=False, header=not os.path.exists('Database\Data\purchaseOrders.csv'), mode='a')
        #print('\nPushing to PO Database...\n\n{}\n\nSuccesfully Pushed'.format(pd.DataFrame(data=[[datetime.now(),self.poField.currentText(),self.customerField.currentText(),self.termsField.currentText(),uniqueIDs]],columns=['Date', 'PO', 'Customer', 'Terms', 'UniqueIDs'])))

        #Print Succesful Message
        self.savedToDBMessage = QMessageBox(self)
        self.savedToDBMessage.setWindowTitle('Invoice Creation Succesful.')
        self.savedToDBMessage.setText('The Invoice has been succesfully saved to the Database.')
        self.savedToDBMessage.setIcon(QMessageBox.Icon.Information)
        self.savedToDBMessage.exec()

        ## ADD OTHER GUI FUNCTIONAILITY
        self.saveButton.setEnabled(False)
        self.addressLabel = QPushButton('Print Labels')

        self.verticalLabelLayout.addWidget(self.addressLabel)
        

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
        self.topLabel.setStyleSheet("""
        border: 2px solid rgb(189, 186, 186)
        """)



        #Selector Field
        selectorFieldLayout = QHBoxLayout()

        self.dateFieldLabel = QLabel('Date')
        self.dateFieldLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.dateField = QtWidgets.QDateEdit(calendarPopup=True,date=date.today())

        self.poLabel = QLabel('PO')
        self.poLabel.setAlignment(Qt.AlignmentFlag.AlignRight)        
        self.poField = QComboBox()
        listPOs = [x for x in pd.read_csv('Database\Data\purchaseOrders.csv')['PO'].values]
        listPOs = listPOs + [pd.read_csv('Database\Data\purchaseOrders.csv')['PO'].iloc[-1]+1]
        listPOs = sorted(listPOs, reverse=True)
        self.poField.addItems(list(map(str, listPOs)))

        self.customerLabel = QLabel('Customer')
        self.customerLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.customerField = QComboBox()
        self.customerField.addItems([str(x) for x in pd.read_csv('Database\Data\contacts.csv')['customer']])

        self.termsLabel = QLabel('Terms')
        self.termsLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.termsField = QComboBox()
        self.termsField.addItems(['Consignment','Sold','Split'])


        # Create a button to trigger the popup window
        self.newCoinButton = QPushButton('Add New Coin')
        self.newCoinButton.clicked.connect(self.show_popup)


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
        selectorFieldLayout.addWidget(self.newCoinButton)

        """ BARCODE SECTION """
        # Bar Code Input
        self.BarCodeLabel = QLabel('Scan Bar Code:')
        self.BarCodeInput = QTextEdit()
        self.BarCodeInput.setMaximumSize(300,50)
        self.BarCodeButton = QPushButton('Run')
        self.BarCodeButton.clicked.connect(self.BarCodeRun)

        barcodeLayout = QHBoxLayout()
        barcodeLayout.addStretch(3)
        barcodeLayout.addWidget(self.BarCodeLabel)
        barcodeLayout.addWidget(self.BarCodeInput)
        barcodeLayout.addWidget(self.BarCodeButton)
        barcodeLayout.addStretch(3)

        #PO TABLE & BUTTONS
        bigHorizontalLayout = QHBoxLayout()
        self.verticalLabelLayout = QVBoxLayout()

        #Begin PO Table
        self.table = QtWidgets.QTableView()
        ### USE HELPER PANDAS CLASS
        self.model = PandasModel(createNewPOfunc())
        self.table.setModel(self.model)
        self.table.installEventFilter(self)
        self.table.setColumnWidth(1,300)
        self.table.setColumnWidth(4,30)
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
        pageLayout.addLayout(barcodeLayout)
        pageLayout.addLayout(bigHorizontalLayout)


        pageLayout.addStretch(5)
        self.setLayout(pageLayout)

    """BEGIN EVENT FILTER"""
    def eventFilter(self, source, event):
        if source == self.table and str(event.type()) not in eventList:
            self.succesfulConnectionMessage = QMessageBox(self)
            self.succesfulConnectionMessage.setWindowTitle('Event Popup')
            self.succesfulConnectionMessage.setText('EVENT #:\n{}'.format(event.type()))
            self.succesfulConnectionMessage.setIcon(QMessageBox.Icon.Information)
            self.succesfulConnectionMessage.setStyleSheet('''QLabel {
            border: 2px solid red;
            padding: 2px;
            max-width: 2000%;
            }''')
            self.succesfulConnectionMessage.exec()

        if source == self.table and event.type() == QKeyEvent.Type.KeyPress and event.key() == 16777220:  #If you are in the table, and click Enter
            try:
                tableEntry = self.model._data['PCGS #'].iloc[-1]
                newDF = updateTable(pd.DataFrame(self.model._data),tableEntry)
                newDF = pd.concat([newDF, createNewPOfunc()])
                newIndex = ['{:03d}'.format(i) for i in range(1, len(newDF)+1)]
                newDF.index = newIndex
                self.model = PandasModel(newDF)
                self.table.setModel(self.model)
                self.table.installEventFilter(self)
                self.table.setColumnWidth(1,300)
                self.table.setColumnWidth(4,30)
                self.table.setColumnWidth(7,200)
                self.table.setColumnWidth(8,200)

            except IndexError:
                print(IndexError)
            except ValueError:
                print(ValueError)
        return super().eventFilter(source,event)

    """BEGIN FUNCTIONS"""
    def show_popup(self):
        # Create a popup window to get user input
        text, ok = QInputDialog.getMultiLineText(self, 'Enter Coin Information', 'Please Enter the Coin Information',
                                                 'Pcgs_no: \nCountry: \nCoin_date: \nDenomination: \nVariety: \nPrefix: \nSuffix: \nQty_Minted: \nReference_no: \nRowLastUpdated: \ncoin_no: \nService: ')
        # Check if the user clicked 'OK' and retrieve the entered text
        if ok:
            coinData = text.split('\n')
            coinData = [x.split(': ').pop(1) for x in coinData]
            #Reformat CoinData
            coinDataDF = pd.DataFrame({'Pcgs_no':coinData[0],'Country':coinData[1],'Coin_date':coinData[2],'Denomination':coinData[3],'Variety':coinData[4],'Prefix':coinData[5],'Suffix':coinData[6],'Qty_Minted':coinData[7],'Reference_no':coinData[8],'RowLastUpdated':coinData[9],'coin_no':coinData[10],'Service':coinData[11]},index=[0])
            print('\nPushing data to Coin Database...\n\n{}'.format(coinDataDF))
            #Write the coin data to the CoinDB
            coinDataDF.to_csv('Database\Data\coinDB.csv', index=False, header=not os.path.exists('Database\Data\coinDB.csv'), mode='a')
    
    def showLeavingPopup(self):
        self.savedContactMessage = QMessageBox(self)
        self.savedContactMessage.setWindowTitle('Leave without saving?')
        self.savedContactMessage.setText('The data inputted is not saved.\nAre you sure you want to leave?')
        self.savedContactMessage.setIcon(QMessageBox.Icon.Warning)
        self.savedContactMessage.setStandardButtons(QMessageBox.StandardButton.Retry|
                               QMessageBox.StandardButton.Ok|
                               QMessageBox.StandardButton.Cancel)
        self.savedContactMessage.exec()


    def returnHomeScreen(self):
        if self.saveButton.isEnabled() and self.model._data.iloc[0][0] != '':
            self.savedContactMessage = QMessageBox(self)
            self.savedContactMessage.setWindowTitle('Leave without saving?')
            self.savedContactMessage.setText('The data inputted is not saved.\nAre you sure you want to leave?')
            self.savedContactMessage.setIcon(QMessageBox.Icon.Warning)
            self.savedContactMessage.setStandardButtons(QMessageBox.StandardButton.Save|QMessageBox.StandardButton.Close|QMessageBox.StandardButton.Cancel)
            result = self.savedContactMessage.exec()
            if result == QMessageBox.StandardButton.Save:
                self.savedContactMessage.close()
                self.savePO()
                return
            elif result == QMessageBox.StandardButton.Close:
                #Close Window
                print('closing')
                with open("stylesheets/homeStyles.css","r") as file:
                    app.setStyleSheet(file.read())
                homeAppWindow.show()
            elif result == QMessageBox.StandardButton.Cancel:
                self.savedContactMessage.close()
                return

        #Clear Data
        try:
            if not self.phoneLabel.isHidden():
                self.phoneLabel.setHidden(not self.phoneLabel.isHidden())
            if not self.addressLabel.isHidden():
                self.addressLabel.setHidden(not self.addressLabel.isHidden())
            if not self.printOneLabelButton.isHidden():
                self.printOneLabelButton.setHidden(not self.printOneLabelButton.isHidden())
        except AttributeError as ae:
            print('HANDLED: {}'.format(ae))
        self.model = PandasModel(createNewPOfunc())
        self.table.setModel(self.model)
        listPOs = [x for x in pd.read_csv('Database\Data\purchaseOrders.csv')['PO'].values]
        listPOs = listPOs + [pd.read_csv('Database\Data\purchaseOrders.csv')['PO'].iloc[-1]+1]
        listPOs = sorted(listPOs, reverse=True)
        self.BarCodeInput.clear()
        self.poField.clear()
        self.poField.addItems(list(map(str, listPOs)))
        self.saveButton.setEnabled(True)
       
        
        #Close Window
        POAppWindow.close()
        with open("stylesheets/homeStyles.css","r") as file:
            app.setStyleSheet(file.read())
        homeAppWindow.show()


    def savePO(self):
        ##Cleanup data for DB
        dataToPush = self.model._data[:-1]
        uniqueIDs = ['{}-{}'.format(self.poField.currentText(),x) for x in dataToPush.index]
        print('NON CRITICAL ERROR HERE')
        dataToPush['Unique ID'] = uniqueIDs
        print('\nPushing data to Coin Database...\n\n{}'.format(dataToPush))
        ##Save Coin Metadata to PurchaseOrderCoins to Database
        dataToPush.to_csv('Database\Data\purchaseOrderCoins.csv', index=False, header=not os.path.exists('Database\Data\purchaseOrderCoins.csv'), mode='a')

        ##Save PO Metadata
        pd.DataFrame(data=[[datetime.now(),self.poField.currentText(),self.customerField.currentText(),self.termsField.currentText(),uniqueIDs]],columns=['Date', 'PO', 'Customer', 'Terms', 'UniqueIDs']).to_csv('Database\Data\purchaseOrders.csv', index=False, header=not os.path.exists('Database\Data\purchaseOrders.csv'), mode='a')
        print('\nPushing to PO Database...\n\n{}\n\nSuccesfully Pushed'.format(pd.DataFrame(data=[[datetime.now(),self.poField.currentText(),self.customerField.currentText(),self.termsField.currentText(),uniqueIDs]],columns=['Date', 'PO', 'Customer', 'Terms', 'UniqueIDs'])))

        #Print Succesful Message
        self.savedToDBMessage = QMessageBox(self)
        self.savedToDBMessage.setWindowTitle('PO Creation Succesful.')
        self.savedToDBMessage.setText('The Purchase Order Information\nhas been succesfully saved to the Database.')
        self.savedToDBMessage.setIcon(QMessageBox.Icon.Information)
        self.savedToDBMessage.setStandardButtons(QMessageBox.StandardButton.Close)
        self.savedToDBMessage.exec()

        ## ADD OTHER GUI FUNCTIONAILITY
        self.saveButton.setEnabled(False)
        self.phoneLabel = QPushButton('Print PO')
        self.addressLabel = QPushButton('Print Labels')
        self.printOneLabelButton = QPushButton('Print One Label')


        self.verticalLabelLayout.addWidget(self.phoneLabel)
        self.verticalLabelLayout.addWidget(self.addressLabel)
        self.verticalLabelLayout.addWidget(self.printOneLabelButton)
        
    def BarCodeRun(self):
        try:
            tableEntry = self.BarCodeInput.toPlainText()
            print(len(tableEntry))
            newDF = updateTableSerial(pd.DataFrame(self.model._data),tableEntry)
            newDF = pd.concat([newDF, createNewPOfunc()])
            newIndex = ['{:03d}'.format(i) for i in range(1, len(newDF)+1)]
            newDF.index = newIndex
            self.model = PandasModel(newDF)
            self.table.setModel(self.model)
            self.table.installEventFilter(self)
            self.table.setColumnWidth(1,300)
            self.table.setColumnWidth(4,30)
            self.table.setColumnWidth(7,200)
            self.table.setColumnWidth(8,200)
        except IndexError:
            print(IndexError)
        except ValueError:
            print(ValueError)
        
        self.BarCodeInput.clear()
        self.BarCodeInput.setFocus()
        return 


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
        self.topLabel.setStyleSheet("""
        border: 2px solid rgb(189, 186, 186)
        """)

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
        customerBoxLayout.addStretch(1)
        customerBoxLayout.addWidget(self.customerLabel)
        customerBoxLayout.addWidget(self.customerEntry)
        customerBoxLayout.addStretch(1)

        #Email
        self.emailLabel = QLabel('Email:')
        self.emailLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.emailEntry = QLineEdit()
        emailBoxLayout.addStretch(1)
        emailBoxLayout.addWidget(self.emailLabel)
        emailBoxLayout.addWidget(self.emailEntry)
        emailBoxLayout.addStretch(1)

        #Phone
        self.phoneLabel = QLabel('Phone:')
        self.phoneLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.phoneEntry = QLineEdit()
        phoneBoxLayout.addStretch(1)
        phoneBoxLayout.addWidget(self.phoneLabel)
        phoneBoxLayout.addWidget(self.phoneEntry)
        phoneBoxLayout.addStretch(1)

        #Address
        self.addressLabel = QLabel('Address:')
        self.addressLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.addressEntry = QLineEdit()
        AddressBoxLayout.addStretch(1)
        AddressBoxLayout.addWidget(self.addressLabel)
        AddressBoxLayout.addWidget(self.addressEntry)  
        AddressBoxLayout.addStretch(1)

        #Vertical Entries
        verticalLayout.addLayout(customerBoxLayout)
        verticalLayout.addLayout(emailBoxLayout)
        verticalLayout.addLayout(phoneBoxLayout)
        verticalLayout.addLayout(AddressBoxLayout)

        #Save & Close Buttons
        newContactButtonsLayout = QHBoxLayout()

        self.saveNewContactButton = QPushButton('Save')
        self.saveNewContactButton.clicked.connect(self.saveNewContact)

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
    def saveNewContact(self):
        pd.DataFrame(data=[[self.customerEntry.text(),self.emailEntry.text(),self.phoneEntry.text(),self.addressEntry.text()]]).to_csv('Database\Data\contacts.csv', index=False, header=not os.path.exists('Database\Data\contacts.csv'), mode='a')
        #Print Succesful Contact Save
        self.savedContactMessage = QMessageBox(self)
        self.savedContactMessage.setWindowTitle('Contact Creation Succesful.')
        self.savedContactMessage.setText('The Contact was saved correctly.\nUnfortunately, you will have to close the application to see this populated in the PO')
        self.savedContactMessage.setIcon(QMessageBox.Icon.Information)
        self.savedContactMessage.exec()
        #os.execl(sys.executable, sys.executable, *sys.argv)

    def returnHomeScreen(self):
        self.customerEntry.setText('')
        self.emailEntry.setText('')
        self.phoneEntry.setText('')
        self.addressEntry.setText('')
        newContactWindow.close()
        with open("stylesheets/homeStyles.css","r") as file:
            app.setStyleSheet(file.read())
        homeAppWindow.show()


class ScannerTesterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(self.screen().size().width(), self.screen().size().height()-80)

        """BEGIN WIDGITS"""
        #Back Button
        hbox = QHBoxLayout()
        backButton = QPushButton(QIcon("assets\FreeWebToolkit_1677391325.ico"),"", self)
        backButton.setGeometry(0, 0, 75, 100)
        backButton.setIconSize(QSize(80,80))
        backButton.clicked.connect(self.returnHomeScreen)

        vbox = QVBoxLayout()
        # create a label in the center
    
        self.scanBoxLabel = QLabel('Try Scanning Below')
        self.scanBoxLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # create a QTextEdit widget to display the barcode data
        self.text_edit = QTextEdit()
        self.text_edit.setGeometry(0,0,100,100)
        self.text_edit.setStyleSheet('background-color: #f0f0f0;')

        # create a button to clear the entry form
        self.labelPrint = QPushButton('Clear Entry Form')
        self.labelPrint.setGeometry(0, 0, 200, 200)
        self.labelPrint.setIconSize(QSize(100,100))
        self.labelPrint.clicked.connect(self.clearData)

        #Place Widgets
        hbox.addWidget(backButton)
        hbox.addStretch(4)
        vbox.addLayout(hbox)
        vbox.addWidget(self.scanBoxLabel)
        vbox.addStretch(1)
        vbox.addWidget(self.text_edit)
        vbox.addWidget(self.labelPrint)
        vbox.addStretch(5)
        self.setLayout(vbox)

    
    def clearData(self):
        self.text_edit.clear()
        self.text_edit.setFocus()

    def returnHomeScreen(self):
        scannerTesterWindow.close()
        with open("stylesheets/homeStyles.css","r") as file:
            app.setStyleSheet(file.read())
        homeAppWindow.show()


class PrinterTesterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(self.screen().size().width(), self.screen().size().height()-80)

        """BEGIN WIDGITS"""
        #Back Button
        hbox = QHBoxLayout()
        backButton = QPushButton(QIcon("assets\FreeWebToolkit_1677391325.ico"),"", self)
        backButton.setGeometry(0, 0, 75, 100)
        backButton.setIconSize(QSize(80,80))
        backButton.clicked.connect(self.returnHomeScreen)

        vbox = QVBoxLayout()
        # create a label in the center


        #Place Widgets
        hbox.addWidget(backButton)
        hbox.addStretch(7)
        vbox.addLayout(hbox)
        vbox.addStretch(7)
        self.setLayout(vbox)


    def returnHomeScreen(self):
        PrinterTesterWindow.close()
        with open("stylesheets/homeStyles.css","r") as file:
            app.setStyleSheet(file.read())
        homeAppWindow.show()

"""CALL APPLICATION"""

app = QApplication([])
with open("stylesheets/loginStyles.css","r") as file:
    app.setStyleSheet(file.read())

loginWindow = loginScreen()
homeAppWindow = homeApp()
newInvoiceWindow = newInvoiceApp()
POAppWindow = POApp()
newContactWindow = newContactApp()
scannerTesterWindow = ScannerTesterApp()
PrinterTesterWindow = PrinterTesterApp()

loginWindow.show()
#homeAppWindow.show()
#POAppWindow.show()
#newContactWindow.show()
#newInvoiceWindow.show()

app.exec()



"""
HELPFUL LINKS:

For Structure: https://www.pythonguis.com/tutorials/pyqt6-layouts/

For CSS Styling with PyQt6: https://doc.qt.io/qtforpython/overviews/stylesheet-examples.html#style-sheet-usage

All Qt Modules: https://doc.qt.io/qtforpython/modules.html

"""