from PyQt6.QtWidgets import (
    QWidget, QApplication, QVBoxLayout, QPushButton, QHBoxLayout, QDialog, QMessageBox,QInputDialog,
    QTextEdit, QGridLayout, QStackedLayout, QFrame,
    QLabel, QCheckBox, QComboBox, QListWidget, QLineEdit,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider, QTableWidget, QStyledItemDelegate
)
from PyQt6.QtGui import *
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QFont

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
# Purchase Order Fuctions
from Database.createNewPO import *
from Database.getCoinData import *
from Database.updatePOTable import *
from Database.editExistingPO import *
# Serial Functions
from Database.updatePOTableSerial import *
from Database.getCoinDataSerial import *
# Invoice Functions
from Database.createNewInvoice import *
from Database.updateInvoiceTableSerial import *
from Database.getCoinInvoiceSerial import *
# Report Functions
from Database.inventoryReport import *


""" Import functions for Printer """
from win32com.client import Dispatch
from assets.printCoinLabel import *



global app
global loginWindow
global homeAppWindow
global POAppWindow
global verticalLabelLayout

""" SET REV VERSION """
revVersion = 'v0.02.05'
lastUpdate = '2/24/2024'

""" SET FONTS """
font = "Perpetua Titling MT"
font2 = 'Adobe Devanagari'

custom_font1 = QFont(font,64)
custom_font2 = QFont(font2)



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

class NonEditableDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        # Override the default behavior to prevent editing
        return None

"""BEGIN APP"""

class loginScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PCGS Coin Inventory Tracker')
        self.setWindowIcon(QIcon('assets/coin.ico'))
        self.resize(self.screen().size().width(), self.screen().size().height()-80) # width,height

        # Create a QLabel widget for the background image
        background_label = QLabel(self)
        pixmap = QPixmap('assets/bridge_background.jpg')
        background_label.setPixmap(pixmap)
        background_label.setGeometry(0, 0, self.width(), self.height())

        """BEGIN WIDGITS"""
        self.title = QLabel("Third Coast\nSupply Company LLC")
        self.title.setObjectName('title')
        self.title.setFont(custom_font1)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
        self.user = QLabel("Login Form:")
        self.user.setFont(custom_font2)    
        self.user.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.pwd = QLabel("Password:")
        self.pwd.setFont(custom_font2)  
        self.pwd.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        self.unInput = QLineEdit()

        self.pwInput = QLineEdit()
        self.pwInput.setEchoMode(QLineEdit.EchoMode.Password)

        self.button1 = QPushButton('Register')
        self.button1.setFont(custom_font2)  
        self.button1.clicked.connect(self.register)

        self.button2 = QPushButton("Login")
        self.button2.setFont(custom_font2)
        self.button2.clicked.connect(self.login)

        self.revVersion = QLabel('Version: {}\nLast Update: {}'.format(revVersion,lastUpdate))
        self.revVersion.setObjectName('rev')
        self.revVersion.setAlignment(Qt.AlignmentFlag.AlignRight)

        #Set window layout
        layout = QVBoxLayout()
        hbox = QHBoxLayout()

        layout.addStretch(3)
        hbox.addWidget(self.title)
        layout.addStretch(2)
        layout.addLayout(hbox)
        loginLayout = QGridLayout()
        loginLayout.addWidget(self.user, 1, 0)
        loginLayout.addWidget(self.pwd, 2, 0)
        loginLayout.addWidget(self.unInput, 1, 1, 1, 2)
        loginLayout.addWidget(self.pwInput, 2, 1, 1, 2)
        loginLayout.addWidget(self.button1, 3, 1)
        loginLayout.addWidget(self.button2, 3, 2)
        #loginLayout.setContentsMargins()
        loginLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        loginLayout.setSpacing(10)
        
        layout.addLayout(loginLayout)

        layout.addStretch(7)
        layout.addWidget(self.revVersion)

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
            self.noLoginPopup.setText('Incorrect login or password. Please try again.\
                                      \n\nIf this is your first time logging in,\
                                      please click the register button. ')
            self.noLoginPopup.setIcon(QMessageBox.Icon.Warning)
            self.noLoginPopup.setStyleSheet('''QLabel {
            border: 2px solid red;
            padding: 2px;
            max-width: 2000%;
            }''')
            self.noLoginPopup.exec()

    def register(self):
        self.registerKey, ok = QInputDialog.getText(self,'User Register Account Key', 'Please Enter The Registration Key', QLineEdit.EchoMode.Password)
        
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
        elif ok and (self.registerKey != unpws):
            self.failRegisterPopup = QMessageBox(self)
            self.failRegisterPopup.setWindowTitle('Registration Unsuccessful.')
            self.failRegisterPopup.setText('Incorrect Registration Key. Please try again.')
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

        # Create a QLabel widget for the background image
        background_label = QLabel(self)
        pixmap = QPixmap('assets/bridge_background.jpg')
        background_label.setPixmap(pixmap)
        background_label.setGeometry(0, 0, self.width(), self.height())

        #Logout Button
        self.logoutButton = QPushButton("Logout",self, clicked = self.logout)
        logoutLayout.addWidget(self.logoutButton)
        logoutLayout.addStretch(5)

        #Title
        self.Title = QLabel('Third Coast \nSupply Company LLC')
        self.Title.setFont(custom_font1)  
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
        self.newInvoiceLabel.setFont(custom_font2)  
        self.newInvoiceLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # New Purchase Order
        self.newPurchaseOrder = QPushButton(QIcon("assets/newPO.ico"), "", self)
        self.newPurchaseOrder.setGeometry(0, 0, 200, 200)
        self.newPurchaseOrder.setIconSize(QSize(100,100))
        self.newPurchaseOrder.clicked.connect(self.newPO)

        # New Purchase Label
        self.newPurchaseOrderLabel = QLabel('New Purchase Order')
        self.newPurchaseOrderLabel.setFont(custom_font2)
        self.newPurchaseOrderLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # New Contact
        self.newContact = QPushButton(QIcon("assets/newContact.ico"), "", self)
        self.newContact.setGeometry(0, 0, 200, 200)
        self.newContact.setIconSize(QSize(100,100))
        self.newContact.clicked.connect(self.newContactFunc)

        # New Contact Label
        self.newContactLabel = QLabel('New Contact')
        self.newContactLabel.setFont(custom_font2)
        self.newContactLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Run Report
        self.runReport = QPushButton(QIcon("assets/runReport.ico"), "", self)
        self.runReport.setGeometry(0, 0, 100, 200)
        self.runReport.setIconSize(QSize(100,100))
        self.runReport.clicked.connect(self.inventoryReport)

        # Run Report Label
        self.runReportLabel = QLabel('Inventory Report')
        self.runReportLabel.setFont(custom_font2)
        self.runReportLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Scanner Test Page
        self.ScannerTest = QPushButton("Scanner Test", self)
        self.ScannerTest.setFont(custom_font2)
        self.ScannerTest.setGeometry(0, 0, 100, 200)
        self.ScannerTest.setIconSize(QSize(100,100))
        self.ScannerTest.clicked.connect(self.testerFunc)

        # Printer Test Page
        self.PrinterTest = QPushButton("Printer Test", self)
        self.PrinterTest.setFont(custom_font2)
        self.PrinterTest.setGeometry(0, 0, 100, 200)
        self.PrinterTest.setIconSize(QSize(100,100))
        self.PrinterTest.clicked.connect(self.printerTesterFunc)

        self.revVersion = QLabel('Version: {}\nLast Update: {}'.format(revVersion,lastUpdate))
        self.revVersion.setObjectName('rev')
        self.revVersion.setAlignment(Qt.AlignmentFlag.AlignRight)

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
        hbox3.addWidget(self.ScannerTest)
        hbox4.addWidget(self.PrinterTest)
        hbox3.addStretch(4)
        hbox4.addStretch(4)
        vbox.addLayout(hbox3)
        vbox.addSpacing(10)
        vbox.addLayout(hbox4)
        vbox.addStretch(1)
        vbox.addWidget(self.revVersion)

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
        with open("stylesheets\\newInvoice.css","r") as file:
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

    def inventoryReport(self):
        homeAppWindow.close()
        with open('stylesheets\inventoryReport.css',"r") as file:
            app.setStyleSheet(file.read())
        inventoryReportWindow.show()

    def testerFunc(self):
        homeAppWindow.close()
        scannerTesterWindow.show()

    def printerTesterFunc(self):
        homeAppWindow.close()
        with open('stylesheets\printerTestStyles.css',"r") as file:
            app.setStyleSheet(file.read())
        PrinterTesterWindow.show()


class newInvoiceApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('New Invoice')
        self.setWindowIcon(QIcon('assets\coin.ico'))
        self.resize(self.screen().size().width(), self.screen().size().height()-80)


        # Create a QLabel widget for the background image
        background_label = QLabel(self)
        pixmap = QPixmap('assets/bridge_background.jpg')
        background_label.setPixmap(pixmap)
        background_label.setGeometry(0, 0, self.width(), self.height())

        """BEGIN WIDGITS"""
        #Back Button
        backButton = QPushButton(QIcon("assets\\backButton.ico"),"", self)
        backButton.setObjectName('backButton')
        backButton.setGeometry(0, 0, 75, 100)
        backButton.setIconSize(QSize(80,80))
        backButton.clicked.connect(self.returnHomeScreen)        

        #Top Label
        self.topLabel = QLabel('Third Coast\nSupply Company LLC')
        self.topLabel.setFont(custom_font1)
        self.topLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.topLabel.setStyleSheet("""
        border: 2px solid rgb(189, 186, 186)
        """)

        #Selector Field
        selectorFieldLayout = QHBoxLayout()

        self.dateFieldLabel = QLabel('Date')
        self.dateFieldLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.dateFieldLabel.setFont(custom_font2)
        self.dateField = QtWidgets.QDateEdit(calendarPopup=True,date=date.today())

        self.invoiceLabel = QLabel('Inv #')
        self.invoiceLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.invoiceLabel.setFont(custom_font2)        
        self.invoiceField = QComboBox()
        df = pd.read_csv('Database\Data\invoices.csv')
        listInvoices = [x for x in pd.read_csv('Database\Data\invoices.csv')['Invoice'].values]
        listInvoices = listInvoices + [pd.read_csv('Database\Data\invoices.csv')['Invoice'].iloc[-1]+1]
        listInvoices = sorted(listInvoices, reverse=True)
        self.invoiceField.addItems(list(map(str, listInvoices)))

        self.customerLabel = QLabel('Customer')
        self.customerLabel.setFont(custom_font2)
        self.customerLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.customerField = QComboBox()
        self.customerField.addItems([str(x) for x in pd.read_csv('Database\Data\contacts.csv')['customer']])

        self.termsLabel = QLabel('Terms')
        self.termsLabel.setFont(custom_font2)
        self.termsLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.termsField = QComboBox()
        self.termsField.addItems(['Immediate', 'Approval' , 'Time to Pay'])

        """ BARCODE SECTION """
        # Bar Code Input
        self.InvoiceBarCodeLabel = QLabel('Scan TCS Bar Code:')
        self.InvoiceBarCodeLabel.setFont(custom_font2)
        self.InvoiceBarCodeInput = QTextEdit()
        self.InvoiceBarCodeInput.setMaximumSize(300,50)
        self.InvoiceBarCodeInput.setPlaceholderText('Scan Here')
        self.InvoiceBarCodeInput.installEventFilter(self)
        self.InvoiceBarCodeButton = QPushButton('Run')
        self.InvoiceBarCodeButton.setFont(custom_font2)

        barcodeLayout = QHBoxLayout()
        barcodeLayout.addStretch(3)
        barcodeLayout.addWidget(self.InvoiceBarCodeLabel)
        barcodeLayout.addWidget(self.InvoiceBarCodeInput)
        barcodeLayout.addWidget(self.InvoiceBarCodeButton)
        barcodeLayout.addStretch(3)

        selectorFieldLayout.addStretch(1)
        selectorFieldLayout.addWidget(self.dateFieldLabel)
        selectorFieldLayout.addWidget(self.dateField)
        selectorFieldLayout.addWidget(self.invoiceLabel)
        selectorFieldLayout.addWidget(self.invoiceField)
        selectorFieldLayout.addWidget(self.customerLabel)
        selectorFieldLayout.addWidget(self.customerField)
        selectorFieldLayout.addWidget(self.termsLabel)
        selectorFieldLayout.addWidget(self.termsField)
        selectorFieldLayout.addStretch(1)

        #INVOICE TABLE & BUTTONS
        bigHorizontalLayout = QHBoxLayout()
        self.verticalLabelLayout = QVBoxLayout()

        #Begin INVOICE Table
        self.Invoicetable = QtWidgets.QTableView()
        ### USE HELPER PANDAS CLASS
        self.Invoicemodel = PandasModel(createNewInvoicefunc())
        self.Invoicetable.setModel(self.Invoicemodel)
        self.Invoicetable.verticalHeader().setVisible(False)
        self.Invoicetable.setColumnWidth(2,300)
        self.Invoicetable.setColumnWidth(7,200)
        self.Invoicetable.setColumnWidth(8,200)
        self.Invoicetable.resizeColumnToContents(1)
        self.Invoicetable.resizeColumnToContents(3)
        self.Invoicetable.resizeColumnToContents(5)

        #Vertical Buttons
        self.saveInvoiceButton = QPushButton('Save')
        self.saveInvoiceButton.setFont(custom_font2)
        self.saveInvoiceButton.clicked.connect(self.saveInvoice)
        self.verticalLabelLayout.addWidget(self.saveInvoiceButton)

        bigHorizontalLayout.addSpacing(20)
        bigHorizontalLayout.addWidget(self.Invoicetable)
        bigHorizontalLayout.addSpacing(20)
        bigHorizontalLayout.addLayout(self.verticalLabelLayout)

        #Set window layout
        pageLayout = QVBoxLayout()
        topLayout = QHBoxLayout()

        topLayout.addWidget(backButton)
        topLayout.addStretch(4)
        topLayout.addWidget(self.topLabel)
        topLayout.addStretch(5)

        #Begin page layout
        pageLayout.addLayout(topLayout)
