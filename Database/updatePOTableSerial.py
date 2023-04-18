import pandas as pd

from Database.getCoinDataSerial import getCoinDataSerial

def updateTableSerial(df, serial):
    if len(df.index) == 1:
        df = getCoinDataSerial(serial)
    else:
        newPCGSData = getCoinDataSerial(serial)
        df = df[df['Grade'] != '']
        df = pd.concat([df,getCoinDataSerial(serial)])

    return df