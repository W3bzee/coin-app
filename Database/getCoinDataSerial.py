import pandas as pd


serials = ['0074556606659252',
           '01642564006483309016',
           '01425162003056392017',
           '0056706402309935',
           '0153226563659815']



"""

81609263006058497003 1937-D 3 LEGS BUFFALO NICKEL MS63 NGC/6058497-003
"""

def getCoinDataSerial(serial):    
    coinDB = pd.read_csv(r'.\Database\Data\coinDB.csv', encoding= 'unicode_escape')

    """ PARSE SERIAL """
    try:
        if (float(serial[0:6]) in coinDB['coin_no'].to_list()) and (serial[0:3]!='100') and (serial[0:3]!='000') and (serial[0:2]!='00') and (serial[0:2]!='01') and (serial[0:2]!='08'):
            row = coinDB[coinDB['coin_no'] == float(serial[0:6])]
            Grade = serial[6:8]
            Certification_ID_num = serial[10:]
            if row.empty:
                dataToAppend = {'PCGS #':'','Description':'','Grade':'','Service':'','CAC':'','Cost':'','Price':'','Certification ID':'','Addl. Description':''}
            else:
                dataToAppend = {'PCGS #':row['Pcgs_no'].iloc[0],'Description':row['Coin_date_Denomination_Variety'].iloc[0],'Grade':Grade,'Service':row['Service'].iloc[0],'CAC':'','Cost':'','Price':'','Certification ID':Certification_ID_num,'Addl. Description':row['coin_no'].iloc[0]}
                newCoinDF = pd.DataFrame(data=dataToAppend,columns=['PCGS #','Description','Grade','Service','CAC','Cost','Price','Certification ID','Addl. Description'],index=['001'])
                return newCoinDF

        if (serial[0:3] == '100' or serial[0:3]=='000'):
            serial = serial[3:]
            serial = serial[0:6]+serial[8:]
        service = 'PCGS' if (serial[0:2] == '00' or serial[0:2] == '08') else 'NGC'
        serial = serial[2::]
        Pcgs_no = int(serial[0:4])
        Grade = int(serial[4:6])
        Certification_ID_num = int(serial[6:-1])
    except:
        print('Different Serial')
        Pcgs_no = int(serial)
        Grade = ''
        Certification_ID_num = ''

    """ GET CORRESPONDING ROW & RETURN DATAFRAME """
    row = coinDB[coinDB['Pcgs_no'] == Pcgs_no][coinDB['Service']==service]

    if row.empty:
        dataToAppend = {'PCGS #':'','Description':'','Grade':'','Service':'','CAC':'','Cost':'','Price':'','Certification ID':'','Addl. Description':''}

    dataToAppend = {'PCGS #':Pcgs_no,'Description':row['Coin_date_Denomination_Variety'].iloc[0],'Grade':Grade,'Service':service,'CAC':'','Cost':'','Price':'','Certification ID':Certification_ID_num,'Addl. Description':row['coin_no'].iloc[0]}
    newCoinDF = pd.DataFrame(data=dataToAppend,columns=['PCGS #','Description','Grade','Service','CAC','Cost','Price','Certification ID','Addl. Description'],index=['001'])

    return newCoinDF