#
        pageLayout.addLayout(selectorFieldLayout)
        pageLayout.addLayout(barcodeLayout)
        pageLayout.addLayout(bigHorizontalLayout)
        pageLayout.addSpacing(60)
        self.setLayout(pageLayout)

    """BEGIN EVENT FILTER"""
    def eventFilter(self, source, event):
        if event.type() == QKeyEvent.Type.KeyRelease and event.key() == 16777220:  #If you click Enter  ###   39   ###
            tableEntry = self.InvoiceBarCodeInput.toPlainText()
            tableEntry = tableEntry.replace(' ','')


            if tableEntry.__contains__('\n'):
                tableEntry = tableEntry.replace('\n','')
                
            if len(self.InvoiceBarCodeInput.toPlainText()) == 1:
                self.InvoiceBarCodeInput.clear()
                self.InvoiceBarCodeInput.setFocus()
                self.InvoiceBarCodeInput.setPlaceholderText('Scan Here')
                return False#super().eventFilter(source,event)


            if tableEntry in self.Invoicemodel._data[:-1]['ID #'].values:
                self.InvoiceBarCodeInput.clear()
                self.InvoiceBarCodeInput.setFocus()
                self.InvoiceBarCodeInput.setPlaceholderText('Scan Here')

                #Popup Window
                self.savedContactMessage = QMessageBox(self)
                self.savedContactMessage.setWindowTitle('Duplicate Data')
                self.savedContactMessage.setText('That specific TCS Barcode is already in this invoice.\n\
                                                 Click Apply to add the row again')
                self.savedContactMessage.setIcon(QMessageBox.Icon.Warning)
                self.savedContactMessage.setStandardButtons(QMessageBox.StandardButton.Apply|QMessageBox.StandardButton.Cancel)
                result = self.savedContactMessage.exec()
                if result == QMessageBox.StandardButton.Cancel:
                    self.savedContactMessage.close()
                    return False
                elif result == QMessageBox.StandardButton.Apply:
                    self.savedContactMessage.close()
            else:
                try:
                    newInvoiceDF = updateInvoiceTableSerial(pd.DataFrame(self.Invoicemodel._data),tableEntry)
                    newDF = pd.concat([newInvoiceDF, createNewInvoicefunc()])
                    self.Invoicemodel = PandasModel(newDF)
                    self.Invoicetable.setModel(self.Invoicemodel)
                    self.Invoicetable.verticalHeader().setVisible(False)
                    self.Invoicetable.setColumnWidth(2,300)
                    self.Invoicetable.setColumnWidth(7,200)
                    self.Invoicetable.setColumnWidth(8,200)
                    self.Invoicetable.resizeColumnToContents(1)
                    self.Invoicetable.resizeColumnToContents(3)
                    self.Invoicetable.resizeColumnToContents(5)


            
                except IndexError:
                    print(IndexError)
                    self.savedToInvoiceDBMessage = QMessageBox(self)
                    self.savedToInvoiceDBMessage.setWindowTitle('Unsuccesfully found the entry of: {}'.format(tableEntry))
                    self.savedToInvoiceDBMessage.setText('Please scan a Third Coast Supply printed barcode')
                    self.savedToInvoiceDBMessage.setIcon(QMessageBox.Icon.Warning)
                    self.savedToInvoiceDBMessage.setStandardButtons(QMessageBox.StandardButton.Close)
                    self.savedToInvoiceDBMessage.setStyleSheet("QMessageBox { min-width:500px }")
                    self.savedToInvoiceDBMessage.exec()
                except ValueError:
                    print(ValueError)
                    self.savedToInvoiceDBMessage = QMessageBox(self)
                    self.savedToInvoiceDBMessage.setWindowTitle('Unsuccesfully found the entry of: {}'.format(tableEntry))
                    self.savedToInvoiceDBMessage.setText('Please scan a Third Coast Supply printed barcode')
                    self.savedToInvoiceDBMessage.setIcon(QMessageBox.Icon.Warning)
                    self.savedToInvoiceDBMessage.setStandardButtons(QMessageBox.StandardButton.Close)
                    self.savedToInvoiceDBMessage.setStyleSheet("QMessageBox { min-width:500px }")
                    self.savedToInvoiceDBMessage.exec()
            

            self.InvoiceBarCodeInput.clear()
            self.InvoiceBarCodeInput.setFocus()
            self.InvoiceBarCodeInput.setPlaceholderText('Scan Here')

        return super().eventFilter(source,event)

    """BEGIN FUNCTIONS"""
    def returnHomeScreen(self):
        #Clear Data
        self.Invoicemodel = PandasModel(createNewInvoicefunc())
        self.Invoicetable.setModel(self.Invoicemodel)
        listPOs = [x for x in pd.read_csv('Database\Data\invoices.csv')['Invoice'].values]
        listPOs = listPOs + [pd.read_csv('Database\Data\invoices.csv')['Invoice'].iloc[-1]+1]
        listPOs = sorted(listPOs, reverse=True)
        self.invoiceField.clear()
        self.invoiceField.addItems(list(map(str, listPOs)))
        self.saveInvoiceButton.setEnabled(True)
        self.saveInvoiceButton.setStyleSheet("stylesheets/newInvoice.css")
       
        #Close Window
        newInvoiceWindow.close()
        with open("stylesheets/homeStyles.css","r") as file:
            app.setStyleSheet(file.read())
        homeAppWindow.show()


    def saveInvoice(self):
        ##Cleanup data for DB
        tableData = self.Invoicemodel._data[:-1]
        if tableData.empty or tableData['PCGS #'][-1] == '':
            self.savedToInvoiceDBMessage = QMessageBox(self)
            self.savedToInvoiceDBMessage.setWindowTitle('Save Unsuccesful')
            self.savedToInvoiceDBMessage.setText('Save unsuccesful as the dataframe is empty.\nPlease scan a Third Coast Supply barcode & click "enter".')
            self.savedToInvoiceDBMessage.setIcon(QMessageBox.Icon.Warning)
            self.savedToInvoiceDBMessage.setStandardButtons(QMessageBox.StandardButton.Close)
            self.savedToInvoiceDBMessage.setStyleSheet("QMessageBox { min-width:500px }")
            self.savedToInvoiceDBMessage.exec()
            return
        ##Cleanup data for DB
        print('\nPushing data to Invoice Coin Database...\n\n{}'.format(tableData))

        ##Save Coin Metadata to inventoryCoins Database
        tableData.to_csv('Database\Data\invoiceCoins.csv', index=False, header=not os.path.exists('Database\Data\invoiceCoins.csv'), mode='a')

        uniqueIDs = tableData['ID #'].iloc[:].to_list()
        uniqueIDs = [x for x in uniqueIDs if x != '']
        
        ##Save Invoice Metadata
        pd.DataFrame(data=[[datetime.now(),self.invoiceField.currentText(),self.customerField.currentText(),self.termsField.currentText(),uniqueIDs]],columns=['Date', 'Invoice', 'Customer', 'Terms', 'UniqueIDs']).to_csv('Database\Data\invoices.csv', index=False, header=not os.path.exists('Database\Data\invoices.csv'), mode='a')
        print('\nPushing to Invoice to Database...\n\n{}\n\nSuccesfully Pushed'.format(pd.DataFrame(data=[[datetime.now(),self.invoiceField.currentText(),self.customerField.currentText(),self.termsField.currentText(),uniqueIDs]],columns=['Date', 'Invoice', 'Customer', 'Terms', 'UniqueIDs'])))
        
        ##Remove Coins from inventoryCoins Database
        inventoryCoins = pd.read_csv('Database\Data\inventoryCoins.csv')
        # Remove the rows with the indexes 1 and 2
        print('Removing coins from Coin Inventory...\n\n {}\n\nSuccesfully Pushed'.format(inventoryCoins[inventoryCoins['UniqueID'].isin(uniqueIDs)]))
        inventoryCoins = inventoryCoins[~inventoryCoins['UniqueID'].isin(uniqueIDs)]
        inventoryCoins.to_csv('Database\Data\inventoryCoins.csv', index=False)

        #Print Succesful Message
        self.savedToDBMessage = QMessageBox(self)
        self.savedToDBMessage.setWindowTitle('Invoice Creation Succesful.')
        self.savedToDBMessage.setText('The Invoice has been succesfully saved to the Database.')
        self.savedToDBMessage.setIcon(QMessageBox.Icon.Information)
        self.savedToDBMessage.exec()

        ## ADD OTHER GUI FUNCTIONAILITY
        self.saveInvoiceButton.setEnabled(False)
        self.saveInvoiceButton.setStyleSheet("background-color: gray;")
        #self.addressLabel = QPushButton('Print Labels')
        #self.verticalLabelLayout.addWidget(self.addressLabel)
        

class POApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Create New PO')
        self.setWindowIcon(QIcon('assets\coin.ico'))
        self.resize(self.screen().size().width(), self.screen().size().height()-80)

        # Create a QLabel widget for the background image
        background_label = QLabel(self)
        pixmap = QPixmap('assets/bridge_background.jpg')
        background_label.setPixmap(pixmap)
        background_label.setGeometry(0, 0, self.width(), self.height())

        """BEGIN WIDGITS"""
        #Back Button
        backButton = QPushButton(QIcon("assets\\backButton.ico"),"", self)
        backButton.setObjectName('backButton')
        backButton.setGeometry(0, 0, 75, 100)
        backButton.setIconSize(QSize(80,80))
        backButton.clicked.connect(self.returnHomeScreen)
        
        #Top Label
        self.topLabel = QLabel('Third Coast\nSupply Company LLC')
        self.topLabel.setFont(custom_font1)
        self.topLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.topLabel.setStyleSheet("""
        border: 2px solid rgb(189, 186, 186)
        """)

        self.editExistingPOButton = QPushButton('Edit Existing PO')
        self.editExistingPOButton.setFont(custom_font2)
        self.editExistingPOButton.clicked.connect(self.editExistingPO)

        #Selector Field
        selectorFieldLayout = QHBoxLayout()

        self.dateFieldLabel = QLabel('Date')
        self.dateFieldLabel.setFont(custom_font2)
        self.dateFieldLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.dateField = QtWidgets.QDateEdit(calendarPopup=True,date=date.today())

        self.poLabel = QLabel('PO')
        self.poLabel.setFont(custom_font2)
        self.poLabel.setAlignment(Qt.AlignmentFlag.AlignRight)        
        self.poField = QComboBox()
        listPOs = [x for x in pd.read_csv('Database\Data\purchaseOrders.csv')['PO'].values]
        listPOs = listPOs + [pd.read_csv('Database\Data\purchaseOrders.csv')['PO'].iloc[-1]+1]
        listPOs = sorted(listPOs, reverse=True)
        self.poField.addItems(list(map(str, listPOs)))

        self.customerLabel = QLabel('Customer')
        self.customerLabel.setFont(custom_font2)
        self.customerLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.customerField = QComboBox()
        self.customerField.addItems([str(x) for x in pd.read_csv('Database\Data\contacts.csv')['customer']])

        self.termsLabel = QLabel('Terms')
        self.termsLabel.setFont(custom_font2)
        self.termsLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.termsField = QComboBox()
        self.termsField.addItems(['Consignment','Sold','Split'])

        # Create a button to trigger the popup window

        self.saveCoinToDB = QPushButton('Add New Coin to DB')
        self.saveCoinToDB.setFont(custom_font2)
        self.saveCoinToDB.clicked.connect(self.addNewCoin)

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
        buttonLayout = QVBoxLayout()

        buttonLayout.addWidget(self.saveCoinToDB)
        buttonLayout.addWidget(self.editExistingPOButton)
        selectorFieldLayout.addLayout(buttonLayout)

        """ BARCODE SECTION """
        # Bar Code Input
        self.BarCodeLabel = QLabel('Scan Bar Code:')
        self.BarCodeLabel.setFont(custom_font2)
        self.BarCodeInput = QTextEdit()
        self.BarCodeInput.setMaximumSize(300,50)
        self.BarCodeInput.setPlaceholderText('Scan Here')
        self.BarCodeInput.installEventFilter(self)
        self.BarCodeButton = QPushButton('Run')
        self.BarCodeButton.setFont(custom_font2)
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
        self.table.setColumnWidth(1,300)
        self.table.setColumnWidth(4,30)
        self.table.setColumnWidth(7,200)
        self.table.setColumnWidth(8,200)

        #Vertical Buttons
        self.saveButton = QPushButton('Save')
        self.saveButton.setFont(custom_font2)
        self.saveButton.clicked.connect(self.savePO)

        self.newCoinButton = QPushButton('Add New Row')
        self.newCoinButton.setFont(custom_font2)
        self.newCoinButton.clicked.connect(self.AddNewRow)

        self.deleteRowButton = QPushButton('Delete Last Row')
        self.deleteRowButton.setFont(custom_font2)
        self.deleteRowButton.clicked.connect(self.deleteRow)

        self.verticalLabelLayout.addWidget(self.saveButton)
        self.verticalLabelLayout.addWidget(self.newCoinButton)
        self.verticalLabelLayout.addWidget(self.deleteRowButton)

        bigHorizontalLayout.addSpacing(20)
        bigHorizontalLayout.addWidget(self.table)
        bigHorizontalLayout.addSpacing(20)
        bigHorizontalLayout.addLayout(self.verticalLabelLayout)

        #Set window layout
        pageLayout = QVBoxLayout()
        topLayout = QHBoxLayout()

        topLayout.addWidget(backButton)
        topLayout.addStretch(4)
        topLayout.addWidget(self.topLabel)
        topLayout.addStretch(5)
        pageLayout.addLayout(topLayout)
        topLayout.addStretch(1)

        #Begin page layout

        pageLayout.addLayout(selectorFieldLayout)
        pageLayout.addLayout(barcodeLayout)
        pageLayout.addLayout(bigHorizontalLayout)
        pageLayout.addSpacing(60)
        self.setLayout(pageLayout)

    """BEGIN EVENT FILTER"""
    def eventFilter(self, source, event):
        if event.type() == QKeyEvent.Type.KeyRelease and event.key() == 16777220:  #If you click Enter
            try:
                tableEntry = self.BarCodeInput.toPlainText()
                newDF = updateTableSerial(pd.DataFrame(self.model._data),tableEntry)
                newDF = pd.concat([newDF, createNewPOfunc()])
                newIndex = ['{:03d}'.format(i) for i in range(1, len(newDF)+1)]
                newDF.index = newIndex
                self.model = PandasModel(newDF)
                self.table.setModel(self.model)
                self.table.setColumnWidth(1,300)
                self.table.setColumnWidth(4,30)
                self.table.setColumnWidth(7,190)
                self.table.setColumnWidth(8,190)
                delegate = NonEditableDelegate()
                #self.table.setItemDelegateForColumn(0, delegate)
                #self.table.setItemDelegateForColumn(1, delegate)
                #self.table.setItemDelegateForColumn(2, delegate)
                #self.table.setItemDelegateForColumn(3, delegate)
                #self.table.setItemDelegateForColumn(7, delegate)
                #self.table.setItemDelegateForColumn(8, delegate)
 
            except IndexError:
                print(IndexError)
            except ValueError:
                print(ValueError)

            self.BarCodeInput.clear()
            self.BarCodeInput.setFocus()
            self.BarCodeInput.setPlaceholderText('Scan Here')

        return super().eventFilter(source,event)

    """BEGIN FUNCTIONS"""
    def showLeavingPopup(self):
        self.savedContactMessage = QMessageBox(self)
        self.savedContactMessage.setWindowTitle('Leave without saving?')
        self.savedContactMessage.setText('The data inputted is not saved.\nAre you sure you want to leave?\n\nIf you are just printing labels\nfrom a previous PO, the data is already saved')
        self.savedContactMessage.setIcon(QMessageBox.Icon.Warning)
        self.savedContactMessage.setStandardButtons(QMessageBox.StandardButton.Retry|
                               QMessageBox.StandardButton.Ok|
                               QMessageBox.StandardButton.Cancel)
        self.savedContactMessage.exec()


    def returnHomeScreen(self):
        if self.saveButton.isEnabled() and self.model._data.iloc[0][0] != '':
            self.savedContactMessage = QMessageBox(self)
            self.savedContactMessage.setWindowTitle('Leave without saving?')
            self.savedContactMessage.setText('The data inputted is not saved.\nAre you sure you want to leave?\n\nIf you are just printing labels\nfrom a previous PO, the data is already saved')
            self.savedContactMessage.setIcon(QMessageBox.Icon.Warning)
            self.savedContactMessage.setStandardButtons(QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No)
            result = self.savedContactMessage.exec()
            #if result == QMessageBox.StandardButton.Save:
            #    self.savedContactMessage.close()
            #    self.savePO()
            #    return
            if result == QMessageBox.StandardButton.Yes:
                #Close Window
                print('closing')
                with open("stylesheets/homeStyles.css","r") as file:
                    app.setStyleSheet(file.read())
                homeAppWindow.show()
            elif result == QMessageBox.StandardButton.No:
                self.savedContactMessage.close()
                return

        #Clear Data
        try:
            if not self.printLabelsLabel.isHidden():
                self.printLabelsLabel.setHidden(not self.printLabelsLabel.isHidden())
            if not self.printOneLabelButton.isHidden():
                print('is hidden')
                self.printOneLabelButton.setHidden(not self.printOneLabelButton.isHidden())
            #if not self.printPOLabel.isHidden():
            #    self.printPOLabel.setHidden(not self.saveButton.isHidden())
        except AttributeError as ae:
            #print('HANDLED: {}'.format(ae))
            print('')
        self.model = PandasModel(createNewPOfunc())
        self.table.setModel(self.model)
        self.saveButton.setText('Save PO')
        listPOs = [x for x in pd.read_csv('Database\Data\purchaseOrders.csv')['PO'].values]
        listPOs = listPOs + [pd.read_csv('Database\Data\purchaseOrders.csv')['PO'].iloc[-1]+1]
        listPOs = sorted(listPOs, reverse=True)
        self.BarCodeInput.clear()
        self.poField.clear()
        self.poField.addItems(list(map(str, listPOs)))
        self.saveButton.setEnabled(True)
        self.saveButton.setStyleSheet("stylesheets\poStyles.css")
        self.newCoinButton.setEnabled(True)
        self.deleteRowButton.setEnabled(True)
        self.newCoinButton.setStyleSheet("stylesheets\poStyles.css")
        self.deleteRowButton.setStyleSheet("stylesheets\poStyles.css")
        
        #Close Window
        POAppWindow.close()
        with open("stylesheets/homeStyles.css","r") as file:
            app.setStyleSheet(file.read())
        homeAppWindow.show()

    def addNewCoin(self):
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
    
    def savePO(self):
        if len(self.model._data['PCGS #']) == 1 and (self.model._data['PCGS #'].iloc[0] == ''):
            self.savedToDBMessage = QMessageBox(self)
            self.savedToDBMessage.setWindowTitle('Save Unsuccesful')
            self.savedToDBMessage.setText('Save unsuccesful as the dataframe is empty.\nPlease scan a barcode & click "enter".')
            self.savedToDBMessage.setIcon(QMessageBox.Icon.Warning)
            self.savedToDBMessage.setStandardButtons(QMessageBox.StandardButton.Close)
            self.savedToDBMessage.setStyleSheet("QMessageBox { min-width:500px }")
            self.savedToDBMessage.exec()
            return
        ##Cleanup data for DB
        dataToPush = self.model._data[:-1]
        uniqueIDs = ['{}-{}'.format(self.poField.currentText(),x) for x in dataToPush.index]
        print('NON CRITICAL ERROR HERE')
        dataToPush['Unique ID'] = uniqueIDs
        print('\nPushing data to Coin Database...\n\n{}'.format(dataToPush))

        #See if PO is being Edited or is new
        POCoinsDB = pd.read_csv('Database\Data\purchaseOrderCoins.csv')
        if not POCoinsDB[POCoinsDB['UniqueID'].str.split('-').str[0] == self.poField.currentText()].empty: #If the PO # is already in the Database (being edited)
            print('NOT AVAILABLE YET')

            # Print NOT WORKING MESSAGE
            self.savedToDBMessage = QMessageBox(self)
            self.savedToDBMessage.setWindowTitle('PO Edit Unsuccesful.')
            self.savedToDBMessage.setText('Unfortunately the PO Editing is a hard ass problem\n\nshit azz developer is working on it\nIn the meantime, you can use this to print old labels')
            self.savedToDBMessage.setIcon(QMessageBox.Icon.Warning)
            self.savedToDBMessage.setStandardButtons(QMessageBox.StandardButton.Close)
            self.savedToDBMessage.setStyleSheet("QMessageBox { min-width:500px }")
            self.savedToDBMessage.exec()

            return
        
        ##Save Coin Metadata to inventoryCoins Database
        dataToPush.to_csv('Database\Data\inventoryCoins.csv', index=False, header=not os.path.exists('Database\Data\inventoryCoins.csv'), mode='a')

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
        self.savedToDBMessage.setStyleSheet("QMessageBox { min-width:500px }")
        self.savedToDBMessage.exec()

        ## ADD OTHER GUI FUNCTIONAILITY
        self.saveButton.setEnabled(False)
        self.saveButton.setStyleSheet("background-color: gray;")
        self.newCoinButton.setEnabled(False)
        self.newCoinButton.setStyleSheet("background-color: gray;")
        self.deleteRowButton.setEnabled(False)
        self.deleteRowButton.setStyleSheet("background-color: gray;")
        #self.printPOLabel = QPushButton('Print PO')
        button = self.findChild(QPushButton, "printOneLabelButton")
        if button is not None:
            print('Already Exists')
        else:
            self.printLabelsLabel = QPushButton('Print Labels')
            self.printLabelsLabel.clicked.connect(self.PrintAllCoins)
            self.printOneLabelButton = QPushButton('Print One Label')
            self.printOneLabelButton.clicked.connect(self.PrintOneCoin)


        #self.verticalLabelLayout.addWidget(self.printPOLabel)
        self.verticalLabelLayout.addWidget(self.printLabelsLabel)
        self.verticalLabelLayout.addWidget(self.printOneLabelButton)
        
    def BarCodeRun(self):
        try:
            tableEntry = self.BarCodeInput.toPlainText()
            newDF = updateTableSerial(pd.DataFrame(self.model._data),tableEntry)
            newDF = pd.concat([newDF, createNewPOfunc()])
            newIndex = ['{:03d}'.format(i) for i in range(1, len(newDF)+1)]
            newDF.index = newIndex
            self.model = PandasModel(newDF)
            self.table.setModel(self.model)
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

    def PrintAllCoins(self):
        try:
            dataToPrint = self.model._data
            dataToPrint = dataToPrint[dataToPrint['PCGS #'] != '']
            for index,row in dataToPrint.iterrows():
                print('Printing Labels for: {}'.format(self.poField.currentText()))
                date = row[1].split('-')[0] if len(row[1].split('-')) == 3 else "-".join([str(item) for item in row[1].split('-')[0:2]])

                print('Date: ', date)
                print('Denom: ', row[1].split('-')[-2])
                print('Service: ', row[3])
                print('CAC: ', row[4])
                print('Cost: ', row[5])
                print('Price: ', row[6])
                print('PCGS#: ', row[0])
                print('PO Index: ',index)


                printCoinLabel(date, row[1].split('-')[-2], row[3], row[2], row[6],self.poField.currentText(),index, row[0], row[4])

            self.savedToDBMessage = QMessageBox(self)
            self.savedToDBMessage.setWindowTitle('Labels printing!')
            self.savedToDBMessage.setText('The labels are printing!\n\nYou can now find these\ncoins in an invoice.')
            self.savedToDBMessage.setIcon(QMessageBox.Icon.Information)
            self.savedToDBMessage.setStandardButtons(QMessageBox.StandardButton.Close)
            self.savedToDBMessage.exec()
            
        except IndexError as IE:
            print(IE)

    def PrintOneCoin(self):
        text, ok = QInputDialog.getMultiLineText(self, 'Enter Coin Information', 'Please Enter the Coin Index\nLeftmost Number on Table')
        if ok:
            parseText = text
            try:
                dataToPrint = self.model._data                 
                dataToPrint = dataToPrint[dataToPrint.index == text]
                for index,row in dataToPrint.iterrows():
                    if index == parseText:
                        print('Printing Labels for:')
                        print(row[1].split('-')[0], row[1].split('-')[-2], row[3], row[2], row[6], self.poField.currentText(),'-',index, row[0], row[4])
                        printCoinLabel(row[1].split('-')[0], row[1].split('-')[-2], row[3], row[2], row[6], self.poField.currentText(),index, row[0], row[4])
                    else:
                        self.savedToDBMessage = QMessageBox(self)
                        self.savedToDBMessage.setWindowTitle('Error with index {}'.format(index))
                        self.savedToDBMessage.setText('That index {} is not saved. Please ensure you are entering the leftmost number.'.format(index))
                        self.savedToDBMessage.setIcon(QMessageBox.Icon.Information)
                        self.savedToDBMessage.setStandardButtons(QMessageBox.StandardButton.Close)
                        self.savedToDBMessage.exec()
                        return

                self.savedToDBMessage = QMessageBox(self)
                self.savedToDBMessage.setWindowTitle('Labels printing!')
                self.savedToDBMessage.setText('The label is printing!\n\nYou can now find these\ncoins in an invoice.')
                self.savedToDBMessage.setIcon(QMessageBox.Icon.Information)
                self.savedToDBMessage.setStandardButtons(QMessageBox.StandardButton.Close)
                self.savedToDBMessage.exec()
                
            except IndexError as IE:
                print(IE)

    def AddNewRow(self):
            newDF = pd.concat([self.model._data, createNewPOfunc()])
            newIndex = ['{:03d}'.format(i) for i in range(1, len(newDF)+1)]
            newDF.index = newIndex
            self.model = PandasModel(newDF)
            self.table.setModel(self.model)
            self.table.setColumnWidth(1,300)
            self.table.setColumnWidth(4,30)
            self.table.setColumnWidth(7,200)
            self.table.setColumnWidth(8,200)
            #delegate = QtWidgets.QItemDelegate()
            #self.table.setItemDelegateForColumn(0, delegate)
            #self.table.setItemDelegateForColumn(1, None)
            #self.table.setItemDelegateForColumn(2, None)
            #self.table.setItemDelegateForColumn(3, None)
            #self.table.setItemDelegateForColumn(7, None)
            #self.table.setItemDelegateForColumn(8, None)
    
    def deleteRow(self):
        newDF = self.model._data[:-1]
        newIndex = ['{:03d}'.format(i) for i in range(1, len(newDF)+1)]
        newDF.index = newIndex
        self.model = PandasModel(newDF)
        self.table.setModel(self.model)
        self.table.setColumnWidth(1,300)
        self.table.setColumnWidth(4,30)
        self.table.setColumnWidth(7,200)
        self.table.setColumnWidth(8,200)

    def editExistingPO(self):
        #Show popup
        coin_info, ok_pressed = QInputDialog.getText(self, 'Enter Coin Information', 'Please Enter the PO# or scan a coin Inventory Barcode from the PO:')
       # Check if the user clicked 'OK' and retrieve the entered text
        if ok_pressed:
            try:
                extractValuesDF = getPOInfoFromBarcode(coin_info)
                PO = extractValuesDF['PO'].iloc[0]
                customer = extractValuesDF['Customer'].iloc[0]
                terms = extractValuesDF['Terms'].iloc[0]
                uniqueIDs = extractValuesDF['UniqueIDs'].iloc[0]
                coinDB = getCoinFromTCSLabel(str(PO))
                #coinDB['CAC'] = ''
                newDF = coinDB
                newIndex = ['{:03d}'.format(i) for i in range(1, len(newDF)+1)]
                newDF.index = newIndex
                self.model = PandasModel(newDF)
                self.table.setModel(self.model)
                self.table.setColumnWidth(1,300)
                self.table.setColumnWidth(4,30)
                self.table.setColumnWidth(7,190)
                self.table.setColumnWidth(8,190)
                delegate = NonEditableDelegate()
                
                #Change selector dropdown fields
                self.customerField.setCurrentText(customer)
                self.poField.setCurrentText(str(PO))
                self.termsField.setCurrentText(terms)

                #Adjust UI
                button = self.findChild(QPushButton, "printOneLabelButton")
                if button is not None:
                    print('Already Exists')
                else:
                    self.saveButton.setText('Save Updated PO')
                    self.printLabelsLabel = QPushButton('Print Labels')
                    self.printLabelsLabel.setObjectName("printLabelsButton")
                    self.printLabelsLabel.clicked.connect(self.PrintAllCoins)

                    self.printOneLabelButton = QPushButton('Print One Label')
                    self.printLabelsLabel.setObjectName("printOneLabelButton")
                    self.printOneLabelButton.clicked.connect(self.PrintOneCoin)
                    #self.verticalLabelLayout.addWidget(self.printPOLabel)
                    self.verticalLabelLayout.addWidget(self.printLabelsLabel)
                    self.verticalLabelLayout.addWidget(self.printOneLabelButton)


                self.AddNewRow()
                #Remove Data from Database


                #Resave PO data to Database


            except IndexError as IE:
                self.savedContactMessage = QMessageBox(self)
                self.savedContactMessage.setWindowTitle('PO Not Found')
                self.savedContactMessage.setText('The PO of {} is not found in the Database'.format(coin_info))
                self.savedContactMessage.setIcon(QMessageBox.Icon.Warning)
                self.savedContactMessage.exec()

        return


class newContactApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Create New Contact')
        self.setWindowIcon(QIcon('assets\coin.ico'))
        self.resize(self.screen().size().width(), self.screen().size().height()-80)

        # Create a QLabel widget for the background image
        background_label = QLabel(self)
        pixmap = QPixmap('assets/bridge_background.jpg')
        background_label.setPixmap(pixmap)
        background_label.setGeometry(0, 0, self.width(), self.height())
        
        """BEGIN WIDGITS"""
        #Back Button
        backButton = QPushButton(QIcon("assets\\backButton.ico"),"", self)
        backButton.setObjectName('backButton')
        backButton.setGeometry(0, 0, 75, 100)
        backButton.setIconSize(QSize(80,80))
        backButton.clicked.connect(self.returnHomeScreen)
        
        #Top Label
        self.topLabel = QLabel('Third Coast \nSupply Company LLC')
        self.topLabel.setFont(custom_font1)
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
        self.customerLabel.setFont(custom_font2)
        self.customerLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.customerEntry = QLineEdit()
        customerBoxLayout.addStretch(1)
        customerBoxLayout.addWidget(self.customerLabel)
        customerBoxLayout.addWidget(self.customerEntry)
        customerBoxLayout.addStretch(1)

        #Email
        self.emailLabel = QLabel('Email:')
        self.emailLabel.setFont(custom_font2)
        self.emailLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.emailEntry = QLineEdit()
        emailBoxLayout.addStretch(1)
        emailBoxLayout.addWidget(self.emailLabel)
        emailBoxLayout.addWidget(self.emailEntry)
        emailBoxLayout.addStretch(1)

        #Phone
        self.phoneLabel = QLabel('Phone:')
        self.phoneLabel.setFont(custom_font2)
        self.phoneLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.phoneEntry = QLineEdit()
        phoneBoxLayout.addStretch(1)
        phoneBoxLayout.addWidget(self.phoneLabel)
        phoneBoxLayout.addWidget(self.phoneEntry)
        phoneBoxLayout.addStretch(1)

        #Address
        self.addressLabel = QLabel('Address:')
        self.addressLabel.setFont(custom_font2)
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
        self.saveNewContactButton.setFont(custom_font2)
        self.saveNewContactButton.clicked.connect(self.saveNewContact)

        newContactButtonsLayout.addStretch(1)
        newContactButtonsLayout.addWidget(self.saveNewContactButton)
        newContactButtonsLayout.addStretch(1)

        #Set top layout
        topLayout = QHBoxLayout()
        topLayout.addWidget(backButton)
        topLayout.addStretch(4)
        topLayout.addWidget(self.topLabel)
        topLayout.addStretch(5)

        #Begin page layout
        pageLayout = QVBoxLayout()
        pageLayout.addLayout(topLayout)
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


class inventoryReportApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PCGS Coin Inventory Tracker')
        self.setWindowIcon(QIcon('assets\coin.ico'))
        self.resize(self.screen().size().width(), self.screen().size().height()-80)

        # Create a QLabel widget for the background image
        background_label = QLabel(self)
        pixmap = QPixmap('assets/bridge_background.jpg')
        background_label.setPixmap(pixmap)
        background_label.setGeometry(0, 0, self.width(), self.height())
        
        """BEGIN WIDGITS"""
        #Back Button
        backButton = QPushButton(QIcon("assets\\backButton.ico"),"", self)
        backButton.setObjectName('backButton')
        backButton.setGeometry(0, 0, 75, 100)
        backButton.setIconSize(QSize(80,80))
        backButton.clicked.connect(self.returnHomeScreen)

        #Refresh Button
        refreshButton = QPushButton(QIcon("assets\\refresh.ico"),"", self)
        refreshButton.setObjectName('refreshButton')
        refreshButton.setGeometry(0, 0, 75, 100)
        refreshButton.setIconSize(QSize(80,80))
        refreshButton.clicked.connect(self.refresh)

        #Top Label
        self.topLabel = QLabel('Third Coast \nSupply Company LLC')
        self.topLabel.setFont(custom_font1)
        self.topLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.topLabel.setStyleSheet("""
        border: 2px solid rgb(189, 186, 186)
        """)
        
        #Set top layout
        topLayout = QHBoxLayout()
        topLayout.addWidget(backButton)
        topLayout.addStretch(1)
        topLayout.addWidget(self.topLabel)
        topLayout.addStretch(1)
        topLayout.addWidget(refreshButton)
        self.dataDisplaylayout = QHBoxLayout()

        reportData = getReportData()
        # Create and add labels and fields to the layout
        data = {
            "Count of PO's": str(reportData[0]),
            "Count of Invoices": str(reportData[1]),
            "Total Coins in Inventory": str(reportData[2]),
            "Total Price Paid": str(reportData[3]),
            "Total Price Sold": str(reportData[4])
        }
        for label_text, value_text in data.items():
            frame = QFrame(self)
            frame.setFrameShape(QFrame.Shape.Box)
            frame.setLineWidth(1)

            label = QLabel(label_text, frame)
            label.setFont(custom_font2)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            value = QLineEdit(value_text, frame)
            value.setReadOnly(True)
            value.setAlignment(Qt.AlignmentFlag.AlignCenter)

            frameLayout = QVBoxLayout(frame)
            frameLayout.addWidget(label)
            frameLayout.addWidget(value)

            self.dataDisplaylayout.addWidget(frame)
        

        #Add layout to space data Display to left hand side
        self.mainDataLayout = QHBoxLayout()
        self.mainDataLayout.addLayout(self.dataDisplaylayout)


        #Begin page layout
        self.pageLayout = QVBoxLayout()
        self.pageLayout.addLayout(topLayout)
        self.pageLayout.addStretch(1)
        self.pageLayout.addLayout(self.mainDataLayout)


        self.pageLayout.addStretch(5)
        self.setLayout(self.pageLayout)


    """BEGIN FUNCTIONS"""
    def returnHomeScreen(self):
        inventoryReportWindow.close()
        with open("stylesheets/homeStyles.css","r") as file:
            app.setStyleSheet(file.read())
        homeAppWindow.show()

    def refresh(self):
        #self.dataDisplaylayout = QHBoxLayout()
        reportData = getReportData()
        # Create and add labels and fields to the layout
        dataNew = {
            "Count of PO's": str(reportData[0]),
            "Count of Invoices": str(reportData[1]),
            "Total Coins in Inventory": str(reportData[2]),
            "Total Price Paid": str(reportData[3]),
            "Total Price Sold": str(reportData[4])
        }

        for i in reversed(range(self.dataDisplaylayout.count())): 
            self.dataDisplaylayout.itemAt(i).widget().setParent(None)

        import time

        print("Before pause")
        time.sleep(1)  # Pause the script for 1 second
        print("After pause")

        for label_text, value_text in dataNew.items():
            frame = QFrame(self)
            frame.setFrameShape(QFrame.Shape.Box)
            frame.setLineWidth(1)

            label = QLabel(label_text, frame)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            value = QLineEdit(value_text, frame)
            value.setReadOnly(True)
            value.setAlignment(Qt.AlignmentFlag.AlignCenter)

            frameLayout = QVBoxLayout(frame)
            frameLayout.addWidget(label)
            frameLayout.addWidget(value)

            self.dataDisplaylayout.addWidget(frame)
        #Add layout to space data Display to left hand side
        self.mainDataLayout = QHBoxLayout()
        self.mainDataLayout.addLayout(self.dataDisplaylayout)
        self.pageLayout.addLayout(self.mainDataLayout)

        print('Attempted to update')

        return


class ScannerTesterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Scanner Test')
        self.resize(self.screen().size().width(), self.screen().size().height()-80)

        # Create a QLabel widget for the background image
        background_label = QLabel(self)
        pixmap = QPixmap('assets/bridge_background.jpg')
        background_label.setPixmap(pixmap)
        background_label.setGeometry(0, 0, self.width(), self.height())

        """BEGIN WIDGITS"""
        #Back Button
        hbox = QHBoxLayout()
        backButton = QPushButton(QIcon("assets\\backButton.ico"),"", self)
        backButton.setObjectName('backButton')
        backButton.setGeometry(0, 0, 75, 100)
        backButton.setIconSize(QSize(80,80))
        backButton.clicked.connect(self.returnHomeScreen)

        vbox = QVBoxLayout()
        # create a label in the center
    
        self.scanBoxLabel = QLabel('Try Scanning Below')
        self.scanBoxLabel.setFont(custom_font2)
        self.scanBoxLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # create a QTextEdit widget to display the barcode data
        self.text_edit = QTextEdit()
        self.text_edit.setGeometry(0,0,100,100)
        self.text_edit.setStyleSheet('background-color: #f0f0f0;')

        # create a button to clear the entry form
        self.labelPrint = QPushButton('Clear Entry Form')
        self.labelPrint.setFont(custom_font2)
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
        self.setWindowTitle('Printer Test')
        self.resize(self.screen().size().width(), self.screen().size().height()-80)

        # Create a QLabel widget for the background image
        background_label = QLabel(self)
        pixmap = QPixmap('assets/bridge_background.jpg')
        background_label.setPixmap(pixmap)
        background_label.setGeometry(0, 0, self.width(), self.height())

        """BEGIN WIDGITS"""
        #Back Button
        hbox = QHBoxLayout()
        backButton = QPushButton(QIcon("assets\\backButton.ico"),"", self)
        backButton.setObjectName('backButton')
        backButton.setGeometry(0, 0, 75, 100)
        backButton.setIconSize(QSize(80,80))
        backButton.clicked.connect(self.returnHomeScreen)

        vbox = QVBoxLayout()
        #Top Label
        self.topLabel = QLabel('Scan a Manufacturers Barcode & Click Run')
        self.topLabel.setFont(custom_font2)
        self.topLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.topLabel.setStyleSheet("""
        border: 2px solid rgb(189, 186, 186)
        """)

        hbox2 = QHBoxLayout()

        self.InvoiceBarCodeLabel2 = QLabel('Bar Code:')
        self.InvoiceBarCodeLabel2.setFont(custom_font2)
        self.InvoiceBarCodeInput2 = QTextEdit()
        self.InvoiceBarCodeInput2.setMaximumSize(300,50)
        #self.InvoiceBarCodeInput2.setPlaceholderText('(XXX-XXX)')
        self.InvoiceBarCodeRunButton2 = QPushButton('Run')
        self.InvoiceBarCodeRunButton2.setFont(custom_font2)
        self.InvoiceBarCodeRunButton2.clicked.connect(self.runPrintTest)

        hbox2.addStretch(5)
        hbox2.addWidget(self.InvoiceBarCodeLabel2)
        hbox2.addWidget(self.InvoiceBarCodeInput2)
        hbox2.addWidget(self.InvoiceBarCodeRunButton2)
        hbox2.addStretch(5)

        #Place Widgets
        hbox.addWidget(backButton)
        hbox.addStretch(7)
        vbox.addLayout(hbox)

        vbox.addWidget(self.topLabel)
        vbox.addStretch(1)
        vbox.addLayout(hbox2)

        vbox.addStretch(10)
        self.setLayout(vbox)


    def returnHomeScreen(self):
        PrinterTesterWindow.close()
        with open("stylesheets/homeStyles.css","r") as file:
            app.setStyleSheet(file.read())
        homeAppWindow.show()

    def runPrintTest(self):
        tableEntry = self.InvoiceBarCodeInput2.toPlainText()
        tableEntry = tableEntry.replace(' ','')

        if tableEntry.__contains__('\n'):
            tableEntry = tableEntry.replace('\n','')
            
        if len(self.InvoiceBarCodeInput2.toPlainText()) == 1:
            self.InvoiceBarCodeInput2.clear()
            self.InvoiceBarCodeInput2.setFocus()
            #self.InvoiceBarCodeInput2.setPlaceholderText('(XXX-XXX)')
            return 

        
        #invoiceCoins = pd.read_csv('Database\Data\purchaseOrderCoins.csv')
        try:
            row = getCoinDataSerial(tableEntry)
            print('Printing single Label for:\n')
            print(row['Description'].iloc[0].split('-')[0], row['Description'].iloc[0].split('-')[-2], row['Service'].iloc[0], row['Grade'].iloc[0], str('100'), str('XXX'), str('XXX'), row['PCGS #'].iloc[0])
            printCoinLabel(row['Description'].iloc[0].split('-')[0], row['Description'].iloc[0].split('-')[-2], row['Service'].iloc[0], row['Grade'].iloc[0], str('100'), str('XXX'), str('XXX'), row['PCGS #'].iloc[0])
  
        except IndexError as IE:
            print('not available')
        
        self.InvoiceBarCodeInput2.clear()
        self.InvoiceBarCodeInput2.setFocus()

        return



