#This script was intially used to parse data but later we wanted to parse more features,
#therefore we we created modified version of this script(p2.py)

#---------------------------------------------------------------------------

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
def Key_Stats(gather="Total Debt/Equity (mrq):"):
	statspath = path+'/_KeyStats'
	stock_list=[x[0] for x in os.walk(statspath)]#Getting all the directories
	stock_list.sort();
	df = pd.DataFrame(columns=['Date','Unix','Ticker','DE Ratio','Price','stock_p_change','SP500','sp500_p_change','Difference','Status'])

	
	sp500_df=pd.DataFrame.from_csv("YAHOO-INDEX_GSPC.csv")#Containing data about sp500 for about 10 years (Quandl.com)

	ticker_list=[]
	#print(stock_list)
	#print(statspath)
	for each_dir in stock_list[1:25]:
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
 					try:

 						value=source.split(gather+'</td><td class="yfnc_tabledata1">')[1]#searching for vales of DebtEquity
 						value2=float(value.split('</td>')[0])
 						#print(ticker+":",value2)
 						
 						#print(gather+'</td><td class="yfnc_tabledata1">')
 					except Exception as e:
 						
 						
 						#time.sleep(1)
 						value=source.split(gather+'</td>\r\n<td class="yfnc_tabledata1">')[1]#searching for vales of DebtEquity
 						value2=float(value.split('</td>')[0])
 						#print(str(e),ticker,file,value2)
 					try:
 						sp500_date=datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')
 						row=sp500_df[(sp500_df.index==sp500_date)]
 						sp500_value=float(row["Adjusted Close"])
 					except:
 						sp500_date=datetime.fromtimestamp(unix_time-259200).strftime('%Y-%m-%d')#Skipping the values by
 						row=sp500_df[(sp500_df.index==sp500_date)]#approx 3 days if is value not available on particular day 
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
						status="underperfrom"

					#Values added to the data frame

 					df=df.append({'Date':date_stamp,'Unix':unix_time,'Ticker':ticker,'DE Ratio':value2,'Price':stock_price2,'SP500':sp500_value,'stock_p_change':stock_p_change,'sp500_p_change':sp500_p_change,'Difference':diff,'Status':status,},ignore_index= True)#adding the value to the dataframe
 				except Exception as e:
 					pass



#----------------------------------------------------------------------------------------

# Plotting to get an idea about how many underperformed/outer performed
 	for each_ticker in ticker_list:
 		try:
 			plot_df=df[(df['Ticker']==each_ticker)]
 			plot_df=plot_df.set_index(['Date'])
 			if plot_df['Status'][-1]=="underperfrom":
 				color='r'
 			else:
 				color='g'
 			plot_df['Difference'].plot(label=each_ticker,color=color)
 			plt.legend()
 		except:
 			pass
 	plt.show()


#-------------------------------------------------------------------------------------------

#saving the file in csv format
 	save=gather.replace(' ','').replace(')','').replace('(','').replace('/','')+('.csv')#
 	print(save)
 	#df.to_csv(save)

Key_Stats()




