# Portfolio Projects
## End-to-End Containerized Face Detection App
### Context and Objective
The benefits of containerization are well-known. Compared to monolitihic applications, containerized applications are easier to ship, simpler to maintain, can run anywhere, and have resusable components. The goal of this project was to build an end-to-end containerized application.
### Data, Libraries, and Environment
There was no data acquisition or model training in this project, as I resused the pre-trained frontal face HAAR Cascade Classifier from OpenCV. The application is intended to capture a live video stream from an edge device (or VM emulation of an edge device) running on an ARM64 architecture and send individual frames for processing via MQTT to and cloud machine with an x86 architecture. The faces are extracted from each frame and sent to an S3 bucket for storage. The entire application is containerized and runs on K3s (lightweight version of Kubernetes).
### Results and Impact
I successfully built and deployed this application according to the requirements above. It is completely containerized, so any of these pieces can be reused and run anywhere. Additionally, the face detection model can be swapped out for a more sophisticated one. See the link for more details and access to the S3 bucket.
### Learnings
This project taught me how useful Docker containers and Kubernetes are for cloud-native technologies.
## Natural Language Processing - Classification of Direct- and Quasi-Identifiers with Transformers
### Context and Objective
Classification of direct- and quasi-identifiers in unstructured text is a task of increasing importance to privacy preservation and responsible data set creation. Although intersecting with well-studied Named Entity Recognition (NER) tasks (e.g. person identification, coreference resolution, location identification), classification of identifiers presents challenges due to the broad definition of identifiers and the length of content over which identifier context must be considered. Entities within legal and medical documents are often named at the beginning of the document with coreferences appearing thousands of tokens later. Accurate detection and masking of such identifiers could unlock datasets that would otherwise be locked to researchers based on privacy. My objective was to develop transformer models that beat the existing state-of-the-art benchmark for classification of direct- and quasi-identifiers.
### Data, Libraries, and Environment
The data was sourced from Pilán et. al. (reference in paper, see repo). Data consisted of 1,268 documents from the European Court of Human Rights and 553 out-of-domain Wikipedia articles. All Longformer models were trained on a VM on GCP with 96 CPU and 600+ GB of memory. Training framework for Longformer was Tensorflow and framework for DeBERTa was Pytorch.
### Results and Impact
I beat the state-of-the-art benchmark by concatenating the hidden states from the Longformer with document-level embeddings from SPECTER and feeding the concatenated tensor to a deep neural network. This model can be further improved by adjusting the sliding attention window of the Longformer. Additionally, follow up work would address how to replace tokens which are masked with meaningful alternatives so that such datasets could be used by researchers.
### Learnings
Combining deep learning with state-of-the-art models in NLP can have a massive impact across verticals. In my opinion, NLP stands to disrupt verticals which have not yet reaped the benefits of machine learning (i.e., venture capital, investment/asset management, legal).

## Lucy Classifier
### Context and Objective
I've become more interested in computer vision and wanted to try my hand at training a neural network that could discriminate between images of my own French Bulldog and other random Frenchies. I also wanted to deploy this as a lightweight Flask app. The objective was to use transfer learning to achieve a validation accuracy of 0.9 or higher.
### Data, Libraries, and Environment
The images of Lucy were taken by my family, friends, and me. The other images of Frenchies came from the Stanford Dogs Dataset. I trained the neural network locally and used Tensorflow as my training framework.
### Results and Impact
The network achieves a validation accuracy of 0.92 and a test accuracy of 0.96 (test set is smaller than validation set). A full writeup can be found on Medium.
### Learnings
Data preparation for computer vision projects should not be underestimated - time and complexity should be expected, despite how simple the task might seem. Training and validation data must be sufficiently similar. Image classification is easier understood than implemented. Training the model is only half the battle - deployment is nontrivial.

## Airbnb Exploratory Data Analysis
### Context and Objective
March 2021 marked one year after my return to the Bay Area. My interest in further developing programming skills was growing and I thought an analysis of my former home city’s peer-to-peer housing market would offer me an opportunity to practice some Pandas and data visualization basics. The objective of this project was to quantify the extent to which Airbnb listings changed during the first year of Covid-19.
### Data, Libraries, and Environment
The data for this project was sourced from the Inside Airbnb data repository. After downloading the relevant files, I used Pandas, Seaborn, and Matplotlib to clean, explore, and analyze the data. All of this was done locally within a Jupyter Notebook.
### Results and Impact
As suspected, the total number of Airbnb listings plummeted. The average price per night fell more across Manhattan listings than it did across Brooklyn listings, despite an equivalent drop in the total number of listings in both boroughs. A full writeup can be found on Medium.
### Learnings
This project taught me the importance of thoroughly exploring a data set. Although my goal was one of description, my exploratory data analysis revealed ancillary questions of explanation (what causes the difference in average price across boroughs) and prediction (what will average prices look like for the next year) that I may not have imagined if I had not closely examined the data set.

