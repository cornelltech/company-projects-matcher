import teams
import numpy as np
import pandas as pd
from sklearn import preprocessing
from scipy import linalg
from scipy import spatial
import clustering

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

	print "One hot data[0] is "
	print one_hot_data[0]

def is_positive_semidefinite(matrix):
	def check_row(row):
		return [entry for entry in row if entry < 0]
	res = [row for row in matrix if not (check_row(row) == [])]
	return res == []

def do_mahal_distance(file, use_pseudo_inv = True):
	data_array = clustering.__init__(file)
	
	# After preprocessing, the vector is
	# (degree_pursuing, cs_ug, type_tech_stren, cod_abil, num_yrs_work_exp)
	one_hot_data_preprocessed = clustering.do_preprocessing(data_array)
	return one_hot_data_preprocessed
	
	covariance_matrix = np.cov(one_hot_data_preprocessed)
	print "Covariance matrix is: "
	print covariance_matrix

	if (not (is_positive_semidefinite(covariance_matrix))):
		error = ("Covariance matrix of data is not positive semidefinite, i.e., there exist ",
				 "negative eigenvalues. Fix this by applying a linear translation to input.")
		raise teams.FunctionError(error)

	# Calculate the inverse of the covariance matrix.
	if (not(use_pseudo_inv)):
		cov_inverse = linalg.inv(covariance_matrix)
		print "(Real) inverse of the covariance matrix is: "
		print cov_inverse

	# Calculate the pseudoinverse of a matrix.
	else:
		# TODO: Eventually want to use the matrix square root at some pt
		#  cov_inverse = linalg.pinv(matrix_square_root)
		cov_inverse = linalg.pinv(covariance_matrix)
		print "(Pseudo) inverse of the covariance matrix is: "
		print cov_inverse

	obs_zero = one_hot_data_preprocessed[0]
	obs_one = one_hot_data_preprocessed[1]

	

	#spatial.distance.mahalanobis()

if (__name__ == "__main__"):
	np.set_printoptions(threshold=np.nan)

	r = do_mahal_distance("survey_responses.csv")
	
	print is_positive_semidefinite(r)

	# check_positive_definite(np.array([[-1, -2], [5, 6]]))
	

	# Calcuate matrix square root (REALLY small and has j's in it, even for normalized data)
	# matrix_square_root = linalg.sqrtm(covariance)
	# print matrix_square_root

	

# Need to do one hot encoding  on these categories first 