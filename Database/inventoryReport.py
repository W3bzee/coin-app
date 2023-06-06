import pandas as pd
import locale
locale.setlocale( locale.LC_ALL, '' )


def getReportData():
    countPO = pd.read_csv('Database\Data\purchaseOrders.csv').shape[0]-1
    countInvoices = pd.read_csv('Database\Data\invoices.csv').shape[0]-1
    countCoinsInventory = pd.read_csv('Database\Data\inventoryCoins.csv').shape[0]
    pricePaid = locale.currency(pd.read_csv('Database\Data\purchaseOrderCoins.csv')['Cost'].sum(),grouping=True )
    priceSold = locale.currency(pd.read_csv('Database\Data\invoiceCoins.csv')['Price'].sum(),grouping=True )

    return countPO, countInvoices, countCoinsInventory, pricePaid, priceSold
    
