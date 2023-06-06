import requests
from win32com.client import Dispatch
import pathlib

my_printer = 'DYMO LabelWriter 450 Turbo'
printer_com = Dispatch('Dymo.DymoAddIn')
printer_com.SelectPrinter(my_printer)
label_path = 'assets\label_final.label'
printer_com.Open2(label_path)


# LABEL OPTIONS
"""
- TITLE
- PHONE
- PCGS
- DENOM
- SERVICE
- GRADE
- PRICE
"""

barCode_value = '101-002'
PCGS_value = '8734'


printer_label = Dispatch('Dymo.DymoLabels')
print(printer_label.getObjectNames(True))
print(printer_label.getText('PCGS'))

#print(printer_label.AddressFieldCount)

printer_label.setField('BARCODE',barCode_value)
printer_label.setField('PCGS',PCGS_value)
printer_label.setField('DENOM', )


""" START PRINT """
#printer_com.StartPrintJob()
#printer_com.Print(1,False)
#printer_com.EndPrintJob()