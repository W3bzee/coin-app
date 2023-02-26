import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt

from PyQt6.QtCore import QSize




class MyWindow(QWidget):
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
        window.close()
        import createPO.purchaseOrderApp
            #with open("homeScreen\messageBoxStyles.css","r") as file:
            #    app.setStyleSheet(file.read())


"""CALL APPLICATION"""
window = MyWindow()
window.show()
