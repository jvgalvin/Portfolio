# Summary of Project

This is the second individual project that I completed as part of the course Fundamentals of Data Engineering, a core course for UC Berkeley's MIDS program. The goal of the project was to gain additional experience connecting to a SQL database, writing SQl queries, and visualizing data from these queries in a business user-friendly format. Moreover, I gained experience creating staging tables in PostgreSQL, parsing JSON, loading data into PostgreSQL, and validating data once it was loaded to staging tables. Like the first project, the output of this project is a recommendations for a fictional business, which was derived from data.

## Tools Used

I used a PostgreSQL database comprised of several tables containing synthetic sales and product data for a fictional meal prep and delivery business. I adopted functions written in Python from a lab I completed during this course to connect to the database, write and execute the queries required, and recursively print the contents of a JSON file. For data validation, I made use of fuzzy logic. For subsequent manipulation, I utilized Pandas and visualized plots using Matplotlib.

## Environment

I completed this project exclusively from a VM running on AWS within a docker cluster of anaconda and postgres containers. I used a Jupyter Notebook server within this cluster to work within the notebooks contained in this repository.

## How to Read Files in this Repository

The Jupyter Notebooks contained within this repository should be read / viewed in order, from 1 through 7. Notebooks 5 and 7 contain executive summaries and business recommendations for the fictitious business.
