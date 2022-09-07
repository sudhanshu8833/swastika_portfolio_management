from .models import *
import yfinance as yf
import math
import pandas as pd
import time
from smartapi import SmartConnect
from smartapi import SmartWebSocket
import traceback
from pytz import timezone
import json
# import telepot
# bot = telepot.Bot("5448843199:AAEKjMn2zwAyZ5tu8hsLIgsakxoLf980BoY")
# bot.getMe()

# time.sleep(5)

import logging
logger = logging.getLogger('dev_log')

from datetime import datetime


class run_strategy():

    def __init__(self, strategy):
        self.parameters = strategy
        self.ltp_prices={}
        self.times=time.time()
        for i in range(100):
            try:
                self.obj = SmartConnect(api_key='NuTmF22y')
                data = self.obj.generateSession("Y99521", "abcd@1234")
                refreshToken = data['data']['refreshToken']
                self.feedToken = self.obj.getfeedToken()
                break
            except Exception as e:
                print(str(e))
                time.sleep(1)

    def ltp_nifty_options(self, message,token_dict,dict_token):

        for i in range(len(message)):
            if 'ltp' in message[i]:
                try:
                    with open('datamanagement/data.json') as file:
                        data=json.load(file)
                        data[str(message[i]['tk'])]=str(message[i]['ltp'])
                        json_object = json.dumps(data, indent = 2)
                        with open("datamanagement/data.json","w") as write_file:
                            write_file.write(json_object)

                            
                except Exception as e:
                    logger.info(str(e))

        with open('datamanagement/data.json') as file:
            data=json.load(file)
            data['26000']=self.obj.ltpData("NSE", 'NIFTY', "26000")['data']['ltp']
            json_object = json.dumps(data, indent = 2)
            with open("datamanagement/data.json","w") as write_file:
                write_file.write(json_object)


    def calculate_websocket_token(self,token_dict, dict_token):
        token=""
        lists=[]
        for key,value in token_dict.items():
            lists.append(value)

        token=""
        for i in range(len(lists)):
            token=token+"nse_fo|"+str(lists[i])

            if i==len(lists)-1:
                token=token
            else:
                token=token+'&'

        return token

    def websocket(self,token_dict, dict_token):


        # feed_token=092017047
        FEED_TOKEN=self.feedToken
        CLIENT_CODE="Y99521"
        # token="mcx_fo|224395"
        token=self.calculate_websocket_token(token_dict, dict_token)    #SAMPLE: nse_cm|2885&nse_cm|1594&nse_cm|11536&nse_cm|3045
        # token="mcx_fo|226745&mcx_fo|220822&mcx_fo|227182&mcx_fo|221599"
        task="mw"   # mw|sfi|dp

        ss = SmartWebSocket(FEED_TOKEN, CLIENT_CODE)

        # bot.sendMessage(1039725953,"websocket connection is being stablished")

        def on_message(ws, message):

            try:
                print(message)

                self.ltp_nifty_options(message,token_dict,dict_token)

            except Exception:
                print(traceback.format_exc())

        def on_open(ws):
            print("on open")
            ss.subscribe(task,token)
            
        def on_error(ws, error):
            print(error)
            
        def on_close(ws):
            
            ss._on_open = on_open
            ss._on_message = on_message
            ss._on_error = on_error
            ss._on_close = on_close

            ss.connect()

            return False

        # Assign the callbacks.
        ss._on_open = on_open
        ss._on_message = on_message
        ss._on_error = on_error
        ss._on_close = on_close

        ss.connect()






    def token_calculations(self, nifty_price, expiry,token_dict,dict_token):
       
        strike_prices = []

        spot = round(nifty_price/50, 0)*50


        low_vix = spot-600
        high_vix = spot+600

        spot_value = low_vix

        while spot_value <= high_vix:
            strike_prices.append(spot_value)
            spot_value += 50

        df = pd.read_csv('datamanagement/scripts.csv')
        # token_dict = {}
        # dict_token = {}
        for i in range(len(df)):
            for j in range(len(strike_prices)):
                symbol = str(expiry)+str(int(strike_prices[j]))
                if symbol in df['symbol'][i]:
                    token_dict[str(df['symbol'][i])] = str(df['token'][i])
                    dict_token[str(df['token'][i])] = str(df['symbol'][i])


        return token_dict, dict_token




    def run(self):
        try:

            
            price_buy = self.obj.ltpData("NSE", 'NIFTY', "26000")['data']['ltp']


            
            token_dict, dict_token=self.token_calculations(price_buy, self.parameters.expiry_1,{},{})
            token_dict, dict_token=self.token_calculations(price_buy, self.parameters.expiry_2,token_dict,dict_token)


            value=self.websocket(token_dict, dict_token)
            return value
        except Exception:
            print(traceback.format_exc())
