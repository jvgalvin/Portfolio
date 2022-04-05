import pandas as pd
import numpy as np
import os

### Import linkedin_file, sfdc_ct, and my_zips_frame as dataframes ###
linkedin_frame = pd.read_csv('/Users/jack.galvin/Desktop/LinkedIn Analysis/internet2linkedin.csv')
sfdc_frame = pd.read_csv('/Users/jack.galvin/Desktop/LinkedIn Analysis/sfdcct.csv')
my_zips_frame = pd.read_csv('/Users/jack.galvin/Desktop/LinkedIn Analysis/zips.csv')

# Append leading zero to zip code
linkedin_frame['headquarter_postal_code'] = linkedin_frame['headquarter_postal_code'].apply(lambda x: '{0:0>5}'.format(x))

### Filter linkedin_file so it has just accounts that should be looked into ###

def filter_linkedin_file(linkedin, my_zips):
	""" Filter linkedin_file so it only has accounts with zip codes contained in my_zips_frame and correct company size """
	
	my_zips_list = list(my_zips_frame['Zip Code'])
	filtered_by_zip = linkedin[linkedin['headquarter_postal_code'].isin(my_zips_list)]
	under_5k_employee = filtered_by_zip[filtered_by_zip['staff_count'] <= 5000]
	final_filtered_frame = under_5k_employee[under_5k_employee['staff_count'] >= 10]
	return final_filtered_frame

working_file = filter_linkedin_file(linkedin_frame,my_zips_frame)

### Identify OEM prospects and CDT prospects ###

oem_indicators, cdt_indicators = ['platform', 'saas', 'software', 'cloud', 'insights', 'actionable'], ['sql', 'python', 'data science']
oem_running_list, cdt_running_list = [], []

for line in working_file['description']:
	line = line.lower()
	if any(substring in line for substring in oem_indicators) == True:
		oem_running_list.append(1)
	else:
		oem_running_list.append(0)

for line in working_file['description']:
	line = line.lower()
	if any(substring in line for substring in cdt_indicators) == True:
		cdt_running_list.append(1)
	else:
		cdt_running_list.append(0)

working_file['oem_potential'] = oem_running_list
working_file['cdt_potential'] = cdt_running_list

def add_sfdc_scores(row):
	""" Pull in intent, buying stage, and profile fit from sfdc_frame by website key """

	intent_score, buying_stage, profile_fit = 0, [], []
	idx = 0
	website = str(working_file.iloc[row, 9]).lower().replace('/','').replace('.com', '').replace('http:', '').replace('.org', '').replace('www', '').replace('https:', '').replace('.', '').replace('net', '')
	if sfdc_frame['Website'].str.contains(website).any() == True:
		idx = sfdc_frame[sfdc_frame['Website'].str.contains(website, na = False)].index[0]
		intent_score = sfdc_frame.iloc[idx, 7]
		buying_stage = sfdc_frame.iloc[idx, 8]
		profile_fit = sfdc_frame.iloc[idx, 9]
	else:
		pass
	return intent_score, buying_stage, profile_fit
		
intent_scores, buying_stages, profile_fits = [], [], []
for line in range(len(working_file)):
	intent_scores.append(add_sfdc_scores(line)[0])
	buying_stages.append(add_sfdc_scores(line)[1])
	profile_fits.append(add_sfdc_scores(line)[2])

working_file['sfdc_intent_score'] = intent_scores
working_file['sfdc_buying_stage'] = buying_stages
working_file['sfdc_profile_fit'] = profile_fits

### Calculate a composite final OEM score ###

fc_pct_75, fc_pct_50, fc_pct_25 = np.percentile(working_file['follower_count'].to_numpy(), 75), np.percentile(working_file['follower_count'].to_numpy(), 50), np.percentile(working_file['follower_count'].to_numpy(), 25)
sc_pct_80, sc_pct_65, sc_pct_50 = np.percentile(working_file['staff_count'].to_numpy(), 80), np.percentile(working_file['staff_count'].to_numpy(), 65), np.percentile(working_file['staff_count'].to_numpy(), 50)
is_pct_85, is_pct_75, is_pct_65 = np.percentile(working_file['sfdc_intent_score'].to_numpy(), 85), np.percentile(working_file['sfdc_intent_score'].to_numpy(), 75), np.percentile(working_file['sfdc_intent_score'].to_numpy(), 65)

def calculate_oem_score(row):
	""" Calculates a composite OEM metric for a single company """
	oem_score = 0
	if working_file.iloc[row, 26] == 1:
		oem_score += 1
	if working_file.iloc[row, 14] >= fc_pct_75:
		oem_score += 3
	elif fc_pct_50 <= working_file.iloc[row, 14] < fc_pct_75:
		oem_score += 2
	elif fc_pct_25 <= working_file.iloc[row, 14] < fc_pct_50:
		oem_score += 1
	if working_file.iloc[row, 11] >= sc_pct_80:
		oem_score += 3
	elif sc_pct_65 <= working_file.iloc[row, 11] < sc_pct_80:
		oem_score += 2
	elif sc_pct_50 <= working_file.iloc[row, 11] < sc_pct_65:
		oem_score += 1
	if working_file.iloc[row, 28] >= is_pct_85:
		oem_score += 3
	elif is_pct_75 <= working_file.iloc[row, 28] < is_pct_85:
		oem_score += 2
	elif is_pct_65 <= working_file.iloc[row, 28] < is_pct_75:
		oem_score += 1
	else:
		pass
	return oem_score

final_scores = [calculate_oem_score(line) for line in range(len(working_file))]

working_file['final_oem_score'] = final_scores
working_file = working_file.sort_values('final_oem_score', ascending = False)
working_file.to_csv('ct_internet_companies_scored_2_18.csv')








	





