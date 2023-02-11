import sys
from PyQt6.QtWidgets import (
    QWidget, QApplication, QVBoxLayout, QPushButton, QHBoxLayout,
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
        layout = QVBoxLayout()
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

        """PCGS Data Field"""
        #Start 1st Label Row
        pcgsDataLabelLayout = QHBoxLayout()

        self.inventoryNumLabel = QLabel('Inventory #')
        self.inventoryNumLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.PCGSLabel = QLabel('PCGS')
        self.PCGSLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
        self.coinLabel = QLabel('Coin')
        self.coinLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        pcgsDataLabelLayout.addWidget(self.inventoryNumLabel)
        pcgsDataLabelLayout.addWidget(self.PCGSLabel)
        pcgsDataLabelLayout.addWidget(self.coinLabel)      

        #Start 1st Data Row
        pcgsDataLayout = QHBoxLayout()

        self.inventoryNum = QLabel('--')
        self.inventoryNum.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.PCGSNum = QLabel('--')
        self.PCGSNum.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
        self.coin = QLabel('--')
        self.coin.setAlignment(Qt.AlignmentFlag.AlignCenter)

        pcgsDataLayout.addWidget(self.inventoryNum)
        pcgsDataLayout.addWidget(self.PCGSNum)
        pcgsDataLayout.addWidget(self.coin)  

        
        #Start 2nd Label Row
        pcgsDataLabelLayout2 = QHBoxLayout()
        
        self.serviceLabel = QLabel('Service')
        self.serviceLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gradeLabel = QLabel('Grade')
        self.gradeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
        self.certNumLabel = QLabel('Cert #')
        self.certNumLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        pcgsDataLabelLayout2.addWidget(self.serviceLabel)
        pcgsDataLabelLayout2.addWidget(self.gradeLabel)
        pcgsDataLabelLayout2.addWidget(self.certNumLabel)      

        #Start 2nd Data Row
        pcgsDataLayout2 = QHBoxLayout()
        
        self.service = QLabel('--')
        self.service.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.grade = QLabel('--')
        self.grade.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
        self.certNum = QLabel('--')
        self.certNum.setAlignment(Qt.AlignmentFlag.AlignCenter)

        pcgsDataLayout2.addWidget(self.service)
        pcgsDataLayout2.addWidget(self.grade)
        pcgsDataLayout2.addWidget(self.certNum) 

        #Start INPUT LABEL Row 
        pcgsDataInputLabelLayout = QHBoxLayout()
        
        self.CACLabel = QLabel('CAC')
        self.CACLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.costLabel = QLabel('Cost')
        self.costLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
        self.priceLabel = QLabel('Price')
        self.priceLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        pcgsDataInputLabelLayout.addWidget(self.CACLabel)
        pcgsDataInputLabelLayout.addWidget(self.costLabel)
        pcgsDataInputLabelLayout.addWidget(self.priceLabel) 

        #Start INPUT Row
        pcgsDataInputLayout = QHBoxLayout()
        
        self.CACInput = QLineEdit()
        self.CACInput.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.costInput = QLineEdit()
        self.costInput.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
        self.priceInput = QLineEdit()
        self.priceInput.setAlignment(Qt.AlignmentFlag.AlignCenter)

        pcgsDataInputLayout.addWidget(self.CACInput)
        pcgsDataInputLayout.addWidget(self.costInput)
        pcgsDataInputLayout.addWidget(self.priceInput) 


        #Buttons
        poOrInvoiceLayout = QHBoxLayout()
        poButton = QPushButton('Create PO')
        invoiceButton = QPushButton('Create Invoice')

        poOrInvoiceLayout.addWidget(poButton)
        poOrInvoiceLayout.addWidget(invoiceButton)
        


        """BEGIN PAGE LAYOUT"""
        #layout
        layout.addWidget(self.topLabel)
        layout.addWidget(self.BarCodeInput)
        layout.addWidget(runButton)
        layout.addLayout(pcgsDataLabelLayout)
        layout.addLayout(pcgsDataLayout)
        layout.addLayout(pcgsDataLabelLayout2)
        layout.addLayout(pcgsDataLayout2)
        layout.addLayout(pcgsDataInputLabelLayout)
        layout.addLayout(pcgsDataInputLayout)
        layout.addLayout(pcgsDataInputLabelLayout)
        layout.addLayout(poOrInvoiceLayout)


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

For CSS Styling with PyQt6: https://doc.qt.io/qtforpython/overviews/stylesheet-examples.html#style-sheet-usage

"""