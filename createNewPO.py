import pandas as pd
import numpy as np

def createNewPOfunc():
    
    newPODF = pd.DataFrame(columns=['PCGS #','Description','Grade','Service','CAC','Cost','Price','Certification ID','Addl. Description'],index=np.arange(1,15))
    return newPODF
