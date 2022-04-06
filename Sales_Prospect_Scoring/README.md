# Purpose
The purpose of creating this script was to make the prospecting process more efficient. Note this was created while I was an Account Executive and is specifically targeted for identifying prospective customers for Business Intelligence / Anlytics Software.

# Date
This project was completed in January 2021.

# Context
I was provided with a list of nearly 2,000 companies and their HQ zip codes by my former employer. This list represented the companies which I was expected to target. I thought that it would be more efficient to deploy a more automated way of targeting likely customers than sifting through 2,000 companies manually.

# Approach
I purchased a subscription to LinkedIn Helper, which combed through all LinkedIn company pages for companies with a HQ in my list of zip codes and produced a flat file with the name of the company, revenue, number of employees, description, and several other variables. I removed any companies which belonged to another division (Enterprise Sales). 

I used keywords that appear in the LinkedIn descriptions for current customers to identify prospects. Additionally, I combined this data with data about buying stage, profile fit, and intent score from Salesforce. 

Separately, I had clustered current customers to inform my scoring - the analysis cannot be published as it contains confidential information, but confirms that select fields from LinkedIn and the scores from Salesforce are informative. The clustering informed how the final scores were weighted. 

# Impact
This saved months of manual work for myself and my team.
