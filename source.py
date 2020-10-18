from kiteconnect import KiteTicker, KiteConnect
import numpy as np 
import pandas as pd 
import talib
from datetime import datetime,timedelta


if __name__ == '__main__':
	api_key = 'dummy_api_key'
	api_secret = 'dummy_api_secret'

	kite = KiteConnect(api_key=api_key)

	data = kite.generate_session("dummy_access_token",api_secret = api_secret)
	kite.set_access_token(data['access_token'])
	
	#Date between which we want to fetch historical data

	from_date = datetime.strftime(datetime.now()-timedelta(100),'%Y-%m-%d')
	to_date = datetime.today().strftime('%Y-%m-%d')
	interval = '1minute'

	tokens = {738561:'RELIANCE',541249:'HDFCBANK'}

    log = []

	while True:
		#fetch historical data every 15 minute
		if (datetime.now().second == 0) and (datetime.now().minute % 15 == 0)
			for token in tokens:
				records = kite.historical_data(token,from_date = from_date,to_date = to_date,interval = interval)
				df = pd.DataFrame(records)
				df.drop(df.tail(1).index, inplace = True)

				Open = df['open'].values
				high = df['high'].values
				low  = df['low'].values
				close = df['close'].values
				volume = df['volume'].values

				sma5 = talib.SMA(close,5)
				sma15 = talib.SMA(close,15)

				price = kite.ltp('NSE:' + tokens[token])
				ltp = price['NSE:' + tokens[token]]['last price']

				if(sma5[-2]<sma15[-2]) and (sma5[-1]>sma15[-1]):
					buy_order_id = kite.place_order(variety = kite.VARIETY_REGULAR,
													exchange = kite.EXCHANGE_NSE,
													order_type=kite.ORDER_TYPE_MARKET,
													tradingsymbol = tokens[token],
													transaction_type = kite.TRANSACTION_TYPE_BUY,
													quantity = 1,
													validity = kite.VALIDITY_DAY,
													product = kite.PRODUCT_MIS,
													)

				if(sma5[-2]>sma15[-2]) and (sma5[-1]<sma15[-1]):
					sell_order_id = kite.place_order(variety = kite.VARIETY_REGULAR,
													exchange = kite.EXCHANGE_NSE,
													order_type=kite.ORDER_TYPE_MARKET,
													tradingsymbol = tokens[token],
													transaction_type = kite.TRANSACTION_TYPE_SELL,
													quantity = 1,
													validity = kite.VALIDITY_DAY,
													product = kite.PRODUCT_MIS,
													)
				
