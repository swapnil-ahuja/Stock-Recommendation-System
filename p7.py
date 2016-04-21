# This script is used to parse the websites and store the html files in a folder.
# Website Parsed Yahoo Finance 

import urllib3.request
import os
import time


path="/home/swapnil/Desktop/intraQuarter"

def Check_Yahoo():
	statspath = path+'/_KeyStats'
	stock_list=[x[0] for x in os.walk(statspath)]
	count=0
	for e in stock_list[1:]:
		try:
			e=e.replace(statspath+"/","")
			link="http://finance.yahoo.com/q/ks?s="+e.upper()+"+key+statistics"
			#resp=urllib3.request.urlopen(link).read()
			http=urllib3.PoolManager()
			resp = http.request('GET', link,preload_content=False).read()
			#print(str(resp))
			save=path+"/forward/"+str(e)+".html"
			store=open(save,"w")
			store.write(str(resp))
			store.close()
			count=count+1
			if count>70:
				count=0
				print("Sleeping for Rest")
				time.sleep(10)

		except Exception as e:
			print(str(e))
			time.sleep(2)


Check_Yahoo()