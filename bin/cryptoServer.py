#! /usr/bin/python3
import pandas as pd
import datetime as dt
import pickle
import time
from coinbase.wallet.client import Client
print('Starting Server')
def getData():
    key = 'blank'
    secret = 'blank'
    client = Client(key, secret)

    date,time=client.get_time()['iso'][:-1].split('T')
    date=date.split('-')
    date=dt.date(int(date[0]),int(date[1]),int(date[2]))
    time=time.split(':')
    time=dt.time(int(time[0]),int(time[1]),int(time[2]))
    
    btc=float(client.get_buy_price(currency_pair='BTC-USD')['amount'])
    eth=float(client.get_buy_price(currency_pair='ETH-USD')['amount'])
    ltc=float(client.get_buy_price(currency_pair='LTC-USD')['amount'])
    return(date,time,btc,eth,ltc)
def writedb(database,dps):
    #dps is a list with data in the following order
    #date, time, btc, eth, ltc
    database['Date']+=[dps[0]]
    database['Time']+=[dps[1]]
    database['BTC']+=[dps[2]]
    database['ETH']+=[dps[3]]
    database['LTC']+=[dps[4]]
    return(0)
def storedb(directory, database):
    with open(directory,'wb') as fi:
        pickle.dump(pd.DataFrame.from_dict(database),fi)
    return(0)
    
db={'Date':[],'Time':[],'BTC':[],'ETH':[],'LTC':[]}

while(True):
#for j in range(4):
    for i in range(100):
        try:
            print(dt.datetime.now())
            writedb(db,getData())
            time.sleep(3)
        except:
            print('Error, will try again')
    datetime=dt.datetime.now().strftime('%Y%m%d%H%M%S')
    print('Storing at time ', dt.datetime.now())
    storedb('./raw_data/'+datetime,db)
    del(db)
    db={'Date':[],'Time':[],'BTC':[],'ETH':[],'LTC':[]}
print('Goodbye')
