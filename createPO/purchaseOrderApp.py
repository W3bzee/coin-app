import sys
from PyQt6.QtWidgets import (
    QWidget, QApplication, QVBoxLayout, QPushButton, QHBoxLayout,
    QTextEdit, QGridLayout, QStackedLayout, QFrame,
    QLabel, QCheckBox, QComboBox, QListWidget, QLineEdit,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider
)
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt


from createPO.findPCGS import pcgsCoinLookup



class MyApp(QWidget):
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
        self.backButton = QPushButton('&Back', clicked=self.returnHome)
    

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

        self.coinNumLabel = QLabel('Coin #')
        self.coinNumLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.coinDateLabel = QLabel('Coin Date')
        self.coinDateLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
        self.denominationLabel = QLabel('Denomination')
        self.denominationLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        pcgsDataLabelLayout.addWidget(self.coinNumLabel)
        pcgsDataLabelLayout.addWidget(self.coinDateLabel)
        pcgsDataLabelLayout.addWidget(self.denominationLabel)      

        #Start 1st Data Row
        pcgsDataLayout = QHBoxLayout()

        self.coinNum = QLabel('--')
        self.coinNum.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.coinDate = QLabel('--')
        self.coinDate.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
        self.denomination = QLabel('--')
        self.denomination.setAlignment(Qt.AlignmentFlag.AlignCenter)

        pcgsDataLayout.addWidget(self.coinNum)
        pcgsDataLayout.addWidget(self.coinDate)
        pcgsDataLayout.addWidget(self.denomination)  

        
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
        
        #Unique Inventory ID (If exists)
        uniqueIdLayout = QHBoxLayout()

        self.uniqueIdLabel = QLabel('Unique Inventory ID')
        self.uniqueIdLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.uniqueId = QLabel('--')
        self.uniqueId.setAlignment(Qt.AlignmentFlag.AlignCenter)

        uniqueIdLayout.addWidget(self.uniqueIdLabel)
        uniqueIdLayout.addWidget(self.uniqueId)


        """BEGIN PAGE LAYOUT"""
        #layout
        layout.addWidget(self.backButton)
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
        layout.addLayout(uniqueIdLayout)


        layout.addWidget(self.outputField)

    """DEFINE FUNCTIONS"""
    def returnHome(self):
        window.close()
        print('IM RUNNING')
        

    def run(self):
        barCode = self.BarCodeInput.text()
        coinNumber = barCode.split('-')[0].split('.')[0]
        grade = barCode.split('-')[0].split('.')[1]

        #Call Database
        dfResults = pcgsCoinLookup(coinNum=coinNumber)        
        print(dfResults)

        date = dfResults['DATE'].values
        denomination = dfResults['DENOM.   VARIETY'].values
        gradeName = dfResults['DESIGN'].values

        #Set labels with data
        self.outputField.setText('{0}'.format(coinNumber))
        self.coinNum.setText('{0}'.format(coinNumber))
        self.coinDate.setText('{0}'.format(date))
        self.denomination.setText('{0}'.format(denomination))
        self.service.setText('PCGS')
        self.grade.setText('{0}'.format(gradeName+grade))




"""CALL APPLICATION"""
window = MyApp()
window.show()




"""
HELPFUL LINKS:

For Structure: https://www.pythonguis.com/tutorials/pyqt6-layouts/

For CSS Styling with PyQt6: https://doc.qt.io/qtforpython/overviews/stylesheet-examples.html#style-sheet-usage

"""