import teams
import numpy as np
from sklearn import preprocessing
from scipy import linalg

def preprocess_random_data(data):
	enc = preprocessing.OneHotEncoder(categorical_features = [True, False, True, True, False])
	enc.fit(data)

	#For 'survey_responses.csv,' this produces a 49 x 15 matrix. The last 4 columns are our quantitative data.
	one_hot_data = enc.transform(data).toarray()

	print "The parameters are: " + str(enc.get_params())
	
	print "The feature indices are: "
	print enc.feature_indices_

	print "The number of values is " 
	print enc.n_values
	
	print "The one hot data is " 
	print one_hot_data
	return one_hot_data

if (__name__ == "__main__"):
	# The vectors come in as
	# (degree_pursuing, cod_abil, cs_ug, type_tech_stren, num_yrs_work_exp)
	a = teams.create_random_student_vectors(50)
	n = np.array(a)

	# After preprocessing, the vector is
	# (degree_pursuing, cs_ug, type_tech_stren, cod_abil, num_yrs_work_exp)
	one_hot_data = preprocess_random_data(n)
	 
	covariance = np.cov(one_hot_data)
	print covariance

	# Calcuate matrix square root
	matrix_square_root = linalg.sqrtm(covariance)
	print matrix_square_root

	# Calculate the pseudoinverse of a matrix.
	pseudo_inverse = linalg.pinv(matrix_square_root)
	print pseudo_inverse

# Need to do one hot encoding  on these categories first 