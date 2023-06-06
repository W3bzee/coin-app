import pandas as pd


def getCoinInvoiceSerial(serial):
    invoiceDB = pd.read_csv(r'.\Database\Data\inventoryCoins.csv')
    """ PARSE SERIAL """
    try:
        row = invoiceDB[invoiceDB['UniqueID'] == serial]

        dataToAppend = {'ID #':row['UniqueID'].iloc[0],
                        'PCGS #':row['PCGS #'].iloc[0],
                        'Description':row['Description'].iloc[0],
                        'Grade':row['Grade'].iloc[0],
                        'Service':row['Service'].iloc[0],
                        'CAC': '' if row['CAC'].isna().iloc[0] else int(row['CAC'].iloc[0]),
                        'Price': '' if row['Price'].isna().iloc[0] else int(row['Price'].iloc[0]),
                        'Certification ID':row['Certification ID'].iloc[0],
                        'Addl. Description':row['Addl. Description'].iloc[0]}

    except:
        print('Not in purchaseOrderCoins DB')
        uniqueID = serial
        Grade = ''
        Certification_ID_num = ''
        dataToAppend = {'ID #':'','PCGS #':'','Description':'','Grade':'','Service':'','CAC':'','Price':'','Certification ID':'','Addl. Description':''}


    newCoinDF = pd.DataFrame(data=dataToAppend,columns=['ID #','PCGS #','Description','Grade','Service','CAC','Price','Certification ID','Addl. Description'],index=['001'])

    return newCoinDF