"""CALL APPLICATION"""

app = QApplication([])
with open("stylesheets/loginStyles.css","r") as file:
    app.setStyleSheet(file.read())

loginWindow = loginScreen()
homeAppWindow = homeApp()
newInvoiceWindow = newInvoiceApp()
POAppWindow = POApp()
newContactWindow = newContactApp()
inventoryReportWindow = inventoryReportApp()
scannerTesterWindow = ScannerTesterApp()
PrinterTesterWindow = PrinterTesterApp()

loginWindow.show()
#homeAppWindow.show()
#POAppWindow.show()
#newContactWindow.show()
#newInvoiceWindow.show()
#inventoryReportWindow.show()
#PrinterTesterWindow.show()

app.exec()



"""
HELPFUL LINKS:

For Structure: https://www.pythonguis.com/tutorials/pyqt6-layouts/

For CSS Styling with PyQt6: https://doc.qt.io/qtforpython/overviews/stylesheet-examples.html#style-sheet-usage

All Qt Modules: https://doc.qt.io/qtforpython/modules.html

"""
######################
"""
--- HEAVY HITTERS

"""

"""
FROM LURCH TO WORK ON

--- Invoice print Piece of Paper

GOAL IS 22nd (26th hard cutoff)

"""


"""
- TO DO
--- Remove Print Labels on Invoice Window
--- Add New Coin takes in BarCode Scanner

"""

### HOW TO EXPORT THE APPLICATION
"""
python -m PyInstaller --onefile --windowed mainApp.py

worth a try:

python -m PyInstaller --onefile --windowed --icon=assets\coin.ico mainApp.py

move folders: dist & build
move file: mainApp.spec
populate dist folder w/: assets, Database, stylesheets, and .env
"""