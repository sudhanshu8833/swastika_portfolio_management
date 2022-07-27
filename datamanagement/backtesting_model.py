# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from smartapi import SmartWebSocket
import math
import yfinance as yf
from finta import TA
import time
import pandas as pd
import json
import datetime
from dateutil import parser
from datetime import datetime
# %%
from smartapi import SmartConnect
obj = SmartConnect(api_key="uWbpZyYm")
data = obj.generateSession("S776051", "Madhya246###")
refreshToken = data['data']['refreshToken']
feedToken = obj.getfeedToken()
userProfile = obj.getProfile(refreshToken)
dictionary={}
current=0

def update_database():
    current=datetime.now().minute


def main(message):


    dictionary['time'] = time.time()

    for i in range(len(message)):
        if 'ltp' in message[i] and 'c' in message[i]:
            if 'ltt' in message[i]:
                times=parser.parse(message[i]['ltt'])

            else:
                times=datetime.fromtimestamp(dictionary['time'])
            dictionary[str(message[i]['tk'])][times] = str(message[i]['ltp'])


    if datetime.now().minute!=current:
        update_database()

    

FEED_TOKEN = feedToken
CLIENT_CODE = "S776051"
# token="mcx_fo|224395"
# SAMPLE: nse_cm|2885&nse_cm|1594&nse_cm|11536&nse_cm|3045
token = "nse_cm|2885&nse_cm|1594&nse_cm|11536&nse_cm|3045"
# token="mcx_fo|226745&mcx_fo|220822&mcx_fo|227182&mcx_fo|221599"
task = "mw"   # mw|sfi|dp

ss = SmartWebSocket(FEED_TOKEN, CLIENT_CODE)


def on_message(ws, message):
    print("Ticks: {}".format(message))

    # main(message)


def on_open(ws):
    print("on open")
    ss.subscribe(task, token)


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






# %%




# %%








# %%






# %%



# %%
with open("values.json") as json_data_file:
    data3 = json.load(json_data_file)

data3 = data3['WELCORP-EQ']
print(data3)


# %%
data = pd.Series(data3).to_frame('Close')


# %%
data.index.rename('Time', inplace=True)


# %%
data.index = pd.to_datetime(data.index, format='%Y-%m-%d %H:%M:%S:%f')


# %%
resample_LTP = pd.DataFrame()
data = data.dropna()
resample_LTP['low'] = data['Close'].resample('1Min').min()






# %%






# %%






# %%


# feed_token=092017047


# %%

dicts = {'e': 'nse_cm', 'ltp': '58.50', 'ltq': '36',
         'ltt': 'NA', 'name': 'sf', 'tk': '5606'}


# %%
[{'e': 'nse_cm', 'ltp': '58.50', 'ltq': '36', 'ltt': 'NA', 'name': 'sf', 'tk': '5606'},
 {'ap': '218.10', 'bp': '217.00', 'bq': '225', 'bs': '16', 'c': '217.15', 'cng': '-00.15',
 'e': 'nse_cm', 'lo': '216.50', 'ltp': '217.00', 'ltq': '25', 'ltt': '20/07/2022 10:23:43',
  'name': 'sf', 'nc': '-00.0691', 'sp': '217.20', 'tbq': '160392', 'tk': '11821', 'to': '46964999.70',
  'tsq': '468241', 'v': '215337'}, {'ap': '123.14', 'bp': '123.30', 'bq': '280', 'bs': '304', 'c': '121.00',
                                    'cng': '02.40', 'e': 'nse_cm', 'lo': '122.10', 'ltp': '123.40', 'ltq': '100', 'ltt': '20/07/2022 10:24:07',
                                    'name': 'sf', 'nc': '01.9835', 'sp': '123.40', 'tbq': '138822', 'tk': '15278',
                                    'to': '22991838.82', 'tsq': '187169', 'v': '186713'}]



