import pandas as pd

from Database.getCoinData import getCoinData
from Database.createNewPO import createNewPOfunc

def updateTable(df, newPCGSNum):
    if len(df.index) == 1:
        df = getCoinData(int(newPCGSNum))
    else:
        newPCGSData = getCoinData(int(newPCGSNum))
        df = df[df['Grade'] != '']
        df = pd.concat([df,getCoinData(int(newPCGSNum))])
        print(df[df['Grade'] != ''])
    return df

