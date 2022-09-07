import json
from datetime import datetime
import random
from sympy import div
from .models import *
import yfinance as yf
import math
import pandas as pd
import time as tim
from smartapi import SmartConnect
from smartapi import SmartWebSocket
import traceback
from pytz import timezone
from datetime import time, datetime
# import telepot
# bot = telepot.Bot("5448843199:AAEKjMn2zwAyZ5tu8hsLIgsakxoLf980BoY")
# bot.getMe()
import logging
logger = logging.getLogger('dev_log')


class run_strategy():

    def __init__(self, strategy):
        self.parameters = strategy
        self.ltp_prices = {}
        self.times = tim.time()
        self.day = datetime.now(timezone("Asia/Kolkata")).day
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

    def ltp_nifty_options(self, token_dict, dict_token):

        position_opened = positions.objects.filter(
            strategy_id=str(self.parameters.strategy_id), status='OPEN')

        with open('datamanagement/data.json') as data_file:
            data = json.load(data_file)
        self.ltp_prices['26000'] = data['26000']

        position_opened = positions.objects.filter(
            strategy_id=str(self.parameters.strategy_id), status='OPEN')
        print(position_opened.all())
        for i in range(len(position_opened)):
            try:
                with open('datamanagement/data.json') as data_file:
                    data = json.load(data_file)
                self.ltp_prices[position_opened[i].token] = data[str(
                    position_opened[i].token)]
                position_opened[i].current_price = float(
                    self.ltp_prices[position_opened[i].token])
                position_opened[i].save()

            except Exception:
                print(traceback.format_exc())

    def shift_position(self, nifty_price, token_dict, dict_token):

        position_opened = positions.objects.filter(strategy_id=str(
            self.parameters.strategy_id), status='OPEN', side='SHORT')
        print(position_opened.all())
        for i in range(len(position_opened)):
            position_opened[i].status = "CLOSED"
            position_opened[i].time_out = datetime.now()
            position_opened[i].price_out = float(
                self.ltp_prices[position_opened[i].token])
            position_opened[i].save()

            p = self.add_orders(position_opened[i].symbol, "BUY", float(
                self.ltp_prices[position_opened[i].token]), False, token_dict, dict_token)

        strike_price = round(nifty_price/50, 0)*50

        if self.parameters.expiry_selected == 0:
            expiry = self.parameters.expiry_1

        if self.parameters.expiry_selected == 1:
            expiry = self.parameters.expiry_2

        symbol_pe = expiry + \
            str(int(strike_price+self.parameters.sell_factor))+'PE'
        symbol_ce = expiry + \
            str(int(strike_price+self.parameters.sell_factor))+'CE'

        symbol_pe_price=self.obj.ltpData("NFO",symbol_pe ,token_dict[symbol_pe])['data']['ltp']
        symbol_ce_price=self.obj.ltpData("NFO",symbol_ce ,token_dict[symbol_ce])['data']['ltp']

        p = self.add_positions(symbol_pe, 'SHORT', symbol_pe_price, 0, 0, token_dict, dict_token)
        p = self.add_positions(symbol_ce, 'SHORT', symbol_ce_price, 0, 0, token_dict, dict_token)
        # p = self.add_orders(symbol_pe, "SELL", float(
        #     self.ltp_prices[token_dict[symbol_pe]]), True, token_dict, dict_token)
        # p = self.add_orders(symbol_ce, "SELL", float(
        #     self.ltp_prices[token_dict[symbol_ce]]), True, token_dict, dict_token)

    def close_all_positions(self, token_dict, dict_token):

        position_opened = positions.objects.filter(
            strategy_id=str(self.parameters.strategy_id), status='OPEN')

        for i in range(len(position_opened)):
            position_opened[i].status = "CLOSED"
            position_opened[i].time_out = datetime.now()
            position_opened[i].price_out = float(
                self.ltp_prices[position_opened[i].token])
            position_opened[i].save()

            if position_opened[i].side == "SHORT":
                p = self.add_orders(position_opened[i].symbol, "BUY", float(
                    self.ltp_prices[position_opened[i].token]), False, token_dict, dict_token)

            if position_opened[i].side == "LONG":
                p = self.add_orders(position_opened[i].symbol, "SELL", float(
                    self.ltp_prices[position_opened[i].token]), False, token_dict, dict_token)

        self.parameters.status = "CLOSED"
        self.parameters.save()
        return None

    def main(self, token_dict, dict_token):

        position_opened = positions.objects.filter(strategy_id=str(
            self.parameters.strategy_id), status='OPEN', side='SHORT')

        if (float(self.ltp_prices['26000']) > self.parameters.T4 and self.parameters.T_now == 3):
            # bot.sendMessage(1039725953,"position shifting")
            self.shift_position(
                float(self.ltp_prices['26000']), token_dict, dict_token)
            self.parameters.T_now = 4
            self.parameters.save()

        if (float(self.ltp_prices['26000']) > self.parameters.T5 and self.parameters.T_now == 4):
            # bot.sendMessage(1039725953,"closing position")
            self.close_all_positions(token_dict, dict_token)
            return "complete"

        if float(self.ltp_prices['26000']) < self.parameters.T3 and self.parameters.T_now == 4:
            # bot.sendMessage(1039725953,"position shifting")
            self.shift_position(
                float(self.ltp_prices['26000']), token_dict, dict_token)
            self.parameters.T_now = 3
            self.parameters.save()

        if float(self.ltp_prices['26000']) < self.parameters.T2 and self.parameters.T_now == 3:
            # bot.sendMessage(1039725953,"position shifting")
            self.shift_position(
                float(self.ltp_prices['26000']), token_dict, dict_token)
            self.parameters.T_now = 2
            self.parameters.save()

        if float(self.ltp_prices['26000']) < self.parameters.T1 and self.parameters.T_now == 2:
            # bot.sendMessage(1039725953,"closing position")
            self.close_all_positions(token_dict, dict_token)
            return "complete"

        if float(self.ltp_prices['26000']) > self.parameters.T3 and self.parameters.T_now == 2:
            # bot.sendMessage(1039725953,"position shifting")
            self.shift_position(
                float(self.ltp_prices['26000']), token_dict, dict_token)
            self.parameters.T_now = 3
            self.parameters.save()

        for i in range(len(position_opened)):

            if float(self.ltp_prices[position_opened[i].token]) < self.parameters.ET:
                # bot.sendMessage(1039725953,"closing position")
                self.close_all_positions(token_dict, dict_token)
                return "complete"

    def calculate_websocket_token(self, token_dict, dict_token):
        token = ""
        lists = []
        for key, value in token_dict.items():
            lists.append(value)

        token = ""
        for i in range(len(lists)):
            token = token+"nse_fo|"+str(lists[i])

            if i == len(lists)-1:
                token = token
            else:
                token = token+'&'

        return token

    def websocket(self, token_dict, dict_token):

        while True:
            try:
                # if datetime.now(timezone("Asia/Kolkata")).day != self.day and datetime.now(timezone("Asia/Kolkata")).time() >= time(8, 30):
                #     self.day = datetime.now(timezone("Asia/Kolkata")).day
                #     for i in range(100):
                #         x = random.randint(0, 30)
                #         tim.sleep(x)
                #         # LOGIN HERE
                #         break

                if time(8, 1) <= datetime.now(timezone("Asia/Kolkata")).time() and time(15, 50) >= datetime.now(timezone("Asia/Kolkata")).time():
                    tim.sleep(1)
                    try:

                        self.ltp_nifty_options(token_dict, dict_token)
                        data = self.main(token_dict, dict_token)
                        if data == "complete":
                            return None

                    except Exception:
                        print(traceback.format_exc())
                        logger.info(str(traceback.format_exc()))

                else:
                    tim.sleep(600*6)

                    logger.info(
                        f"logging {datetime.now(timezone('Asia/Kolkata'))}")

            except Exception:
                print(traceback.format_exc())
                logger.info(str(traceback.format_exc()))

    def vix_calculation(self, price):

        print(self.parameters.working_days_1)
        working_days_1 = self.parameters.working_days_1
        working_days_2 = self.parameters.working_days_2

        if working_days_1 != 0:

            vix_price = float(yf.download(
                "^INDIAVIX", period='1D', interval="1D")['Close'][-1])

            days_vix = vix_price / (math.sqrt(252/working_days_1))

            nifty_range = price*days_vix*(1-vix_price/100)/100
            v_factor = round(nifty_range/50, 0)*50

        else:
            v_factor = 0
        if v_factor < self.parameters.buy_factor:

            vix_price = float(yf.download(
                "^INDIAVIX", period='1D', interval="1D")['Close'][-1])

            days_vix = vix_price / (math.sqrt(252/working_days_2))

            nifty_range = price*days_vix*(1-vix_price/100)/100
            v_factor = round(nifty_range/50, 0)*50

            expiry = self.parameters.expiry_2
            self.parameters.expiry_selected = 1
            self.parameters.save()

        else:
            expiry = self.parameters.expiry_1
            self.parameters.expiry_selected = 0
            self.parameters.save()

        self.parameters.v_factor = v_factor
        self.parameters.save()

        return v_factor

    def add_orders(self, symbol, side, price, open_position, token_dict, dict_token):
        strategy1 = orders(

            strategy_id=self.parameters.strategy_id,
            symbol=symbol,
            time=datetime.now(timezone("Asia/Kolkata")),
            price=price,
            transaction_type=side,
            open_position=open_position,
            order_id=0
        )
        strategy1.save()

    def add_positions(self, symbol, side, price_in, time_out, price_out, token_dict, dict_token):

        strategy1 = positions(

            strategy_id=self.parameters.strategy_id,
            symbol=symbol,
            time_in=datetime.now(timezone("Asia/Kolkata")),
            side=str(side),
            price_in=float(price_in),
            time_out=datetime.now(timezone("Asia/Kolkata")),
            price_out=float(price_out),
            status="OPEN",
            token=str(token_dict[symbol])
        )
        strategy1.save()

    def market_order(self, nifty_price, v_factor, expiry, token_dict, dict_token, limit):
        nifty_price = round(nifty_price/50, 0)*50

        symbol_buy_put = expiry+str(int(nifty_price+v_factor))+'PE'
        symbol_buy_call = expiry+str(int(nifty_price-v_factor))+'CE'

        symbol_sell_put = expiry + \
            str(int(nifty_price+self.parameters.sell_factor))+'PE'
        symbol_sell_call = expiry + \
            str(int(nifty_price-self.parameters.sell_factor))+'CE'

        with open('datamanagement/data.json') as data_file:
            data = json.load(data_file)

        # symbol_buy_put_price = data[token_dict[symbol_buy_put]]
        # symbol_buy_call_price = data[token_dict[symbol_buy_call]]
        # symbol_sell_put_price = data[token_dict[symbol_sell_put]]
        # symbol_sell_call_price = data[token_dict[symbol_sell_call]]
        symbol_buy_put_price =self.obj.ltpData("NFO",symbol_buy_put ,token_dict[symbol_buy_put])['data']['ltp']
        symbol_buy_call_price = self.obj.ltpData("NFO",symbol_buy_call,token_dict[symbol_buy_call])['data']['ltp']
        symbol_sell_put_price = self.obj.ltpData("NFO",symbol_sell_put,token_dict[symbol_sell_put])['data']['ltp']
        symbol_sell_call_price = self.obj.ltpData("NFO",symbol_sell_call,token_dict[symbol_sell_call])['data']['ltp']


        if limit.lower() == "on":
            print("got into limit")
            while True:
                with open('datamanagement/data.json') as data_file:
                    data = json.load(data_file)
                time_start = tim.time()

                price_put = data[token_dict[symbol_buy_put]]
                price_call = data[token_dict[symbol_buy_call]]

                print("^^^^^^^^^^^^")
                print(price_put)
                print(price_call)
                print(self.parameters.time_out)
                print("^^^^^^^^^^^^")

                kem = 0
                while tim.time() <= time_start+self.parameters.time_out:
                    with open('datamanagement/data.json') as data_file:
                        data = json.load(data_file)

                    price_put_now = data[token_dict[symbol_buy_put]]
                    price_call_now = data[token_dict[symbol_buy_call]]

                    print("^^^^^^^^^^^^")
                    print(price_put_now, price_put)
                    print(price_call_now, price_call)
                    print("^^^^^^^^^^^^")
                    if price_put_now < price_put or price_call_now < price_call:
                        kem = 1
                        break

                if kem == 1:
                    break

        if limit.lower() == "on":

            with open('datamanagement/data.json') as data_file:
                data = json.load(data_file)

            symbol_buy_put_price = data[token_dict[symbol_buy_put]]
            symbol_buy_call_price = data[token_dict[symbol_buy_call]]
            symbol_sell_put_price = data[token_dict[symbol_sell_put]]
            symbol_sell_call_price = data[token_dict[symbol_sell_call]]

        if self.parameters.status != "TEST":
            p = self.add_positions(
                symbol_buy_put, "LONG", symbol_buy_put_price, 0, 0, token_dict, dict_token)
            p = self.add_positions(
                symbol_buy_call, "LONG", symbol_buy_call_price, 0, 0, token_dict, dict_token)
            p = self.add_positions(
                symbol_sell_put, "SHORT", symbol_sell_put_price, 0, 0, token_dict, dict_token)
            p = self.add_positions(
                symbol_sell_call, "SHORT", symbol_sell_call_price, 0, 0, token_dict, dict_token)

        p = self.add_orders(symbol_buy_put, "BUY",
                            symbol_buy_put_price, True, token_dict, dict_token)
        p = self.add_orders(symbol_buy_call, "BUY",
                            symbol_buy_call_price, True, token_dict, dict_token)
        p = self.add_orders(symbol_sell_put, "SELL",
                            symbol_sell_put_price, True, token_dict, dict_token)
        p = self.add_orders(symbol_sell_call, "SELL",
                            symbol_sell_call_price, True, token_dict, dict_token)

        if self.parameters.status == "TEST":
            data = orders.objects.filter(
                strategy_id=self.parameters.strategy_id)
            # data.delete()
            self.parameters.delete()
            return data

        print(self.parameters.T1)
        self.parameters.T3 = nifty_price
        self.parameters.T4 = self.parameters.spot + self.parameters.sell_factor + \
            (self.parameters.v_factor-self.parameters.sell_factor) * \
            (self.parameters.TP1/100)
        self.parameters.T5 = self.parameters.spot + self.parameters.sell_factor + \
            (self.parameters.v_factor-self.parameters.sell_factor) * \
            (self.parameters.TP2/100)
        self.parameters.T2 = self.parameters.spot - self.parameters.sell_factor - \
            (self.parameters.v_factor-self.parameters.sell_factor) * \
            (self.parameters.TP1/100)
        self.parameters.T1 = self.parameters.spot - self.parameters.sell_factor - \
            (self.parameters.v_factor-self.parameters.sell_factor) * \
            (self.parameters.TP2/100)
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
        self.parameters.spot = spot
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

    def run(self):
        try:
            with open('datamanagement/data.json') as data_file:
                data = json.load(data_file)

            price_buy = data['26000']

            # print(v_factor,price_buy)
            print(price_buy)

            v_factor = self.vix_calculation(price_buy)

            print(v_factor, price_buy)

            if self.parameters.expiry_selected == 1:
                expiry = self.parameters.expiry_2

            else:
                expiry = self.parameters.expiry_1

            print(expiry)

            token_dict, dict_token = self.token_calculations(
                price_buy, v_factor, expiry)

            data = self.market_order(
                price_buy, v_factor, expiry, token_dict, dict_token, self.parameters.LIMIT)
            if data != None:

                return data
            value = self.websocket(token_dict, dict_token)
            return value
        except Exception:
            print(traceback.format_exc())
