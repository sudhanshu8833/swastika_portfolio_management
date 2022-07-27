import requests
import pandas as pd
import numpy as np
# url="https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"

# data=requests.get(url=url)
# data=data.json()

df=pd.read_csv('scripts.csv')

symbol=df['symbol'].to_numpy()
exchange=df['exch_seg'].to_numpy()

for i in range(1000):
    print(i)
    if 'NIFTY' in symbol[i][:4] and 'NFO' in exchange[i]:
        continue
    else:
        df.drop([i], axis=0, inplace=True)
print(df)

df.to_csv("scripts_this.csv")

