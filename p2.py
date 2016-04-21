#This a fully working script but here the stock prices are provided by parsing Yahoo Finanace pages which had a 
#lot of data which was N/A,therefore later we moved on a different source to get stock prices of the given stocks
#Next Version p5.py
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

	sp500_df=pd.DataFrame.from_csv("YAHOO-INDEX_GSPC.csv")#Containing data about sp500 for about 10 years (Quandl.com)

	
	ticker_list=[]
	#print(stock_list)
	#print(statspath)
	for each_dir in stock_list[1:]:
		each_file=os.listdir(each_dir)#Getting each file for each dir
		#print(each_file)
		#time.sleep(15)
		ticker= each_dir.split('/')[6]
		ticker_list.append(ticker)
		each_file.sort();
		starting_stock_value=False
		starting_sp500_value=False


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
 						sp500_date=datetime.fromtimestamp(unix_time-259200).strftime('%Y-%m-%d')#skipping by 3 days approx
 						row=sp500_df[(sp500_df.index==sp500_date)]
 						sp500_value=float(row["Adjusted Close"])

 					try:
 						#print('file=',file,'company=',ticker,'value=',value2)
 						stock_price1=source.split('</small><big><b>')
						stock_price2=float(stock_price1[1].split('</b></big>')[0])
					except Exception as e:
						#print(str(e))
						try:

							stock_price1=source.split('</small><big><b>')
							stock_price2=(stock_price1[1].split('</b></big>')[0])
							stock_price2=re.search(r'(\d{1,9}\.\d{1,9})',stock_price2)
							stock_price2=float(stock_price2.group(1))
							#print(stock_price2)
							#time.sleep(15)
						except Exception as e:
							#print(str(e),ticker,file)
							stock_price1=source.split('<span class="time_rtq_ticker">')
							stock_price2=(stock_price1[1].split('</span>')[0])
							stock_price2=re.search(r'(\d{1,9}\.\d{1,9})',stock_price2)
							stock_price2=float(stock_price2.group(1))
							#print(stock_price2)
							#time.sleep(5)


					if not starting_stock_value:
						starting_stock_value=stock_price2
					if not starting_sp500_value:
						starting_sp500_value=sp500_value
					
					stock_p_change=((stock_price2 - starting_stock_value)/starting_stock_value)*100
					sp500_p_change=((sp500_value - starting_sp500_value)/starting_sp500_value)*100
					diff=stock_p_change- sp500_p_change


					#Criteria for decdiding whether the stock underperformed/outperformed	
					if diff >0:
						status="outperform"	
					else:
						status="underperform"
					
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

 	# saving all the data in a .csv file
 	df.to_csv("Key_Stats.csv")#saving the file in csv format

Key_Stats()




