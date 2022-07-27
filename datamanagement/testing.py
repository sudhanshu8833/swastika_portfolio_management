# from .models import *
import yfinance as yf
import math
import pandas as pd
import time
from smartapi import SmartConnect
from smartapi import SmartWebSocket
import traceback
import requests
import telepot

obj = SmartConnect(api_key="uWbpZyYm")
data = obj.generateSession("S776051", "Madhya246###")
refreshToken = data['data']['refreshToken']
feedToken = obj.getfeedToken()
userProfile = obj.getProfile(refreshToken)

def this_scripts():

    url="https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
    data=requests.get(url=url)
    data=data.json()
    df = pd.DataFrame(data)

    df1=pd.DataFrame()

    df1=df[:1]
    print(df1)


    for i in range(len(df)):
        print(i)

        if 'NIFTY' in df['symbol'][i][:6] and 'NFO' in df['exch_seg'][i]:
            df1.loc[len(df1.index)] = df.loc[i] 
        else:
            continue
    print(df)

    df1.to_csv("scripts.csv")

this_scripts()