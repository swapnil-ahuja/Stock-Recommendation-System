#Gets stock price data for the last 10 years of the given stocks through Quandl API and saves it as Stock_Prices.csv
import pandas as pd 
import os
from Quandl import Quandl
import time

auth_tok="sWvmc386JVsw1tBbwsWs"

# data= Quandl.get("WIKI/KO",trim_start="2000-12-12",trim_end="2001-01-02")

# print(data["Adj. Close"])

path="/home/swapnil/Desktop/intraQuarter"
def Stock_Prices():
	df=pd.DataFrame()
	statspath=path+"/_KeyStats"
	stock_list=[x[0] for x in os.walk(statspath)]
	stock_list.sort()
	for each_dir in stock_list[1:]:
		try:
			ticker= each_dir.split('/')[6]
			print(ticker)
			name="WIKI/"+ticker.upper()
			data=Quandl.get(name,trim_start="2000-12-12",trim_end="2014-12-30",authtoken=auth_tok)
			data[ticker.upper()]=data["Adj. Close"]
			df=pd.concat([df,data[ticker.upper()]],axis=1)
		except Exception as e:
			print(str(e))
			#time.sleep(10)

	df.to_csv("Stock_Prices.csv")


Stock_Prices()