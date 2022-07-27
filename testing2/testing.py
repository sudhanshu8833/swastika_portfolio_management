
from finta import TA
from smartapi import SmartConnect
import numpy as np
import pandas as pd

obj = SmartConnect(api_key="uWbpZyYm")
data = obj.generateSession("S776051", "Madhya246###")
refreshToken = data['data']['refreshToken']
feedToken = obj.getfeedToken()
userProfile = obj.getProfile(refreshToken)
print(userProfile)

df=pd.read_csv("parameters.csv")
df=df.set_index("parameters")

TSL_factor = int(df['Data'][0])
ATR_period = int(df['Data'][1])
amount_invest = int(df['Data'][2])
stock = df['Data'][3]
stock_token = df['Data'][4]
time_frame = df['Data'][5]
position = ""


def candles(token, interval):

    ohlc_intraday = pd.DataFrame()

    historicParam = {
        "exchange": "NSE",
        "symboltoken": str(token),
        "interval": interval,
        "fromdate": "2022-07-05 09:15",
        "todate": "2022-12-14 15:25"
    }

    data = obj.getCandleData(historicParam)
    # print(data)
    data = pd.DataFrame(data)["data"]
    open = []
    close = []
    high = []
    low = []
    volume = []
    index = []
    for i in range(len(data)):
        open.append(data[i][1])

    for i in range(len(data)):
        close.append(data[i][4])

    for i in range(len(data)):
        high.append(data[i][2])

    for i in range(len(data)):
        low.append(data[i][3])

    for i in range(len(data)):
        index.append(data[i][0])

    for i in range(len(data)):
        volume.append(data[i][5])

    ohlc_intraday["Datetime"] = np.array(index)
    ohlc_intraday["Open"] = np.array(open)
    ohlc_intraday["High"] = np.array(high)
    ohlc_intraday["Low"] = np.array(low)
    ohlc_intraday["Close"] = np.array(close)
    ohlc_intraday["volume"] = np.array(volume)
    ohlc_intraday.set_index("Datetime", inplace=True)

    ohlc_intraday['ATR'] = TA.ATR(ohlc_intraday, ATR_period)
    # print(ohlc_intraday)

    return ohlc_intraday[:-1]

# BUY - rsi cross below (from csv)
# This is the function which runs every time

# EXCLUSIVE FOR ANGEL


def ltp_price(instrument, symbol_token):

    ltp_price = obj.ltpData("NSE", str(instrument)+'-EQ',
                            str(symbol_token))['data']['ltp']

    return ltp_price


def trade_signal(df2, ltp):
    global position, price_sell, stop_loss, stoploss, price_buy
    signal = ""

    if position == "":

        # BUY CONDITION
        # GREEN CANDLE AND (UPPER WICK <BODY OR UPPER WICK> 30% OF BODY)
        if df2['Close'][-1] > df2['Open'][-1] and (abs(df2['High'][-1]-df2['Close'][-1]) < abs(df2['Open'][-1]-df2['Close'][-1]) or abs(df2['High'][-1]-df2['Close'][-1]) > .3 * abs(df2['High'][-1]-df2['Low'][-1])):
            signal = "BUY"
            position = 'LONG'

        # SELL CONDITION
        # RED CANDLE AND (LOWER WICK <BODY OR LOWER WICK> 30% OF BODY)
        elif df2['Close'][-1] < df2['Open'][-1] and (abs(df2['Low'][-1]-df2['Close'][-1]) < abs(df2['Open'][-1]-df2['Close'][-1]) or abs(df2['Low'][-1]-df2['Close'][-1]) > .3*abs(df2['High'][-1]-df2['Low'][-1])):
            signal = "SELL"
            position = 'SHORT'

    elif position == 'LONG':
        if price_buy < ltp:
            stoploss = (ltp-price_buy)*TSL_factor+stoploss
            price_buy = ltp

        if stoploss > ltp:
            signal = "EXIT-BUY"
            position = ""

    elif position == 'SHORT':
        if price_sell > ltp:
            stop_loss = (ltp - price_sell)*TSL_factor+stop_loss
            price_sell = ltp

        if stop_loss < ltp:
            signal = 'EXIT-SELL'
            position = ""

    return signal


def market_order(symbol, symboltoken, tt, quantity):

    try:
        orderparams = {
            "variety": "NORMAL",
            "tradingsymbol": str(symbol),
            "symboltoken": str(symboltoken),
            "transactiontype": str(tt),
            "exchange": "NSE",
            "ordertype": "MARKET",
            "producttype": "INTRADAY",
            "duration": "DAY",
            "quantity": str(quantity)
        }

        orderId = obj.placeOrder(orderparams)
    except Exception as e:
        print(str(e))


def main():
    global stoploss, price_buy, price_sell, stop_loss, quantity

    ltp = ltp_price(stock, stock_token)
    df = candles(stock_token, time_frame)

    print(ltp)

    signal = trade_signal(df, ltp)

    if signal == "BUY":
        stoploss = ltp-df['ATR'][-1]
        price_buy = ltp

        quantity = int(amount_invest/ltp)
        market_order(stock, stock_token, "BUY", quantity)

    elif signal == "SELL":
        stop_loss = ltp+df['ATR'][-1]
        price_sell = ltp
        quantity = int(amount_invest/ltp)
        market_order(stock, stock_token, "SELL", quantity)

    elif signal == "EXIT-BUY":
        market_order(stock, stock_token, "SELL", quantity)

    elif signal == "EXIT-SELL":
        market_order(stock, stock_token, "BUY", quantity)


while True:
    main()
