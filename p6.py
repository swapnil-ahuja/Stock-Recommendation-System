#This is the final script that implements the SVM on the data seta and predicts the nature of stocks in the future.
#Finally suggesting us a few stocks for investing

import pandas as pd
import os
import time
import numpy as np
from sklearn import svm ,preprocessing
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
import re

from collections import Counter
style.use("ggplot")

FEATURES = ['DE Ratio', 'Trailing P/E', 'Price/Sales', 'Price/Book', 'Profit Margin', 'Operating Margin', 'Return on Assets', 'Return on Equity', 'Revenue Per Share', 'Market Cap', 'Enterprise Value', 'Forward P/E', 'PEG Ratio', 'Enterprise Value/Revenue', 'Enterprise Value/EBITDA', 'Revenue', 'Gross Profit', 'EBITDA', 'Net Income Avl to Common ', 'Diluted EPS', 'Earnings Growth', 'Revenue Growth', 'Total Cash', 'Total Cash Per Share', 'Total Debt', 'Current Ratio', 'Book Value Per Share', 'Cash Flow', 'Beta', 'Held by Insiders', 'Held by Institutions', 'Shares Short (as of', 'Short Ratio', 'Short % of Float', 'Shares Short (prior ']
Benchmark=8

def Build_Data_Set(features=FEATURES):
	data_df=pd.DataFrame.from_csv("Key_Stats_acc_perf_NO_NA.csv")
	#data_df=data_df[:100]
	#data_df=data_df.reindex(np.random.permutation(data_df.index))
	data_df=data_df.replace("NaN",-99999).replace("N/A",-99999)

	X=np.array(data_df[features].values)

	# y=(data_df["Status"].replace("underperform",0).replace("outperform",1).values.tolist())

	X=preprocessing.scale(X)

	z=np.array(data_df[["stock_p_change","sp500_p_change"]])

	y=(z[:,0]-z[:,1])
	# print(len(y))

	for i in range(len(y)):
		if y[i]>Benchmark:
			y[i]=1
		else:
			y[i]=0

	
	return X,y,z



def Analysis():
	
	test_size=1;

	# invest_amount=10000 # Invesment in Dollars $
	# total_invests=0
	# if_market=0
	# if_strat=0
	
	X,y,z=Build_Data_Set()
	#print(len(X))
	#print(y[:10])
	clf=svm.SVC(kernel="linear",C=1.0)
	clf.fit(X[:-test_size],y[:-test_size])
	
	# correct_count=0
	# for x in range(1,test_size+1):
	# 	if clf.predict(X[-x])[0] == y[-x]:
	# 		correct_count+=1
	# 	if clf.predict(X[-x])[0]==1:
	# 		invest_return=invest_amount +(invest_amount*(z[-x][0]/100))
	# 		market_return=invest_amount +(invest_amount*(z[-x][1]/100))

	# 		total_invests+=1
	# 		if_market+=market_return
	# 		if_strat+=invest_return



	#print(correct_count)
	#print(test_size)
	# Accuracy=((correct_count* 100.00)/test_size)
	# print ("Accuracy:",Accuracy)

	# print("Total Trades:",total_invests)
	# print("Ending with Strategy:",if_strat)
	# print("Ending with Market:",if_market)

	# compared=((if_strat-if_market)/if_market)*100.0
	# do_nothing=total_invests*invest_amount

	# avg_market=((if_market- do_nothing)/do_nothing)*100.0
	# avg_start=((if_strat- do_nothing)/do_nothing)*100.0



	# print("Compared to market we earn",str(compared)+"% more")
	# print("Average Invesment return:",str(avg_start)+"%")
	# print("Average Market return:",str(avg_market)+"%")


	data_df=pd.DataFrame.from_csv("forward_sample_NO_NA.csv")

	data_df=data_df.replace("N/A",-99999).replace("NaN",-99999)

	X=np.array(data_df[FEATURES].values)

	X=preprocessing.scale(X)

	z=data_df["Ticker"].values.tolist()

	invest_list=[]

	for i in range(len(X)):
		p=clf.predict(X[i])[0]
		if p==1:
			#print(z[i])
			invest_list.append(z[i])

	# print(len(invest_list))
	invest_list.sort()
	# print(invest_list)
	return invest_list


final_list=[]

loops=3
print("Wait while the list is being Prepared....")
for x in range(loops):
	stock_list=Analysis()
	#print("Loop Exceuted:"+str(x+1))
	for e in stock_list:
		final_list.append(e)

x= Counter(final_list)
f=[]

print("\n\nStocks You Should Invest In-:")

for each in x:
	if x[each]>loops-1:
		f.append(each)
		#print str(each)+"_",

#print(f)
path="/home/swapnil/Desktop/intraQuarter"
print(30*'_')
for each in f[1:]:
    full_file_path=path+"/forward/"+str(each)+".html"
    source=open(full_file_path,"r").read()
    #print(each)
    each="("+str(each)+")"
    each=each.upper()
    #print(each)
    value=source.split(each+"</h2>")[0]
    value2=value.split('<div class="title"><h2>')[1]
    print(value2+"\n")




# Build_Data_Set()






