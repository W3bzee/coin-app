import pandas as pd

from Database.getCoinInvoiceSerial import getCoinInvoiceSerial

def updateInvoiceTableSerial(df, serial):
    if df['ID #'].iloc[0] == '':
        df = getCoinInvoiceSerial(serial)
    else:
        newPCGSData = getCoinInvoiceSerial(serial)
        df = df.dropna(subset=['ID #'], how='any', axis=0)
        df = df[df['ID #'] != '']
        df = pd.concat([df,getCoinInvoiceSerial(serial)])

    return df