#Stock Recommender Using SciKit Learn 

###File Description:
- p1 : This script was intially used to parse data but later we wanted to parse more features,
therefore we we created modified version of this script(p2.py)
- p2 : This a fully working script but here the stock prices are provided by parsing Yahoo Finanace pages which had a 
lot of data which was N/A,therefore later we moved on a different source to get stock prices of the given stocks.
Next Version p5
- p3 : This script calculates the accuracy of our data by training and testing the data.
- p4 : Gets stock price data for the last 10 years of the given stocks through Quandl API and saves it as Stock_Prices.csv.
- p5 : It's different from the previous two versions as it obtains data from more reliable resources and is far
more practical in it's approach.
- p6 : This is the final script that implements the SVM on the data seta and predicts the nature of stocks in the future.
Finally suggesting us a few stocks for investing.
- p7 : This script is used to parse the website Yahoo Finance and store the html files in a folder.
- p8 : This script is similar to other scripts  that are used to parse html pages stored but here it is used only to get
present  stock prices from the html files downloaded using script p7.py,so that the algorithm could recommend some stocks for investing.


 
1) First we parsed the Yahoo Finance html pages collection that contains data related of multiple stocks 
for a time period of 10 years(2003-2013).These parsed html pages were also provided by sentdex.com

2) Large number of values of stock prices in these html pages are 'N/A'.Therefore we have taken the stock
prices for over 10 years using QUANDL API.

3) The values of sp500 for the same duaration was also gathered from QUANDL.

4) We have classified a stock on the basis of percentage change in stock value with respect to the sp500.
It is consisdered outperform when the change is more than 10 percent and underperform otherwise.

5) The above data was used to train the SVM Classifier using SciKit Machine Learning Library.First we
test the classifier using our testing data to get the idea of the accuracy of the algorithm.

6) We get the present values for all the features by parsing the Yahoo Finance Website.

7) We fed this present data into our trained classifier to gives us suggestion of the stocks that we should invest in.

This project was developed by taking help from the blogs written on the website sentdex.com



