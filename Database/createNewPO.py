import pandas as pd
import numpy as np

def createNewPOfunc():
    newPODF = pd.DataFrame(columns=['PCGS #','Description','Grade','Service','CAC','Cost','Price','Certification ID','Addl. Description'],index=['001'])
    newPODF.loc['001'] = [''] *len(newPODF.columns)
    return newPODF

