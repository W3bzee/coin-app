import pandas as pd
import numpy as np



def pcgsCoinLookup(coinNum):
    filePath = r'C:\Users\nlebh\Documents\GitHub\coin-app\exampleDF.csv'
    df = pd.read_csv(filePath)
    df = df.drop(columns=['Unnamed: 0'])
    df['COIN #'] = df['COIN #'].apply(int)
    rowdata = df.loc[df['COIN #'] == int(coinNum)]

    return rowdata


