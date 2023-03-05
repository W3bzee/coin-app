import pandas as pd


def getCoinData(serial):
    coinDB = pd.read_csv(r'C:\Users\nlebh\Documents\GitHub\coin-app\Database\Data\coinDB.csv')
    row = coinDB[coinDB['Pcgs_no'] == serial].iloc[-1]
    dataToAppend = {'PCGS #':row['Pcgs_no'],'Description':row['Denomination'],'Grade':63,'Service':row['Service'],'CAC':'','Cost':'','Price':'','Certification ID':row['coin_no'],'Addl. Description':''}
    newCoinDF = pd.DataFrame(data=dataToAppend,columns=['PCGS #','Description','Grade','Service','CAC','Cost','Price','Certification ID','Addl. Description'],index=['001'])

    return newCoinDF
