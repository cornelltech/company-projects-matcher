company-projects-matcher
========================

The matching algorithm for Company Projects: CS 5999.

data: 
	original_survey_responses.csv: unedited
	survey_responses.csv: edited (i.e. numbers for categorical variables, removed timestamps, etc.)
	  
	Contains the data used for initial clustering, regression, and Mahalanobis distance analysis (housed in src/data_analysis).
	This data is made up of 49 responses to the survey docs/link_to_survey.txt.

docs:
	Information on Data: description of possible responses to survey questions. Details variables as categorical or numerical.
	link_to_survey.txt: survey.
	Types of Regression.txt: notes on various types of regression that I could have used.

results:
	Multinomial Logit Results.txt
	OLS Results.txt

	Results from various types of regression analyses, written to files.

src:
	classes:
		student_tests.py
		student.py
		superlongbothteams.py (TEMP)
		teams.py

		Contains all of the classes that will be used to wrap data from survey responses.

	data_analysis:
		clustering.py
		covariance.py
		histogram.py
		regression.py
		scatterplot.py

		Generates a variety of statistical analysis methods.