## Bitcoin Whale Random Forest Classifier
### Context and Objective
Bitcoin prices were rising rapidly at the time I conducted this project (May 2021). News articles of get-rich-quick stories with investments in Bitcoin created such hype that I considered whether it was possible to reliably bet against the market instead. My objective was to build a classifier that could determine if the net sum of Bitcoin whales’ trades within the next 24 hours would be negative.
### Data, Libraries, and Environment
The data for this project was sourced from the BitInfoCharts and Cryptodatadownload. I downloaded the historical Bitcoin prices and manually created the transaction history for the 100 richest Bitcoin addresses. I used Pandas for preprocessing and feature engineering and Plotly for interactive visualizations. I chose to use a random forest classifier due to its relative resistance to overfitting. All of this was done locally within a Jupyter Notebook.
### Results and Impact
My model achieved an AUC (area under the curve) score of 0.73. For those with more capital to spare, using this model as guidance may serve you very well when the Bitcoin bubble busts (alliteration totally intended). A full writeup can be found on Medium.
### Learnings
This project taught me how important it is to be precise when defining a research question. In hindsight, I would not use classification for this type of question, as I would be more interested in knowing what the price will likely be within the next 24 hours - and form an investment decision accordingly.

## Interactive Menu Builder
### Context and Objective
When restaurants shut down during Covid-19, even non-cookers dug deep to find their inner chef. I liked cooking even before this, but was tired of always deciding what to make. I decided to make a change in October 2021. My objective was to build a tool that would select a cocktail, appetizer, dinner, and dessert for me, based on my preferences or the occasion. More specifically, I wanted to practice creating and using classes in this project.
### Data, Libraries, and Environment
I gathered my favorite recipes for cocktails, appetizers, main courses, and desserts online and built separate csv files to mimic a database. I used Pandas to “query” these csv files and Python’s webbrowser library to automatically open the chosen recipes’ web pages in a browser. This program runs entirely within the command line.
### Results and Impact
Whenever I feel like cooking, but don’t want to endlessly debate myself about what to cook, I use this tool. More importantly, I gained valuable experience creating and using classes (the tool is comprised only of classes - there are only 6 lines of code that run the program).
### Learnings
This project helped me realize how much attention to detail is required to write production quality code. In addition to abiding by PEP-8 style guidelines to write readable and reusable code, I learned how to enumerate exhaustive test cases and implement comprehensive error checking to ensure the code does not crash on execution.

## Insider Stock Trading
### Context and Objective
I worked with two colleagues in December 2021 to investigate if buy or sell activity from insiders at publicly-traded companies could serve as a signal of future performance of broader market indices and that company’s stock price.
### Data, Libraries, and Environment
The insider trading activity data was sourced from the SEC’s EDGAR database and historical stock price data was sourced from Yahoo Finance. We used Numpy and Pandas for data cleansing and analysis and Matplotlib, Seaborn, and Plotly for visualizations. This was completed locally in Jupyter Notebooks through collaboration on GitHub.
### Results and Impact
We found that insider trading activity does not predict future performance of broader stock market indices, nor does it predict future performance of a specific company’s stock price. This analysis suggests that investors should include additional data points when making investment decisions.
### Learnings
This project was my first experience collaborating on a project using GitHub. I learned how to structure a repository, use the command line to resolve merge conflicts, and gained a general understanding (in practice) about how data science teams use GitHub to collaborate.

## Sales Prospect Scoring
### Context and Objective
In January 2021, I received a list of 2,000+ companies in my sales territory. I needed an easier and quicker way to prioritize them than manually visiting all of their websites and LinkedIn pages. My objective was to write a script that produces an ordered, prioritized list of accounts to target.
### Data, Libraries, and Environment
I purchased a subscription to LinkedIn Helper to scrape my prospects’ LinkedIn pages and enriched those results with data from Salesforce. I then used keywords within the companies’ descriptions on LinkedIn and primary enrichment tool data to produce a flat file of prioritized accounts. This was built locally and executed through the command line.
### Results and Impact
This saved myself roughly one month of work. Additionally, I used this script to help other members on my team prioritize their counts, which saved them months of work, too. A VP of Sales found that I (an Account Executive at the time) was writing code to prioritize accounts, which spurned conversations of expanding sales operations’ capabilities.
### Learnings
This project taught me that it can be a smarter use of time to invest upfront in clever ways of automating a repetitive task than manually plugging away at it. In hindsight, I would apply machine learning techniques to score these prospects (as opposed to devising my own rules for ranking them).

