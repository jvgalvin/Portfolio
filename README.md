# Purpose
The purpose of this project was to perform an exploratory data analysis in a team setting. This project was completed with Joshua Fram and Wilford Bradford.

# Context
The SEC requires all executives at US listed public companies to disclose any trading activity conducted in the shares of companies for whom they work. This “Insider” buying and selling activity is updated frequently and publicly available for investors to download from the SEC’s website. Some investors have developed strategies that track this data, driven by the notion that if a company’s CEO is buying stock in their own company, it is an indication that they believe it is a good investment. This is ostensibly an important indicator given that the CEO is the person who should be most familiar with the company and its prospects. The reverse holds as well – if an executive is reporting sales of their company, it may be a bad signal about the prospects of that company. This EDA uncovers whether there is a relationship between “Insider” activity and a company’s stock price.

# Data
Primary Dataset: The SEC’s EDGAR Database maintains a running list of all “insider” buys and sells reported via Form 4 submissions. This will be the primary data set. Specifically, the sample set is isolated to companies that saw Insider activity in the 4th quarter of 2018.

The data can be found here: https://www.gurufocus.com/insider/summary

Secondary Dataset: Daily stock returns for a 1-year period following any insider activity that occurred in the sample period (4Q 2018).

The data can be found here: https://finance.yahoo.com/quote/SLS/history?period1=1546300800&period2=1577750400&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true

# Highline Summary
Aggregate insider buying and selling does not predict future performance of broader stock market indices. Moreover, insider buying and selling do not predict future performance of the respective stock that is being bought or sold.
