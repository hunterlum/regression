
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import re
import datetime 
import time
import copy
import math
from decimal import *
import matplotlib.pyplot as plt
from matplotlib import interactive

import matplotlib.patches as mpatches

from gplearn.genetic import SymbolicRegressor
from sklearn import tree
from sklearn import ensemble
import matplotlib.dates
import pytz


# In[2]:


class Crypto:
    def __init__(self,path="./data/temp2.txt",pr=False):
        self.path=path
        self.data=pd.read_csv(path, sep=" ")
        if pr:
            print("PROCESSING DATAFRAME PHASE\n")
            print("Before datetime change: \n")
            print(self.data.head())
            print(type(self.data["Y:M:D:h:m:s"][0]))
        strvtime=np.vectorize(datetime.datetime.strptime)
        time_array=strvtime(list(map(str,self.data['Y:M:D:h:m:s'])),"%Y:%m:%d:%H:%M:%S")
        self.data['Y:M:D:h:m:s']=time_array
        if pr:
            print("\nAfter datetime change: \n")
            print(self.data.head())
            print(type(self.data["Y:M:D:h:m:s"][0]))
            print(type(self.data["Ti-T0"][0]))
            
            
        self.startDate=self.data["Y:M:D:h:m:s"][0]
        self.endDate=self.data["Y:M:D:h:m:s"][self.data.shape[0]-1]
        
    def head(self):
        print ("Head: \n",self.data.head(),"\nTail: \n",self.data.tail())

    def datFuncScalar(self,t,curr='BTC',L=0,R=0):
        if (R==0):
            R=self.data.shape[0]-1

        if((t<self.data.iloc[L,4]) or (t>self.data.iloc[R,4])):
            raise Exception("Index out of Bounds")
        mid=int((R-L)/2)
    
        while(mid>0):
            if(self.data.iloc[L+mid,4]==t):
            #print(1,L,L+mid,R,": ",self.data.iloc[L+mid,4])
                return(float(self.data.loc[L+mid,curr]))
            elif(self.data.iloc[L+mid,4]<t):
            #print(3,L,L+mid,R,": ",self.data.iloc[L+mid,4])
                L=L+mid
                mid=int((R-L)/2)
            elif(self.data.iloc[L+mid,4]>t):
            #print(4,L,L+mid,R,": ",self.data.iloc[L+mid,4])
                R=L+mid
                mid=int((R-L)/2)
        #print(2,L,L+mid,R,": ",self.data.iloc[L+mid,4])
        lamb=(self.data.iloc[R,4]-t)/(self.data.iloc[R,4]-self.data.iloc[L,4])
        return(float (lamb*self.data.loc[L,curr]+(1-lamb)*self.data.loc[R,curr]))

    def datFunc(self,t,curr='BTC'):
        function=np.vectorize(self.datFuncScalar)
        return(function(t,curr=curr))
    
    def dateFuncScalar(self,date,curr='BTC'):
        #function of data given DATE!
        date=date.replace(tzinfo=None)
        return(self.datFunc((date-self.startDate.replace(tzinfo=None)).total_seconds(),curr=curr))
    
    def dateFunc(self,t,curr='BTC'):
        function=np.vectorize(self.dateFuncScalar)
        return(function(t,curr=curr))
    
    def datePart(self,n):
        dt=(self.endDate-self.startDate).total_seconds()
        sec=np.concatenate([np.arange(0,dt,dt/n),[dt]])
        timeDelta=np.vectorize(lambda x:datetime.timedelta(seconds=int(x)))(sec)
        return(sec,timeDelta,timeDelta+self.startDate)


    def lsArr(self,startDate,endDate,freq=3600,past=datetime.timedelta(seconds=24*3600*7),n=5,curr='BTC'):
        """
        input:
            startDate:datetime
            endDate:datetime
            freq=int(sec)
            past=timedelta
            n=int
            curr='BTC,LTC,ETH'
        """
        assert(startDate+past<endDate)
        dt=past.total_seconds()
        deltaSec=np.concatenate([np.arange(0,dt,dt/n),[dt]])
        #timeDelta=np.vectorize(lambda x:datetime.timedelta(seconds=int(x)))(sec)

        t0=startDate+past-self.startDate
        t1=endDate-self.startDate
        sec=np.concatenate([np.arange(t0.total_seconds(),t1.total_seconds(),freq),[t1.total_seconds()]])
        y=self.datFunc(sec,curr=curr)
        time=np.vectorize(lambda x:datetime.timedelta(seconds=int(x)))(sec)+self.startDate
        assert(time[0]-past==startDate)

        X=sec.reshape(-1,1)-deltaSec[1]
        for i in range(2,len(deltaSec)):
            X=np.concatenate([X,sec.reshape(-1,1)-deltaSec[i]],axis=1)
        X=self.datFunc(X,curr=curr)
        X=np.concatenate([sec.reshape(-1,1),X],axis=1)
        for i in range(int(len(y)/100)):
            assert self.dateFuncScalar(time[i],curr=curr)==y[i]
            assert self.datFuncScalar(X[i,0],curr=curr)==y[i]
        assert(sec[0]==X[0][0])
        assert(datetime.timedelta(seconds=sec[0])+self.startDate==startDate+past)
        for j in range(int(len(y)/100)):
            for i in range(1,len(deltaSec)):
                assert(X[j][i]==self.datFunc(sec[j]-deltaSec[i],curr=curr))
        return((y,time,X))

    def train(self,regList,lis):
        for i in regList:
            i.fit(lis[2],lis[0])
        return(regList)
    
    def predict(self,regList,lis):
        yArr=np.empty([lis[2].shape[0],len(regList)])
        for i in range(len(regList)):
            yArr[:,i]=regList[i].predict(lis[2])
        return (yArr)
    
    def plot(self,yArr,lis,col,label):
        for i in range(yArr.shape[1]):
            plt.plot_date(lis[1],yArr[:,i],col[i],label=label[i]) 
        plt.xticks(rotation=50)
        plt.legend()
        plt.show()
        return(None)
    

