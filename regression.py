import pandas as pd 
import numpy as np 
import statsmodels.api as sm 

def do_all_regressions(file):
	data = pd.read_csv(file)
	#data_array = np.array(data)
	
	# ug_major = data_array[:,0]
	# coding_ability = data_array[:,1]
	# degree_pursuing = data_array[:,2]
	# num_yrs_work_experience = data_array[:,3]
	# group_experience = data_array[:,4]
	# m_group_experience = data_array[:,5]

	# do_three_regression('coding_ability','num_yrs_work_experience', 'group_experience', 'm_group_experience', data)

	we = 'num_yrs_work_experience'
	ge = 'group_experience'
	mge = 'm_group_experience'
	ca = 'coding_ability'


	print "Predict coding ability through work experience, group experience, and m_group experience"
	x = data[[we, ge, mge]]
	y = data[ca]
	do_regression(x, y)
	print ""

	print "Predict group experience through work experience, coding ability, and m_group experience"
	x1 = data[[we, ca, mge]]
	y1 = data[ge]
	do_regression(x1, y1)
	print ""

	print "Predict m_group experience through work experience, coding ability, and group experience"
	x2 = data[[we, ca, ge]]
	y2 = data[mge]
	do_regression(x2, y2)
	print ""

	print "Predict work experience through group experience, coding ability, and m_group experience"
	x3 = data[[ca, mge, ge]]
	y3 = data[we]
	do_regression(x3, y3)
	print ""

	print "Predict work experience through coding ability and m_group experience"
	x3 = data[[ca, mge]]
	y3 = data[we]
	do_regression(x3, y3)
	print ""

	print "Predict coding ability through work experience and m_group experience"
	x3 = data[[we, mge]]
	y3 = data[ca]
	do_regression(x3, y3)
	print ""

	print "Predict m_group experience through work experience and coding ability"
	x3 = data[[we, ca]]
	y3 = data[mge]
	do_regression(x3, y3)
	print ""

def do_regression(x, y):
	estimate = sm.OLS(y, x).fit()
	print estimate.summary()

if __name__ == "__main__":
	do_all_regressions('survey_responses.csv')