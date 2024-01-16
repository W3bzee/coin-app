import requests
from win32com.client import Dispatch
import pathlib

my_printer = 'DYMO LabelWriter 450 Turbo'
printer_com = Dispatch('Dymo.DymoAddIn')
printer_com.SelectPrinter(my_printer)
label_path = 'assets\label_final_011524.label'
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
- pcgs_actual
"""
def printCoinLabel(pcgs, denom, service, grade, price, po, uniqueID, pcgs_actual, CAC):
    printer_label = Dispatch('Dymo.DymoLabels')
    CAC = 'CAC' if CAC == '1' else ''
    combination = '{} {} {} {} {}'.format(str(pcgs), str(denom), str(service), str(grade), str(CAC))
    printer_label.setField('COMBO',combination)

    printer_label.setField('PRICE', '$'+str(price))
    printer_label.setField('ID',str(po)+'-'+str(uniqueID))
    printer_label.setField('BARCODE', str(po)+'-'+str(uniqueID))
    printer_label.setField('pcgs_actual',pcgs_actual)

    """ START PRINT """
    printer_com.StartPrintJob()
    printer_com.Print(1,False)
    printer_com.EndPrintJob()

    return 

