# Purpose
The purpose of this personal project is to practice ingesting data from multiple sources, processing and preparing data for a machine learning task, and implementing a machine learning model.

# Context
Several articles indicate that a subset of BitCoin addresses have the power to manipulate the value of the currency. These addresses are dubbed the BitCoin "whales." I determined that if one could accurately predict when the whales would sell the currency, one could short the currency beforehand to make a profit. I hypothesized that fluctuations in the price of BTC may influence when whales buy and sell the currency.

# Data
I used historical BitCoin price data from https://www.cryptodatadownload.com/ and transaction history for the richest 100 BitCoin addresses in the world from https://bitinfocharts.com/top-100-richest-bitcoin-addresses.html.

# Model
I chose to implement a random forest classifier due to it being relatively resistant to overfitting.

# Top Line Summary
A random forest classifier can correctly determine whether or not the sum of all the whales' transactions within the next 24 hours will be negative 73% of the time.

# Writeup
See https://johnvgalvin.medium.com/bitcoin-whales-and-their-power-to-influence-price-fluctuations-d967f04e69b0 for the more complete summary on Medium.
