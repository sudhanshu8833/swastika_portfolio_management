from jugaad_data.nse import derivatives_csv, derivatives_df
df = derivatives_df(symbol="NIFTY", from_date=date(2020,1,1), to_date=date(2020,1,30),
            expiry_date=date(2022,1,30), instrument_type="OPTIDX",strike_price=16000,option_type='PE')
print(df.head())