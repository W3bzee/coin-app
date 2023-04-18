import pandas as pd


serials = ['0074556606659252',
           '01642564006483309016',
           '01425162003056392017',
           '0056706402309935',
           '0153226563659815']



def getCoinDataSerial(serial):
    coinDB = pd.read_csv(r'C:\Users\nlebh\Documents\GitHub\coin-app\Database\Data\coinDB.csv')

    """ PARSE SERIAL """
    try:
        service = 'PCGS' if serial[0:2] == '00' else 'NGC'
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
        dataToAppend = {'PCGS #':'','Description':'','CAC':'','Cost':'','Price':'','Certification ID':'','Addl. Description':''}

    dataToAppend = {'PCGS #':Pcgs_no,'Description':f'{0}-{Grade}-{service}'.format(row['Denomination'].iloc[0]),'CAC':'','Cost':'','Price':'','Certification ID':Certification_ID_num,'Addl. Description':row['coin_no'].iloc[0]}
    newCoinDF = pd.DataFrame(data=dataToAppend,columns=['PCGS #','Description','CAC','Cost','Price','Certification ID','Addl. Description'],index=['001'])

    return newCoinDF
