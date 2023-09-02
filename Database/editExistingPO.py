import pandas as pd

def getCoinFromTCSLabel(barcode):
    poCoinsDB = pd.read_csv(r'.\Database\Data\purchaseOrderCoins.csv')
    """ PARSE SERIAL """
    try:
        dataToAppend = poCoinsDB[poCoinsDB['UniqueID'].str.startswith(barcode.split('-')[0])]
        print(poCoinsDB['UniqueID'].str)
        dataToAppend = dataToAppend.drop(columns=['UniqueID'])
        

    except:
        print('Not in purchaseOrderCoins DB')
        uniqueID = barcode
        Grade = ''
        Certification_ID_num = ''
        dataToAppend = {'ID #':'','PCGS #':'','Description':'','Grade':'','Service':'','CAC':'','Cost':'','Price':'','Certification ID':'','Addl. Description':''}


            # Create a new DataFrame from the filtered data
    newCoinDF = pd.DataFrame(dataToAppend.values,
                                 columns=['PCGS #','Description','Grade','Service','CAC','Cost','Price','Certification ID','Addl. Description'])

    return newCoinDF



def getPOInfoFromBarcode(barcode):

    POnum = barcode.split('-')[0]
    poDB = pd.read_csv(r'.\Database\Data\purchaseOrders.csv')

    return poDB[poDB['PO'] == int(POnum)]

