import teams
import numpy as np
import pandas as pd
from sklearn import preprocessing
from scipy import linalg
from scipy import spatial
from statsmodels.stats import correlation_tools
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

def is_positive_semidefinite(matrix):
	def check_row(row):
		return [entry for entry in row if entry < 0]
	res = [check_row(row) for row in matrix if (not(check_row(row)) ==  [])]
	print "Result of is_positive_semidefinite is "
	print res
	return len(res) == 0

def print_det_and_error(cov_one, cov_two):
	print "Determinant of the nearest correlation matrix is: "
	print linalg.det(cov_two)
	print "Error is: "
	print (cov_one - cov_two)

def do_mahal_distance(student_one, student_two, use_pseudo_inv = True, file = "survey_responses.csv"):
	data_array = clustering.__init__(file)
	
	# (degree_pursuing, cs_ug, type_tech_stren, cod_abil, num_yrs_work_exp)
	one_hot_data_preprocessed = clustering.do_preprocessing(data_array)

	covariance_matrix = np.cov(one_hot_data_preprocessed)

	if (not (is_positive_semidefinite(covariance_matrix))):
		# Could use cov_nearest, but that doesn't produce a positive semidefinite matrix.
		covariance_matrix_two = correlation_tools.corr_nearest(covariance_matrix)
		print_det_and_error(covariance_matrix, covariance_matrix_two)
		covariance_matrix = covariance_matrix_two

	# Calculate the inverse of the covariance matrix.
	if (not(use_pseudo_inv)):
		cov_inverse = linalg.inv(covariance_matrix)
		print "(Real) inverse of the covariance matrix is: "
		print cov_inverse

	# Calculate the pseudoinverse of a matrix.
	else:
		# TODO: Use the matrix square root.
		# cov_inverse = linalg.pinv(matrix_square_root)
		cov_inverse = linalg.pinv(covariance_matrix)
		print "(Pseudo) inverse of the covariance matrix is: "
		print cov_inverse

	# TODO: not sure if we even want to use this. Could go through steps like Serge listed.
	# obs_zero = one_hot_data_preprocessed[0]
	# obs_one = one_hot_data_preprocessed[1]
	# print "Mahal distance is " + str(spatial.distance.mahalanobis(obs_zero, obs_one, cov_inverse))

	# TODO: should return the Mahalanobis distance between the data at the two indices.
	# TODO TODO: should pass in a team, and return the sorted list of mahal distances at all points.
	return (one_hot_data_preprocessed, covariance_matrix_two)

# Pass in team of Students.
# TODO: make a Team ID, and return (Team_ID, result.)
def average_mahal_distance_team(team):
	result = []
	for mem_one in team:
		for mem_two in team:
			if (not(mem_one.ID == mem_two.ID)):
				result.append(do_mahal_distance(mem_one, mem_two))
	return np.mean(result)

def do_and_sort_all_mahal_dists(set_of_teams):
	result = []
	for team in set_of_teams:
		result.append(average_mahal_distance_team)
	return result.sort()

if (__name__ == "__main__"):
	np.set_printoptions(threshold=np.nan)

	result = do_mahal_distance(0, 1)
	data = result[0]
	fixed_cov  = result[1]
	
	print "On fixed: "
	print is_positive_semidefinite(fixed_cov)

	print "Eigenvalues are: "
	print linalg.eig(fixed_cov)
	
	# Calcuate matrix square root (REALLY small and complex, even for normalized data)
 	# matrix_square_root = linalg.sqrtm(fixed_cov)
	# print matrix_square_root


	

# Need to do one hot encoding  on these categories first 