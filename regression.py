import pandas as pd 
import numpy as np 
import statsmodels.api as sm 

def do_regression(file):
	data = pd.read_csv(file)
	#data_array = np.array(data)
	
	# ug_major = data_array[:,0]
	# coding_ability = data_array[:,1]
	# degree_pursuing = data_array[:,2]
	# num_yrs_work_experience = data_array[:,3]
	# group_experience = data_array[:,4]
	# m_group_experience = data_array[:,5]

	x = data[['num_yrs_work_experience', 'group_experience', 'm_group_experience']]
	y = data['coding_ability']

	estimate = sm.OLS(y, x).fit()
	print estimate.summary()

if __name__ == "__main__":
	do_regression('survey_responses.csv')