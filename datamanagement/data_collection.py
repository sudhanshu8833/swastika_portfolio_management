from .models import *
import yfinance as yf
import math
import pandas as pd
import time as tim
from smartapi import SmartConnect
from smartapi import SmartWebSocket
import traceback
from pytz import timezone
import json
from datetime import time, datetime
# import telepot
# bot = telepot.Bot("5448843199:AAEKjMn2zwAyZ5tu8hsLIgsakxoLf980BoY")
# bot.getMe()

# time.sleep(5)

import logging
logger = logging.getLogger('dev_log')




class run_strategy():

    def __init__(self, strategy):
        self.parameters = strategy
        self.ltp_prices={}
        self.times=tim.time()
        for i in range(100):
            try:
                self.obj = SmartConnect(api_key='NuTmF22y')
                data = self.obj.generateSession("Y99521", "abcd@1234")
                refreshToken = data['data']['refreshToken']
                self.feedToken = self.obj.getfeedToken()
                break
            except Exception as e:
                print(str(e))
                tim.sleep(1)

    def ltp_nifty_options(self,token_dict,dict_token):
        tim.sleep(.5)

        position_opened = positions.objects.filter(status='OPEN')
        positions_opened=[]
        tokens_used=[]
        for i in range(len(position_opened)):
            if position_opened[i].token not in tokens_used:
                tokens_used.append(position_opened[i].token)
                positions_opened.append(position_opened[i])


        for i in range(len(positions_opened)):
            
            try:
                with open('datamanagement/data.json') as file:
                    data=json.load(file)
                    data[positions_opened[i].token]=self.obj.ltpData("NFO", positions_opened[i].symbol, positions_opened[i].token)['data']['ltp']
                    tim.sleep(.5)
                    json_object = json.dumps(data, indent = 2)
                    with open("datamanagement/data.json","w") as write_file:
                        write_file.write(json_object)

                        
            except Exception as e:
                logger.info(str(e))
                print(str(e))

        with open('datamanagement/data.json') as file:
            data=json.load(file)
            data['26000']=self.obj.ltpData("NSE", 'NIFTY', "26000")['data']['ltp']
            print(data['26000'])
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


        
        while True:
            try:


                self.ltp_nifty_options(token_dict,dict_token)
                if time(15, 40) <= datetime.now(timezone("Asia/Kolkata")).time():
                    break


            except Exception:
                print(traceback.format_exc())








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

            print(price_buy)
            
            token_dict, dict_token=self.token_calculations(price_buy, self.parameters.expiry_1,{},{})
            token_dict, dict_token=self.token_calculations(price_buy, self.parameters.expiry_2,token_dict,dict_token)
 
            with open('datamanagement/data.json') as file:
                data=json.load(file)
                # data[position_opened[i].token]=self.obj.ltpData("NSE", position_opened[i].symbol, position_opened[i].token)['data']['ltp']
            # for key,value in dict_token.items():
            #     data[key]=self.obj.ltpData("NFO", value,key )['data']['ltp']
            
            json_object = json.dumps(data, indent = 2)

            with open("datamanagement/data.json","w") as write_file:
                write_file.write(json_object)

            value=self.websocket(token_dict, dict_token)
            return value
        except Exception:
            print(traceback.format_exc())
