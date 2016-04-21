#It's different from the previous two versions as it obtains data from more reliable resources and is far
#more practical in it's approach.
import pandas as pd
import os
import time
from datetime import datetime
from time import mktime
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
import re
style.use("dark_background")
#path where the yahoo finance html files are present
path="/home/swapnil/Desktop/intraQuarter"

# gather gives the features we would like to parse
def Key_Stats(gather=["Total Debt/Equity",
                      'Trailing P/E',
                      'Price/Sales',
                      'Price/Book',
                      'Profit Margin',
                      'Operating Margin',
                      'Return on Assets',
                      'Return on Equity',
                      'Revenue Per Share',
                      'Market Cap',
                        'Enterprise Value',
                        'Forward P/E',
                        'PEG Ratio',
                        'Enterprise Value/Revenue',
                        'Enterprise Value/EBITDA',
                        'Revenue',
                        'Gross Profit',
                        'EBITDA',
                        'Net Income Avl to Common ',
                        'Diluted EPS',
                        'Earnings Growth',
                        'Revenue Growth',
                        'Total Cash',
                        'Total Cash Per Share',
                        'Total Debt',
                        'Current Ratio',
                        'Book Value Per Share',
                        'Cash Flow',
                        'Beta',
                        'Held by Insiders',
                        'Held by Institutions',
                        'Shares Short (as of',
                        'Short Ratio',
                        'Short % of Float',
                        'Shares Short (prior ']):
	statspath = path+'/_KeyStats'
	stock_list=[x[0] for x in os.walk(statspath)]#Getting all the directories
	stock_list.sort();

    #defing the structure of the DataFrame
	df = pd.DataFrame(columns = ['Date',
                                 'Unix',
                                 'Ticker',
                                 'Price',
                                 'stock_p_change',
                                 'SP500',
                                 'sp500_p_change',
                                 'Difference',
                                 ##############
                                 'DE Ratio',
                                 'Trailing P/E',
                                 'Price/Sales',
                                 'Price/Book',
                                 'Profit Margin',
                                 'Operating Margin',
                                 'Return on Assets',
                                 'Return on Equity',
                                 'Revenue Per Share',
                                 'Market Cap',
                                 'Enterprise Value',
                                 'Forward P/E',
                                 'PEG Ratio',
                                 'Enterprise Value/Revenue',
                                 'Enterprise Value/EBITDA',
                                 'Revenue',
                                 'Gross Profit',
                                 'EBITDA',
                                 'Net Income Avl to Common ',
                                 'Diluted EPS',
                                 'Earnings Growth',
                                 'Revenue Growth',
                                 'Total Cash',
                                 'Total Cash Per Share',
                                 'Total Debt',
                                 'Current Ratio',
                                 'Book Value Per Share',
                                 'Cash Flow',
                                 'Beta',
                                 'Held by Insiders',
                                 'Held by Institutions',
                                 'Shares Short (as of',
                                 'Short Ratio',
                                 'Short % of Float',
                                 'Shares Short (prior ',                                
                                 ##############
                                 'Status'])

	#Containing data about sp500 for about 10 years (Quandl.com)
	sp500_df=pd.DataFrame.from_csv("YAHOO-INDEX_GSPC.csv")
	
    #stock prices from Qaundl.com 
	stock_df=pd.DataFrame.from_csv("Stock_Prices.csv")
	
	ticker_list=[]
	#print(stock_list)
	#print(statspath)
	counter_sleep=0
	for each_dir in stock_list[1:]:
		each_file=os.listdir(each_dir)#Getting each file for each dir
		#print(each_file)
		#time.sleep(15)
		ticker= each_dir.split('/')[6]
		ticker_list.append(ticker)
		each_file.sort();
		# starting_stock_value=False
		# starting_sp500_value=False
        #This was done as my PC gets heated after processing too many files
        #Therefore the processors rests for some time then countinue execution

		counter_sleep=counter_sleep+1
		if(counter_sleep>300):
			print("pause to rest")
			counter_sleep=0
			time.sleep(20)


		if len(each_file)>0:
			for file in each_file:
				date_stamp= datetime.strptime(file,'%Y%m%d%H%M%S.html')#Getting time for each file
				unix_time=time.mktime(date_stamp.timetuple())#converting it to unix time
				#print(date_stamp,unix_time)
 				#time.sleep(15)
 				#print(file)
 				full_file_path=each_dir+'/'+file
 				#print(full_file_path)
 				source=open(full_file_path,'r').read()#reading each html file
 				#print(source)
 				#time.sleep(15)
 				
 				#time.sleep(1)
 				try:
 					
 					value_list=[]
 					for each_data in gather:
						try:
                            #Using regular expressions to parse all the details we wanted 
							regex=re.escape(each_data)+r'.*?(\d{1,8}\.\d{1,8}M?B?|N/A)%?</td>'
							value = re.search(regex,source)
							value=(value.group(1))
                            # B-Billions M-Millions
							if "B" in value:
								value=float(value.replace("B",''))*1000000000
							elif "M" in value:
								value=float(value.replace("M",''))*1000000

							value_list.append(value)

	 						
	 					except Exception as e:
	 						value="N/A"
	 						value_list.append(value)
	 				#print(value_list)
	 				#time.sleep(15)	
	 						
 					try:
 						sp500_date=datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')
 						row=sp500_df[(sp500_df.index==sp500_date)]
 						sp500_value=float(row["Adjusted Close"])
 					except:
 						sp500_date=datetime.fromtimestamp(unix_time-259200).strftime('%Y-%m-%d')#skipped 3 days
 						row=sp500_df[(sp500_df.index==sp500_date)]
 						sp500_value=float(row["Adjusted Close"])

 					one_year_later=int(unix_time+31536000)

 					try:
 						sp500_1y=datetime.fromtimestamp(one_year_later).strftime('%Y-%m-%d')
 						row=sp500_df[(sp500_df.index==sp500_1y)]
 						sp500_1y_value=float(row["Adjusted Close"])

 					except Exception as e:


 						try:
 							sp500_1y=datetime.fromtimestamp(one_year_later-259200).strftime('%Y-%m-%d')
 							row=sp500_df[(sp500_df.index==sp500_1y)]
 							sp500_1y_value=float(row["Adjusted Close"])

 						except Exception as e:
 							print("S&P 500 exception:",str(e))

 					#print("sp500-1y:",sp500_1y_value)



 					try:
 						stock_price_1y=datetime.fromtimestamp(one_year_later).strftime('%Y-%m-%d')
 						row=stock_df[(stock_df.index==stock_price_1y)][ticker.upper()]
 						stock_1y_value=round(float(row),2)

 					except Exception as e:


 						try:
 							stock_price_1y=datetime.fromtimestamp(one_year_later-259200).strftime('%Y-%m-%d')
	 						row=stock_df[(stock_df.index==stock_price_1y)][ticker.upper()]
	 						stock_1y_value=round(float(row),2)


 						except Exception as e:
 							print("Stock_Price 1 yr later:",str(e))

 					#print("stock_price 1yr later $:",stock_1y_value)


 					try:
 						stock_price=datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')
 						row=stock_df[(stock_df.index==stock_price)][ticker.upper()]
 						stock_price2=round(float(row),2)

 					except Exception as e:


 						try:
 							stock_price=datetime.fromtimestamp(unix_time-259200).strftime('%Y-%m-%d')
 							row=stock_df[(stock_df.index==stock_price)][ticker.upper()]
 							stock_price2=round(float(row),2)


 						except Exception as e:
 							print("Stock_Price:",str(e))

 					#print("stock price present:",stock_price2)
 					#time.sleep(10)













 					#print("i am here")
 					#time.sleep(5)
					stock_p_change=((stock_1y_value - stock_price2)/stock_price2)*100
					sp500_p_change=((sp500_1y_value - sp500_value)/sp500_value)*100
					stock_p_change=round(stock_p_change,2)
					sp500_p_change=round(sp500_p_change,2)
					diff=stock_p_change- sp500_p_change
					diff=round(diff,2)
					#print("sp500_p_change:",sp500_p_change)
					#time.sleep(10)

                    #Criteria for decdiding whether the stock underperformed/outperformed
					if diff >10:
						status=1	
					else:
						status=0


                    #Here we could define the max no of N/A values a row of data can contain (Currently NO N/A)

					if value_list.count("N/A")>0:
						pass
					else:
						df=df.append({'Date':date_stamp,'Unix':unix_time,'Ticker':ticker,'Price':stock_price2,'SP500':sp500_value,'stock_p_change':stock_p_change,'sp500_p_change':sp500_p_change,'Difference':diff,'DE Ratio':value_list[0],
                                            #'Market Cap':value_list[1],
                                            'Trailing P/E':value_list[1],
                                            'Price/Sales':value_list[2],
                                            'Price/Book':value_list[3],
                                            'Profit Margin':value_list[4],
                                            'Operating Margin':value_list[5],
                                            'Return on Assets':value_list[6],
                                            'Return on Equity':value_list[7],
                                            'Revenue Per Share':value_list[8],
                                            'Market Cap':value_list[9],
                                             'Enterprise Value':value_list[10],
                                             'Forward P/E':value_list[11],
                                             'PEG Ratio':value_list[12],
                                             'Enterprise Value/Revenue':value_list[13],
                                             'Enterprise Value/EBITDA':value_list[14],
                                             'Revenue':value_list[15],
                                             'Gross Profit':value_list[16],
                                             'EBITDA':value_list[17],
                                             'Net Income Avl to Common ':value_list[18],
                                             'Diluted EPS':value_list[19],
                                             'Earnings Growth':value_list[20],
                                             'Revenue Growth':value_list[21],
                                             'Total Cash':value_list[22],
                                             'Total Cash Per Share':value_list[23],
                                             'Total Debt':value_list[24],
                                             'Current Ratio':value_list[25],
                                             'Book Value Per Share':value_list[26],
                                             'Cash Flow':value_list[27],
                                             'Beta':value_list[28],
                                             'Held by Insiders':value_list[29],
                                             'Held by Institutions':value_list[30],
                                             'Shares Short (as of':value_list[31],
                                             'Short Ratio':value_list[32],
                                             'Short % of Float':value_list[33],
                                             'Shares Short (prior ':value_list[34],'Status':status,},ignore_index= True)



 				except Exception as e:
 					pass

 	# finally saveing the file in csv format
 	df.to_csv("Key_Stats_acc_perf_NO_NA(Enhanced).csv")#saving the file in csv format

Key_Stats()




