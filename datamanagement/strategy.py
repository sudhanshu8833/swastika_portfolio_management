from .models import *
import yfinance as yf
import math
import pandas as pd
import time
from smartapi import SmartConnect
from smartapi import SmartWebSocket
import traceback

import telepot
bot = telepot.Bot("5448843199:AAEKjMn2zwAyZ5tu8hsLIgsakxoLf980BoY")
bot.getMe()

obj = SmartConnect(api_key="uWbpZyYm")
data = obj.generateSession("S776051", "Madhya246###")
refreshToken = data['data']['refreshToken']
feedToken = obj.getfeedToken()
userProfile = obj.getProfile(refreshToken)

from datetime import datetime


class run_strategy():

    def __init__(self, strategy):
        self.parameters = strategy
        self.ltp_prices={}
        self.times=time.time()

    def ltp_nifty_options(self, message):

        for i in range(len(message)):
            if 'ltp' in message[i]:
                try:
                    self.ltp_prices[str(message[i]['tk'])]=str(message[i]['ltp'])
                except:
                    pass
        self.ltp_prices['26000']=obj.ltpData("NSE", 'NIFTY', "26000")['data']['ltp']
        # self.ltp_prices['79929']=45
        # self.ltp_prices['79972']=55
        # self.ltp_prices['79912']=55
        # self.ltp_prices['79928']=55
        # print(self.ltp_prices)

    def shift_position(self,nifty_price,token_dict, dict_token):

        position_opened=positions.objects.filter(strategy_id=str(self.parameters.strategy_id),status='OPEN',side='SHORT')
        print(position_opened.all())
        for i in range(len(position_opened)):
            position_opened[i].status="CLOSED"
            position_opened[i].time_out=datetime.now()
            position_opened[i].price_out=float(self.ltp_prices[position_opened[i].token])
            position_opened[i].save()

            p=self.add_orders(position_opened[i].symbol,"BUY",float(self.ltp_prices[position_opened[i].token]),False)


        strike_price=round(nifty_price/50, 0)*50

        if self.parameters.expiry_selected==0:
            expiry=self.parameters.expiry_1

        if self.parameters.expiry_selected==1:
            expiry=self.parameters.expiry_2

        symbol_pe=expiry+str(int(strike_price+self.parameters.sell_factor))+'PE'
        symbol_ce=expiry+str(int(strike_price+self.parameters.sell_factor))+'CE'


        p=self.add_positions(symbol_pe,'SHORT',float(self.ltp_prices[token_dict[symbol_pe]]),0,0,token_dict, dict_token)
        p=self.add_positions(symbol_ce,'SHORT',float(self.ltp_prices[token_dict[symbol_ce]]),0,0,token_dict, dict_token)
        p=self.add_orders(symbol_pe,"SELL",float(self.ltp_prices[token_dict[symbol_pe]]),True,token_dict, dict_token)
        p=self.add_orders(symbol_ce,"SELL",float(self.ltp_prices[token_dict[symbol_ce]]),True,token_dict, dict_token)



    def close_all_positions(self,token_dict, dict_token):

        position_opened=positions.objects.filter(strategy_id=str(self.parameters.strategy_id),status='OPEN')

        for i in range(len(position_opened)):
            position_opened[i].status="CLOSED"
            position_opened[i].time_out=datetime.now()
            position_opened[i].price_out=float(self.ltp_prices[position_opened[i].token])
            position_opened[i].save()

            if position_opened[i].side=="SHORT":
                p=self.add_orders(position_opened[i].symbol,"BUY",float(self.ltp_prices[position_opened[i].token]),False,token_dict, dict_token)


            if position_opened[i].side=="LONG":
                p=self.add_orders(position_opened[i].symbol,"SELL",float(self.ltp_prices[position_opened[i].token]),False,token_dict, dict_token)
                
        self.parameters.status="CLOSED"
        self.parameters.save()


    def main(self,token_dict, dict_token):

        position_opened=positions.objects.filter(strategy_id=str(self.parameters.strategy_id),status='OPEN',side='SHORT')


        if (float(self.ltp_prices['26000'])> self.parameters.T4 and self.parameters.T_now==3) or time.time()>self.times+60:
            # bot.sendMessage(1039725953,"position shifting")
            self.shift_position(float(self.ltp_prices['26000']),token_dict, dict_token)
            self.parameters.T_now=4
            self.parameters.save()

        if float(self.ltp_prices['26000'])> self.parameters.T5 and self.parameters.T_now==4:
            bot.sendMessage(1039725953,"closing position")
            self.close_all_positions(token_dict, dict_token)



        if float(self.ltp_prices['26000'])< self.parameters.T3 and self.parameters.T_now==4:
            bot.sendMessage(1039725953,"position shifting")
            self.shift_position(float(self.ltp_prices['26000']),token_dict, dict_token)
            self.parameters.T_now=3
            self.parameters.save()



        if float(self.ltp_prices['26000'])< self.parameters.T2 and self.parameters.T_now==3:
            bot.sendMessage(1039725953,"position shifting")
            self.shift_position(float(self.ltp_prices['26000']),token_dict, dict_token)
            self.parameters.T_now=2
            self.parameters.save()


        if float(self.ltp_prices['26000'])< self.parameters.T1 and self.parameters.T_now==2:
            bot.sendMessage(1039725953,"closing position")
            self.close_all_positions(token_dict, dict_token)




        if float(self.ltp_prices['26000'])> self.parameters.T3 and self.parameters.T_now==2:
            bot.sendMessage(1039725953,"position shifting")
            self.shift_position(float(self.ltp_prices['26000']),token_dict, dict_token)
            self.parameters.T_now=3
            self.parameters.save()


        for i in range(len(position_opened)):


            if float(self.ltp_prices[position_opened[i].token])< self.parameters.ET:
                bot.sendMessage(1039725953,"closing position")
                self.close_all_positions(token_dict, dict_token)


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
        FEED_TOKEN=feedToken
        CLIENT_CODE="S776051"
        # token="mcx_fo|224395"
        token=self.calculate_websocket_token(token_dict, dict_token)    #SAMPLE: nse_cm|2885&nse_cm|1594&nse_cm|11536&nse_cm|3045
        # token="mcx_fo|226745&mcx_fo|220822&mcx_fo|227182&mcx_fo|221599"

        task="mw"   # mw|sfi|dp

        ss = SmartWebSocket(FEED_TOKEN, CLIENT_CODE)

        bot.sendMessage(1039725953,"websocket connection is being stablished")

        def on_message(ws, message):

            try:
                # print("Ticks: {}".format(message))
                self.ltp_nifty_options(message)
                self.main(token_dict, dict_token)
            except Exception:
                print(traceback.format_exc())

        def on_open(ws):
            print("on open")
            ss.subscribe(task,token)
            
        def on_error(ws, error):
            print(error)
            
        def on_close(ws):
            print("Close")

        # Assign the callbacks.
        ss._on_open = on_open
        ss._on_message = on_message
        ss._on_error = on_error
        ss._on_close = on_close

        ss.connect()



    def vix_calculation(self, price):

        print(self.parameters.working_days_1)
        working_days_1 = self.parameters.working_days_1
        working_days_2 = self.parameters.working_days_2

        if working_days_1!=0:

            vix_price = float(yf.download(
                "^INDIAVIX", period='1D', interval="1D")['Close'][-1])

            days_vix = vix_price / (math.sqrt(252/working_days_1))

            nifty_range = price*days_vix*(1-vix_price/100)/100
            v_factor = round(nifty_range/50, 0)*50

        else:
            v_factor=0
        if v_factor < self.parameters.buy_factor:

            vix_price = float(yf.download(
                "^INDIAVIX", period='1D', interval="1D")['Close'][-1])

            days_vix = vix_price / (math.sqrt(252/working_days_2))

            nifty_range = price*days_vix*(1-vix_price/100)/100
            v_factor = round(nifty_range/50, 0)*50


            expiry = self.parameters.expiry_2
            self.parameters.expiry_selected=1
            self.parameters.save()

        else:
            expiry = self.parameters.expiry_1
            self.parameters.expiry_selected=0
            self.parameters.save()



        self.parameters.v_factor=v_factor
        self.parameters.save()

        return v_factor

    def add_orders(self,symbol,side,price,open_position,token_dict, dict_token):
        strategy1=orders(

            strategy_id=self.parameters.strategy_id,
            symbol=symbol,
            time=datetime.now(),
            price=price,
            transaction_type=side,
            open_position=open_position,
            order_id=0
        )
        strategy1.save()

    def add_positions(self,symbol,side,price_in,time_out,price_out,token_dict, dict_token):


        strategy1=positions(

            strategy_id=self.parameters.strategy_id,
            symbol=symbol,
            time_in=datetime.now(),
            side=str(side),
            price_in=float(price_in),
            time_out=datetime.now(),
            price_out=float(price_out),
            status="OPEN",
            token=str(token_dict[symbol])
        )
        strategy1.save()


    def market_order(self, nifty_price, v_factor, expiry,token_dict, dict_token,limit):
        nifty_price=round(nifty_price/50, 0)*50



        symbol_buy_put=expiry+str(int(nifty_price+v_factor))+'PE'
        symbol_buy_call=expiry+str(int(nifty_price-v_factor))+'CE'

        symbol_sell_put=expiry+str(int(nifty_price+self.parameters.sell_factor))+'PE'
        symbol_sell_call=expiry+str(int(nifty_price-self.parameters.sell_factor))+'CE'

        symbol_buy_put_price=obj.ltpData("NFO", symbol_buy_put, token_dict[symbol_buy_put])['data']['ltp']
        symbol_buy_call_price=obj.ltpData("NFO", symbol_buy_call, token_dict[symbol_buy_call])['data']['ltp']
        symbol_sell_put_price=obj.ltpData("NFO", symbol_sell_put, token_dict[symbol_sell_put])['data']['ltp']
        symbol_sell_call_price=obj.ltpData("NFO", symbol_sell_call, token_dict[symbol_sell_call])['data']['ltp']

        if limit.lower()=="on":
            print("got into limit")
            while True:

                time_start=time.time()
                price_put=obj.ltpData("NFO", symbol_buy_put, token_dict[symbol_buy_put])['data']['ltp']*self.parameters.percentage_premium
                price_call=obj.ltpData("NFO", symbol_buy_call, token_dict[symbol_buy_call])['data']['ltp']*self.parameters.percentage_premium
                print("^^^^^^^^^^^^")
                print(price_put)
                print(price_call)
                print(self.parameters.time_out)
                print("^^^^^^^^^^^^")

                kem=0
                while time.time()<=time_start+self.parameters.time_out:
                    price_put_now=obj.ltpData("NFO", symbol_buy_put, token_dict[symbol_buy_put])['data']['ltp']
                    price_call_now=obj.ltpData("NFO", symbol_buy_call, token_dict[symbol_buy_call])['data']['ltp']
                    print("^^^^^^^^^^^^")
                    print(price_put_now,price_put)
                    print(price_call_now,price_call)
                    print("^^^^^^^^^^^^")
                    if price_put_now<price_put or price_call_now<price_call:
                        kem=1
                        break

                if kem==1:
                    break

        if limit.lower()=="on":
            symbol_buy_put_price=obj.ltpData("NFO", symbol_buy_put, token_dict[symbol_buy_put])['data']['ltp']
            symbol_buy_call_price=obj.ltpData("NFO", symbol_buy_call, token_dict[symbol_buy_call])['data']['ltp']
            symbol_sell_put_price=obj.ltpData("NFO", symbol_sell_put, token_dict[symbol_sell_put])['data']['ltp']
            symbol_sell_call_price=obj.ltpData("NFO", symbol_sell_call, token_dict[symbol_sell_call])['data']['ltp']


        p=self.add_positions(symbol_buy_put,"LONG",symbol_buy_put_price,0,0,token_dict, dict_token)
        p=self.add_positions(symbol_buy_call,"LONG",symbol_buy_call_price,0,0,token_dict, dict_token)
        p=self.add_positions(symbol_sell_put,"SHORT",symbol_sell_put_price,0,0,token_dict, dict_token)
        p=self.add_positions(symbol_sell_call,"SHORT",symbol_sell_call_price,0,0,token_dict, dict_token)

        p=self.add_orders(symbol_buy_put,"BUY",symbol_buy_put_price,True,token_dict, dict_token)
        p=self.add_orders(symbol_buy_call,"BUY",symbol_buy_call_price,True,token_dict, dict_token)
        p=self.add_orders(symbol_sell_put,"SELL",symbol_sell_put_price,True,token_dict, dict_token)
        p=self.add_orders(symbol_sell_call,"SELL",symbol_sell_call_price,True,token_dict, dict_token)
        
        print(self.parameters.T1)
        self.parameters.T3=nifty_price
        self.parameters.T4= self.parameters.spot +self.parameters.sell_factor+(self.parameters.v_factor-self.parameters.sell_factor)*(self.parameters.TP1/100)
        self.parameters.T5= self.parameters.spot +self.parameters.sell_factor+(self.parameters.v_factor-self.parameters.sell_factor)*(self.parameters.TP2/100)
        self.parameters.T2=self.parameters.spot -self.parameters.sell_factor-(self.parameters.v_factor-self.parameters.sell_factor)*(self.parameters.TP1/100)
        self.parameters.T1=self.parameters.spot -self.parameters.sell_factor-(self.parameters.v_factor-self.parameters.sell_factor)*(self.parameters.TP2/100)
        print(self.parameters.T3)
        print(self.parameters.T1)
        print(self.parameters.T2)
        print(self.parameters.T4)
        print(self.parameters.T5)
        self.parameters.save()
        print(self.parameters.T1)
    def token_calculations(self, nifty_price, v_factor, expiry):
       
        strike_prices = []

        spot = round(nifty_price/50, 0)*50
        self.parameters.spot=spot
        self.parameters.save()
        low_vix = spot-v_factor-100
        high_vix = spot+v_factor+100

        spot_value = low_vix

        while spot_value <= high_vix:
            strike_prices.append(spot_value)
            spot_value += 50

        df = pd.read_csv('datamanagement/scripts.csv')
        token_dict = {}
        dict_token = {}
        for i in range(len(df)):
            for j in range(len(strike_prices)):
                symbol = str(expiry)+str(int(strike_prices[j]))
                if symbol in df['symbol'][i]:
                    token_dict[str(df['symbol'][i])] = str(df['token'][i])
                    dict_token[str(df['token'][i])] = str(df['symbol'][i])

        return token_dict, dict_token

    def limit_order(self):
        pass

    def run(self):
        try:

            
            price_buy = obj.ltpData("NSE", 'NIFTY', "26000")['data']['ltp']
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            # print(v_factor,price_buy)

            
            v_factor = self.vix_calculation(price_buy)
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            print(v_factor,price_buy)
            
            if self.parameters.expiry_selected==1:
                expiry=self.parameters.expiry_2

            else:
                expiry=self.parameters.expiry_1

            print(expiry)
            
            token_dict, dict_token=self.token_calculations(price_buy, v_factor, expiry)

            
            self.market_order(price_buy, v_factor, expiry,token_dict, dict_token,self.parameters.LIMIT)


            

            self.websocket(token_dict, dict_token)

        except Exception:
            print(traceback.format_exc())
