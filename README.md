# Portfolio Projects
## Airbnb Exploratory Data Analysis
### Context and Objective
March 2021 marked one year after my return to the Bay Area. My interest in further developing programming skills was growing and I thought an analysis of my former home city’s peer-to-peer housing market would offer me an opportunity to practice some Pandas and data visualization basics. The objective of this project was to quantify the extent to which Airbnb listings changed during the first year of Covid-19.
### Data, Libraries, and Environment
The data for this project was sourced from the Inside Airbnb data repository. After downloading the relevant files, I used Pandas, Seaborn, and Matplotlib to clean, explore, and analyze the data. All of this was done locally within a Jupyter Notebook.
### Results and Impact
As suspected, the total number of Airbnb listings plummeted. The average price per night fell more across Manhattan listings than it did across Brooklyn listings, despite an equivalent drop in the total number of listings in both boroughs. A full writeup can be found here on Medium.
### Learnings
This project taught me the importance of thoroughly exploring a data set. Although my goal was one of description, my exploratory data analysis revealed ancillary questions of explanation (what causes the difference in average price across boroughs) and prediction (what will average prices look like for the next year) that I may not have imagined if I had not closely examined the data set.

## Bitcoin Whale Random Forest Classifier
### Context and Objective
Bitcoin prices were rising rapidly at the time I conducted this project (May 2021). News articles of get-rich-quick stories with investments in Bitcoin created such hype that I considered whether it was possible to reliably bet against the market instead. My objective was to build a classifier that could determine if the net sum of Bitcoin whales’ trades within the next 24 hours would be negative.
### Data, Libraries, and Environment
The data for this project was sourced from the BitInfoCharts and Cryptodatadownload. I downloaded the historical Bitcoin prices and manually created the transaction history for the 100 richest Bitcoin addresses. I used Pandas for preprocessing and feature engineering and Plotly for interactive visualizations. I chose to use a random forest classifier due to its relative resistance to overfitting. All of this was done locally within a Jupyter Notebook.
### Results and Impact
My model achieved an AUC (area under the curve) score of 0.73. For those with more capital to spare, using this model as guidance may serve you very well when the Bitcoin bubble busts (alliteration totally intended). A full writeup can be found here on Medium.
### Learnings
This project taught me how important it is to be precise when defining a research question. In hindsight, I would not use classification for this type of question, as I would be more interested in knowing what the price will likely be within the next 24 hours - and form an investment decision accordingly.
