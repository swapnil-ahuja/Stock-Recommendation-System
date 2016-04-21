#This script calculates the accuracy of our data by training and testing the data.

import pandas as pd
import os
import time
import numpy as np
from sklearn import svm ,preprocessing
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
import re
style.use("ggplot")

FEATURES = ['DE Ratio', 'Trailing P/E', 'Price/Sales', 'Price/Book', 'Profit Margin', 'Operating Margin', 'Return on Assets', 'Return on Equity', 'Revenue Per Share', 'Market Cap', 'Enterprise Value', 'Forward P/E', 'PEG Ratio', 'Enterprise Value/Revenue', 'Enterprise Value/EBITDA', 'Revenue', 'Gross Profit', 'EBITDA', 'Net Income Avl to Common ', 'Diluted EPS', 'Earnings Growth', 'Revenue Growth', 'Total Cash', 'Total Cash Per Share', 'Total Debt', 'Current Ratio', 'Book Value Per Share', 'Cash Flow', 'Beta', 'Held by Insiders', 'Held by Institutions', 'Shares Short (as of', 'Short Ratio', 'Short % of Float', 'Shares Short (prior ']


def Build_Data_Set(features=FEATURES):
	data_df=pd.DataFrame.from_csv("Key_Stats.csv")
	#data_df=data_df[:100]
	data_df=data_df.reindex(np.random.permutation(data_df.index))
	X=np.array(data_df[features].values)

	y=(data_df["Status"].replace("underperform",0).replace("outperform",1).values.tolist())

	X=preprocessing.scale(X)

	return X,y

def Analysis():
	
	test_size=1000;
	
	X,y=Build_Data_Set()
	print(len(X))
	#print(y[:10])
	clf=svm.SVC(kernel="linear",C=1.0)
	clf.fit(X[:-test_size],y[:-test_size])
	
	correct_count=0
	for x in range(1,test_size+1):
		if clf.predict(X[-x])[0] == y[-x]:
			correct_count+=1

	#print(correct_count)
	#print(test_size)
	Accuracy=((correct_count* 100.00)/test_size)
	print ("Accuracy:",Accuracy)

# def Randomizing():
# 	df=pd.DataFrame({"D1":range(5),"D2":range(5)})
# 	print(df)
# 	df2=df.reindex(np.random.permutation(df.index))
# 	print(df2)



#Randomizing()






Analysis()







