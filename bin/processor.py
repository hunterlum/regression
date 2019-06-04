
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import datetime as dt
import os


# # Predefined Functions

# Functions used in the processor class

# In[2]:


def read_pickles(base):
    '''Returns a list of dataframes from 
    data located in the base directory'''
    return(list(map(lambda x: pd.read_pickle(base+x),os.listdir(base))))

def sortandfilter(combinedDf):
    combinedDf=combinedDf[['Date','Time','BTC','ETH','LTC']]
    #Sort by date and time
    combinedDf=combinedDf.sort_values(by=['Date','Time'])
    #Create filter to get unique values
    #the first instance of repeated values is returned
    btc=np.array(combinedDf['BTC'][:-1])!=np.array(combinedDf['BTC'][1:])
    ltc=np.array(combinedDf['LTC'][:-1])!=np.array(combinedDf['LTC'][1:])
    eth=np.array(combinedDf['ETH'][:-1])!=np.array(combinedDf['ETH'][1:])
    filterArr=np.append(True,np.logical_or(btc,eth,ltc).reshape(-1,1))
    #apply filter
    combinedDf=combinedDf[filterArr]
    combinedDf.index=range(combinedDf.shape[0])
    return(combinedDf)

#Functions used to remove duplicate datetime values
#pandas has a function to drop duplicates
#it may be worthwhile to reimplement this portion
def combine(x):
    '''Create datetime object from date and time'''
    return(dt.datetime.combine(x[0],x[1]))

def rm_duplicate_dates(df,v=False):
    '''Remove rows that have identical datetimes
    Keep only the first instance of the duplicate datetime'''
    dtls=df[['Date','Time']]
    dtls=list(map(combine,list(zip(dtls['Date'],dtls['Time']))))

    #f means filter
    fdtls=list(np.array(dtls[:-1])<np.array(dtls[1:]))+[True]
    #n is the negation of the filter
    nfdtls=np.invert(fdtls)

    temp=df.loc[fdtls]
    temp.index=range(temp.shape[0])
    if(v):
        print('Shape of dataframe\nBefore Cleaning:',df.shape)
        print('After Cleaning: ',temp.shape)
    return(temp)


# # Processor Class

# In[3]:


class processor:
    '''Class used to transform raw data into structured tables'''
    def __init__(self,base='data/cryptoData',path=None):
        temp=pd.read_pickle(base)
        
        if(path!=None):
            temp=pd.concat(read_pickles(path)+[temp],sort=False)   
        print('Shape of combined df: ',temp.shape)    

        temp=sortandfilter(temp)
        print('After removing duplicate prices: ',temp.shape)

        temp=rm_duplicate_dates(temp)
        print('After removing duplicate datetimes: ', temp.shape)
        
        #output prepared data
        self.data=temp
        return(None)
    
    def save_file(self,name='./cryptoData'):
        self.data.to_pickle(name)
        self.data.to_csv(name+'.csv',index=False)
        
        


# # Sample Usage

# In[4]:


#data=processor(base='data/cryptoData',path=None)
#data.save_file('data/cryptoData')

