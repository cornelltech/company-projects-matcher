import pandas as pd 
import numpy as np 
import statsmodels.api as sm
import statsmodels.discrete as disc  

def do_all_linear_regressions(ug, ca, dp, we, ge, mge, data):

	print "Predict coding ability through work experience, group experience, and m_group experience"
	x = data[[we, ge, mge]]
	y = data[ca]
	do_linear_regression(x, y)
	print ""

	print "Predict group experience through work experience, coding ability, and m_group experience"
	x1 = data[[we, ca, mge]]
	y1 = data[ge]
	do_linear_regression(x1, y1)
	print ""

	print "Predict m_group experience through work experience, coding ability, and group experience"
	x2 = data[[we, ca, ge]]
	y2 = data[mge]
	do_linear_regression(x2, y2)
	print ""

	print "Predict work experience through group experience, coding ability, and m_group experience"
	x3 = data[[ca, mge, ge]]
	y3 = data[we]
	do_linear_regression(x3, y3)
	print ""

	print "Predict work experience through coding ability and m_group experience"
	x3 = data[[ca, mge]]
	y3 = data[we]
	do_linear_regression(x3, y3)
	print ""

	print "Predict coding ability through work experience and m_group experience"
	x3 = data[[we, mge]]
	y3 = data[ca]
	do_linear_regression(x3, y3)
	print ""

	print "Predict m_group experience through work experience and coding ability"
	x3 = data[[we, ca]]
	y3 = data[mge]
	do_linear_regression(x3, y3)
	print ""

def do_linear_regression(x, y):
	model = sm.OLS(y, x)
	estimate = model.fit()
	print estimate.summary()

def do_all_mn_logits(ug, ca, dp, we, ge, mge, data):

	# NOTE: This raises "Warning: Maximum number of iterations has been exceeded.
	#       Current function value: nan
 	#       Iterations: 35"

	print "Predict undergrad major through all other variables."
	x = data[[ca, dp, we, ge, mge]]
	y = data[ug]
	do_mn_logit(x, y)
	print ""

	# NOTE: This raises "Warning: Maximum number of iterations has been exceeded.
 	#        Current function value: nan
	#         Iterations: 35"

	print "Predict undergrad major through all other variables except work experience."
	x = data[[ca, dp, ge, mge]]
	y = data[ug]
	do_mn_logit(x, y)
	print ""

	# NOTE: This raises "Warning: Maximum number of iterations has been exceeded.
    #     Current function value: 0.999195
    #     Iterations: 35"
	print "Predict undergrad major through all non-categorical variables."
	x = data[[ca, we, ge, mge]]
	y = data[ug]
	do_mn_logit(x, y)
	print ""
	
	# NOTE: This raises "numpy.linalg.linalg.LinAlgError: Singular matrix"

	# print "Predict undergrad major through all non-categorical variables except work experience."
	# x = data[[ca, ge, mge]]
	# y = data[ug]
	# do_mn_logit(x, y)
	# print ""

	print "Predict degree pursuing through all other variables."
	x = data[[ca, ug, ge, mge, we]]
	y = data[dp]
	do_mn_logit(x, y)
	print ""

	print "Predict degree pursuing through all other variables except work experience."
	x = data[[ca, ug, ge, mge]]
	y = data[dp]
	do_mn_logit(x, y)
	print ""

	print "Predict degree pursuing through all non-categorical variables."
	x = data[[ca, we, ge, mge]]
	y = data[dp]
	do_mn_logit(x, y)
	print ""

	print "Predict degree pursuing through all non-categorical variables except work experience."
	x = data[[ca, ge, mge]]
	y = data[dp]
	do_mn_logit(x, y)
	print ""

def do_mn_logit(x, y):
	model = disc.discrete_model.MNLogit(y, x)
	estimate = model.fit()
	print estimate.summary()

def extract_columns(file):
	data = pd.read_csv(file)
	ug = 'ug_major'
	ca = 'coding_ability'
	dp = 'degree_pursuing'
	we = 'num_yrs_work_experience'
	ge = 'group_experience'
	mge = 'm_group_experience'
	return ug, ca, dp, we, ge, mge, data

if __name__ == "__main__":
	''' Perform multinomial logistic regression with undergraduate major and degree pursuing as the
		dependent variables. '''

	ug, ca, dp, we, ge, mge, data = extract_columns('survey_responses.csv')
	# do_all_linear_regressions(ug, ca, dp, we, ge, mge, data)
	
	do_all_mn_logits(ug, ca, dp, we, ge, mge, data)


	







