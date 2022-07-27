# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%

import calendar
from datetime import date
from nsepython import *
from datetime import datetime
from datetime import timedelta
import pandas as pd
from time import strptime
import requests
import json
import pandas as pd
from .models import *

# def scripts():

#     url="https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
#     data=requests.get(url=url)
#     data=data.json()
#     df = pd.DataFrame(data)
#     df.to_csv("scripts.csv")


def this_scripts():

    url="https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
    data=requests.get(url=url)
    data=data.json()
    df = pd.DataFrame(data)

    # df=pd.read_csv('datamanagement/scripts.csv')

    df1=df[:1]
    # print(df1)


    for i in range(len(df)):
        print(i)

        if 'NIFTY' in df['symbol'][i][:6] and 'NFO' in df['exch_seg'][i]:
            df1.loc[len(df1.index)] = df.loc[i] 
        else:
            continue
    # print(df)

    df1.to_csv("datamanagement/scripts.csv")


def monthToNum(shortMonth):
    return {
        'jan': 1,
        'feb': 2,
        'mar': 3,
        'apr': 4,
        'may': 5,
        'jun': 6,
        'jul': 7,
        'aug': 8,
        'sep': 9,
        'oct': 10,
        'nov': 11,
        'dec': 12
    }[shortMonth]


def getting_holidays():
    Year = datetime.now().year
    A = calendar.TextCalendar(calendar.SUNDAY)
    B = calendar.TextCalendar(calendar.SATURDAY)

    holiday = pd.json_normalize(nse_holidays()['FO'])

    holidays = []

    for b in range(1, 13):
        for k in A.itermonthdays(Year, b):
            if k != 0:
                day = date(Year, b, k)
                if day.weekday() == 6:
                    # print("%d-%d-%d" % (k,b,Year))
                    holidays.append(str(k)+'-'+str(b)+'-'+str(Year)[-2:])

    for b in range(1, 13):
        for k in B.itermonthdays(Year, b):
            if k != 0:
                day = date(Year, b, k)
                if day.weekday() == 5:
                    # print("%d-%d-%d" % (k,b,Year))
                    holidays.append(str(k)+'-'+str(b)+'-'+str(Year)[-2:])

    holiday_list = list(holiday['tradingDate'])

    for i in range(len(holiday_list)):
        month = holiday_list[i][3:6]
        month = strptime(str(month), '%b').tm_mon
        holidays.append(holiday_list[i][:3]+str(month)+'-'+holiday_list[i][9:])

    return holidays


def expiry_dates():
    expiry_dates = []
    payload = nse_optionchain_scrapper('NIFTY')
    for i in range(1000):
        try:
            currentExpiry, dte = nse_expirydetails(payload, i)
            expiry_dates.append(str(currentExpiry)[2:])

        except:
            return expiry_dates


def convert_to_datetime(holidays, expiry):

    holiday_datetime = []
    expiry_datetime = []

    for i in range(len(holidays)):
        date_time_obj = datetime.strptime(holidays[i], '%d-%m-%y')

        holiday_datetime.append(date_time_obj)

    for i in range(len(expiry)):
        date_time_obj = datetime.strptime(expiry[i], '%y-%m-%d')

        expiry_datetime.append(date_time_obj)

    return holiday_datetime, expiry_datetime


def working_days(expiry_date, holidays):
    current = datetime.now()
    # print(expiry_date)
    difference = expiry_date-current+timedelta(days=1)
    # print(difference)
    for i in range(len(holidays)):
        if holidays[i] > current and holidays[i] < expiry_date:
            difference -= timedelta(days=1)

    return difference.days


def working_day_calculation(value):
    print("doing it brooo....")
    this_scripts()

    holidays = getting_holidays()
    expiry = expiry_dates()
    holiday_date, expiry_date = convert_to_datetime(holidays, expiry)
    days_1 = working_days(expiry_date[0], holiday_date)
    days_2 = working_days(expiry_date[1], holiday_date)

    expiry_nifty=expiry_list('NIFTY')


    expiry_1=option_symbol('NIFTY',expiry_nifty[0])
    expiry_2=option_symbol('NIFTY',expiry_nifty[1])
    # expiry_2=option_symbol('NIFTY',)


    user=User1.objects.get(username='testing')
    

    user.working_days_1=int(days_1)
    user.working_days_2=int(days_2)
    user.expiry_1=expiry_1
    user.expiry_2=expiry_2

    user.save()
    print("done it brooo....")
    return days_1,days_2


# %%
def option_symbol(symbol, expiry_date):

    return str(symbol)+str(expiry_date[:2])+str(expiry_date[3:6]).upper()+expiry_date[-2:]




