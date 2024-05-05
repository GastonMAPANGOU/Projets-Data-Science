#!/usr/bin/env python
# coding: utf-8

# In[58]:


import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime,timedelta
delta = timedelta(
     days=50,
    seconds=27,
   microseconds=10,
    milliseconds=29000,
    minutes=5,
    hours=8,
    weeks=2
 )

actionid="RNO.PA"


# In[59]:


def plotData(df, columns):
    df[columns].plot(figsize=(20,10))
    plt.figure()


    plt.show()


# In[60]:


def diff(a,b):
    if a-b>0:
        return True
    elif a-b==0 :
        return None
    elif a-b<0:
        return False


# In[61]:


def calculforgraphs(actionid,multiplier,period):
    action = yf.Ticker(actionid)
    myDate = datetime.now(); 
    bollingerfirstdate=myDate-timedelta(days=365*4)
    before20=""+str(bollingerfirstdate.year)+"-"+str(bollingerfirstdate.month)+"-"+str(bollingerfirstdate.day)
    bollinger= pd.DataFrame()
    bollinger = action.history(start=before20, end=myDate, interval="1d")
    bollinger['MMperiod']=bollinger['Close'].rolling(period).mean()
    bollinger['MM20']=bollinger['Close'].rolling(20).mean()
    bollinger['MM50']=bollinger['Close'].rolling(50).mean()
    bollinger['UpperBand'] = bollinger['Close'].rolling(period).mean() + bollinger['Close'].rolling(period).std() * multiplier
    bollinger['LowerBand'] = bollinger['Close'].rolling(period).mean() - bollinger['Close'].rolling(period).std() * multiplier
    bollinger['e26'] = pd.Series.ewm(bollinger['Close'], span=26).mean()
    bollinger['e12'] = pd.Series.ewm(bollinger['Close'], span=12).mean()
    bollinger['MACD'] = bollinger['e12'] - bollinger['e26']
    bollinger['signal'] = pd.Series.ewm(bollinger['MACD'], span=9).mean()
    
    return bollinger


# In[62]:


def plotBollinger(actionid):
    plotData(calculforgraphs(actionid,2,20), ['Close','MMperiod','UpperBand','LowerBand'])


# In[63]:


def plotMACD(actionid):
    plotData(calculforgraphs(actionid,2,20), ['MACD','signal','e26','e12'])
    
def plotMM(actionid):
    plotData(calculforgraphs(actionid,2,20), ['MM20','MM50'])


# In[64]:


plotMACD(actionid)


# In[65]:


plotBollinger(actionid)


# In[66]:


plotMM(actionid)