## Customer Segmentation
### Context and Objective
In February 2021, after prioritizing my prospective customer accounts, I wanted to validate if guidance to aim for accounts based on certain metrics was backed by data. My objective was to determine how existing customer accounts naturally clustered and compare the ARR received as a function of employee count, company revenue, and primary enrichment tool match score.
### Data, Libraries, and Environment
The data for this project came from Salesforce. I used Pandas for data preprocessing, Matplotlib for visualization, and scikit-learn for K-means clustering. This was done locally within Jupyter Notebooks.
### Results and Impact
This analysis revealed there really wasn’t any clear difference in ARR for existing accounts as a  function of employee count, company revenue, or enrichment tool match score. This suggested that there are likely other factors that contribute to ARR not captured within these metrics and that these metrics should be used only as guidance, not as deterministic features to be used in targeting or pricing.
### Learnings
I learned how to use unsupervised learning to segment customers along different dimensions. Additionally, I learned that KNN (k nearest neighbors) can be a useful algorithm for imputing null values in a data set.

## Sales Opportunity Classifiers
### Context and Objective
In March 2021, after I had prioritized my prospective accounts for sales outreach, I wanted to know which opportunities were worth the bulk of my time. My objective was to create classifiers that would tell me if an opportunity was likely to be won or not instead of using gut feelings.
### Data, Libraries, and Environment
The data for this project was sourced from Salesforce. I used Pandas, Matplotlib, and Seaborn for data preprocessing and visualizations and scikit-learn for model instantiation, fit, and evaluation. I did all of this locally within Jupyter Notebooks.
### Results and Impact
No classifier (logistic regression, random forest, or support vector machine) performed any better than simple chance performance (50%) at determining if an opportunity would be won. The classifiers were very good at predicting if a deal would be lost, though. It is highly likely that this was due to class imbalance and exclusion of additional features that could boost performance. 
### Learnings
This was my first experience creating supervised machine learning models. While there are several changes I would make in hindsight, I learned the general workflow for such projects and the benefits and limitations of certain models.

## SQL Queries and Functional Programming
### Context and Objective
In February 2022, executives at a fictitious meal prep company received sales data from a third party sales channel and wanted preliminary analytics. My objective was to provide them with initial analytics and recommendations based on what I observed in the data.
### Data, Libraries, and Environment
The data for this project was synthetic. It was stored within PostgreSQL. I used SQL to query the data and converted the results to a Pandas data frame for analysis. I used Matplotlib for visualizations. This was done within an Anaconda and PostgreSQL docker cluster on an AWS virtual machine.
### Results and Impact
Sales figures dipped several days before and after holidays. Additionally, data was available to devise and implement a recency, frequency, monetary value customer model. The complete set of recommendations can be found within the GitHub repository linked below. 
### Learnings
This was the first time that I was able to practice SQL outside of a MOOC or online learning setting. I learned the basic structure and syntax of SQL queries and some nuances therein.

## User Activity Analytics
### Context and Objective
In March 2022, executives at a fictitious meal prep company wanted to conduct a proof of concept with a third party delivery company. My objective was to assess if this relationship was one worth forming.
### Data, Libraries, and Environment
The data for this project was synthetic. I used Pandas to parse the sales data from the third party delivery company (JSON) and loaded this into PostgreSQL. I used fuzzywuzzy (fuzzy logic) to correct inaccuracies in the third party data. I used Matplotlib for visualizations. All of this was done within an Anaconda and PostgreSQL docker cluster on an AWS virtual machine.
### Results and Impact
The only customers who signed up for delivery through the third party service were ones who lived within 5 miles of the existing store location. I recommended pausing formation of a relationship and examining alternative ways of delivering meals. 
### Learnings
I learned how complex SQL queries can quickly become with this project (i.e., nested queries). Additionally, I learned how to parse JSON and why this format is preferred for those who create data (i.e., easy to add new fields) and despised by those who consume it (i.e., small changes in structure mandate updates to scripts).

## Meal Delivery Analysis (Business Expansion)
### Context and Objective
In April 2022, executives at a fictitious meal prep company expressed a desire to expand operations beyond a single location after a successful proof of concept with a third party delivery company. My objective was to work with two colleagues to devise data-driven recommendations about how this fictitious meal prep company could expand its operations.
### Data, Libraries, and Environment
The data for this project was synthetic. We created staging tables and loaded and validated the data within PostgreSQL. Next, we used Neo4j and Cypher’s gds (graph data science) library to build a graph database of the public transit network surrounding the existing company store location. This allowed us to use graph traversal and community detection algorithms to identify prospective future store locations. We used Google’s Map api for visualizations. All of this was done in an Anaconda, PostgreSQL, and Neo4j docker cluster on an AWS virtual machine.
### Results and Impact
We recommended a hybrid option for expansion via meal delivery (using public transit and drones), with a forecasted upside of $4.6M annually. This entailed opening 4 “satellite” locations to which meals would be carried via public transit from the existing store. Commuters could either pick up meals while using public transit or drones could deliver the meals to customers within a 1.5 mile radius.
### Learnings
This was the second project that I used GitHub to complete in a group setting. I gained additional experience resolving merge conflicts, working on branches, and using pull requests. Additionally, I learned how NoSQL graph databases lend themselves to solving certain business challenges and complement structured SQL databases.
