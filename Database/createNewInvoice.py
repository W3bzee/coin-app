import pandas as pd
import numpy as np

def createNewInvoicefunc():
    newInvoiceDF = pd.DataFrame(columns=['ID #','PCGS #','Description','Grade','Service','CAC','Price','Certification ID','Addl. Description'],index=['001'])
    newInvoiceDF.loc['001'] = [''] *len(newInvoiceDF.columns)
    return newInvoiceDF