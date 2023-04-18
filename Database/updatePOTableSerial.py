import pandas as pd

from Database.getCoinDataSerial import getCoinDataSerial

def updateTableSerial(df, serial):
    if len(df.index) == 1:
        df = getCoinDataSerial(serial)
    else:
        newPCGSData = getCoinDataSerial(serial)
        df.drop(index=df.index[-1],axis=0,inplace=True)
        df = pd.concat([df,getCoinDataSerial(serial)])

    return df