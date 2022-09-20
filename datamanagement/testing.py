from AesEverywhere import aes256
import json
from aiohttp import payload
import requests
from smartapi import SmartConnect
from smartapi import SmartWebSocket

# url="https://stagingtradingoapi.swastika.co.in/token"

# body={
#     "grant_type": "password",

# "username": "lakshyaguptaApp",

# "password": "lakshyaguptaApp@01734",

# "version": "1"
# }

obj = SmartConnect(api_key='NuTmF22y')
data = obj.generateSession("Y99521", "abcd@1234")
refreshToken = data['data']['refreshToken']
feedToken = obj.getfeedToken()
print(refreshToken)
headers = {'content-type': 'application/x-www-form-urlencoded'}




# for getting accesstoken
# resonse=requests.post(url,data=body)
# print(resonse.json())



# for creating a session
url="https://stagingtradingoapi.swastika.co.in/api/User/LoginTwoFA"

body={
    "uid":"TDEMO2"
}


body=json.dumps(body)

headers={
    "Authorization":"Bearer orCLa-fYnm7jYpTzYARKZVt9CXZQfOYMUcm5lXaMTxgPVI-piJtgbY91f-fFYFzeLLk5RvcSOnhJ6nkx48TOdL0r0ClkzqBSrUUfdcRxmTXsHwk3Q2Bz3KiGMqFPoZMKdOG2VvHgix1GDZjd8gooK48oWa6EJlCqfK5zW2D8Drl_z9VxdTLqRyxUpeLL1OSW0dGP1gyuXF1f-QG3fFBLmCoY15hz9IulErxIKNUygj8",
    "AppId":"lakshyaguptaApp",
    "version":"1"
}



encrypted = aes256.encrypt(body, 'lakshyagupta@01734')

decrypt=requests.post(url,data=encrypted,headers=headers)
# print(decrypt.json())
print(aes256.decrypt(decrypt.json()['Data'], 'lakshyagupta@01734'))


# /api/PlaceOrder/PlaceOrder

url="https://stagingtradingoapi.swastika.co.in/api/PlaceOrder/PlaceOrder"

body={
    "uid":"TDEMO2",
    "actid":"TDEMO1",
    "Tsym":"MSFT",
    "exch":"NSE",
    "Ttranstype":"B",
    "Ret":""
}