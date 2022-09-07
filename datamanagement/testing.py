# from .models import *
import yfinance as yf
import math
import pandas as pd
import time as tim
from smartapi import SmartConnect
from smartapi import SmartWebSocket
import traceback
import requests
import telepot

from datetime import time,datetime
from pytz import timezone 

# print(datetime.now(timezone("Asia/Kolkata")).time())

# if time(9,14)<=datetime.now(timezone("Asia/Kolkata")).time():
#     print("ji")

# else:
#     print("lets see")

# FEED_TOKEN=feedToken
# CLIENT_CODE="S776051"
# # token="mcx_fo|224395"
# token="nse_cm|2885&nse_cm|1594&nse_cm|11536&nse_cm|3045"    #SAMPLE: nse_cm|2885&nse_cm|1594&nse_cm|11536&nse_cm|3045
# # token="mcx_fo|226745&mcx_fo|220822&mcx_fo|227182&mcx_fo|221599"

# task="mw"   # mw|sfi|dp

# ss = SmartWebSocket(FEED_TOKEN, CLIENT_CODE)

# # bot.sendMessage(1039725953,"websocket connection is being stablished")
# times=time.time()
# def on_message(ws, message):



#     print(message)
#     if time.time()>times+5:
#         ws.on_close(ws)
#         # self.ltp_nifty_options(message,token_dict,dict_token)
#         # self.main(token_dict, dict_token,ws)


# def on_open(ws):
#     print("on open")
#     ss.subscribe(task,token)
    
# def on_error(ws, error):
#     print(error)
    
# def on_close(ws):
#     print("#################")
#     return False

# # Assign the callbacks.
# ss._on_open = on_open
# ss._on_message = on_message
# ss._on_error = on_error
# ss._on_close = on_close

# ss.connect()

