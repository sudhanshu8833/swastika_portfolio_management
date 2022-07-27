
import yfinance as yf


def my_scheduled_job():
    df=yf.download("MSFT",period='1mo',interval='5m')
    df.to_csv("testing.csv")
    print("Hello its working, my friend")

