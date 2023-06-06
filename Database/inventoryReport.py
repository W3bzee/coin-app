import pandas as pd

def getReportData():
    countPO = pd.read_csv('Database\Data\purchaseOrders.csv').shape[0]-1
    countInvoices = pd.read_csv('Database\Data\invoices.csv').shape[0]-1
    countCoinsInventory = pd.read_csv('Database\Data\inventoryCoins.csv').shape[0]
    pricePaid = pd.read_csv('Database\Data\purchaseOrderCoins.csv')['Cost'].sum()
    priceSold = pd.read_csv('Database\Data\invoiceCoins.csv')['Price'].sum()
    
    return countPO, countInvoices, countCoinsInventory, pricePaid, priceSold
    