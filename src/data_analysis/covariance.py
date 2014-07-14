#import teams
import numpy as np
import pandas as pd
from sklearn import preprocessing
from scipy import linalg
from scipy import spatial
from statsmodels.stats import correlation_tools
import clustering

default_file = "/Users/ameyaacharya/Documents/Projects/Company Projects/Code/company-projects-matcher/data/survey_responses.csv"

class CovarianceError(Exception):
	def __init__(self, value):
		self.val = value
	def __str__(self):
		return repr(self.val)

# Used for early early testing, probably won't use again.
# def preprocess_random_data(data):
# 	enc = preprocessing.OneHotEncoder(categorical_features = [True, False, True, True, False])
# 	enc.fit(data)

# 	#For 'survey_responses.csv,' this produces a 49 x 15 matrix. The last 4 columns are our quantitative data.
# 	one_hot_data = enc.transform(data).toarray()

# 	print "The parameters are: " + str(enc.get_params())
	
# 	print "The feature indices are: "
# 	print enc.feature_indices_

# 	print "The number of values is " 
# 	print enc.n_values
	
# 	print "The one hot data is " 
# 	print one_hot_data

# 	return one_hot_data

# Calculates all eigenvalues of the matrix
# If there are negative eigenvalues, returns false.
def is_positive_semidefinite(cov_matrix):
	(eigenvalues, eigenvectors) = linalg.eig(cov_matrix)
	res = []
	#print eigenvalues.shape
	for e in eigenvalues:
		#print e
 		if (e < 0):
	 		res.append(e)
	#print "Negative eigenvalues of covariance matrix are:"
	#print res
	return len(res) == 0

# Reads the data from the file (if we need to fix how the data is read, change clustering init.)
# Preprocesses data with one hot encoding (changes categorical variables into numerical.)
# Fixes matrix if it's not positive semidefinite (adds a small version of the identity.)
# Returns (data, covariance matrix.)
def create_covariance_matrix(file = default_file):
	data_array = clustering.__init__(file)
	one_hot_data_preprocessed = clustering.do_preprocessing(data_array)
	print "One hot data preprocessed is: "
	print one_hot_data_preprocessed
	print one_hot_data_preprocessed.shape

	# rowvar = 0 because each column represents a variable, while the rows are observations
	covariance_matrix = np.cov(one_hot_data_preprocessed, rowvar = 0)
	print "Covariance matrix is:"
	print covariance_matrix
	shape = covariance_matrix.shape
	print shape
	num_rows = shape[0]
	num_cols = shape[1]
	
	# Should never happen
	if (not(num_rows == num_cols)):
		raise CovarianceError("Covariance matrix is not a square matrix.")

	else:
		if (is_positive_semidefinite(covariance_matrix)):
			print "Pos semi def on the first try!"
			pass		
		# Our covariance matrix is not positive semidefinite -- an arithmetic error.
		# Will add (a small number * the identity matrix) to covariance matrix to fix this error.
		else:
			print "Not pos semi def on the first try!"
			n = num_rows
			i = np.array(np.identity(n))
			factor = 10. ** -10
			# Create a matrix that is a small number times the identity.
			small_identity = np.multiply(i, factor)

			# Add that matrix to our covariance matrix (to make sure that our matrix is positive semidefinite.)
			result = np.add(small_identity, covariance_matrix)
			if (not(is_positive_semidefinite(result))):
				raise CovarianceError("Fixed covariance matrix is not positive semidefinite.")
			else:
				covariance_matrix = result

	return (one_hot_data_preprocessed, covariance_matrix)

# Calcuate matrix square root using scipy linalg
def sqrt_covariance_matrix(covariance_matrix):	
 	matrix_square_root = linalg.sqrtm(covariance_matrix)
	return matrix_square_root

def inverse_matrix(sqrt_covariance_matrix, use_pseudo_inv = True):
	
	# Calculate real matrix inverse.
	if (not(use_pseudo_inv)):
	 	cov_inverse = linalg.inv(sqrt_covariance_matrix)
	 	print "(Real) inverse of the sqrt. covariance matrix is: "

	# Calculate the matrix pseudoinverse.
	else:
	 	cov_inverse = np.linalg.pinv(sqrt_covariance_matrix)
		print "(Pseudo) inverse of the sqrt. covariance matrix is: "

	#print cov_inverse
	return cov_inverse
	
def do_mahal_distance(student_one, student_two, use_pseudo_inv = True, file = default_file):
	
	# Calculate the inverse of the covariance matrix.
	# 
	# TODO: not sure if we even want to use this. Could go through steps like Serge listed.
	# obs_zero = one_hot_data_preprocessed[0]
	# obs_one = one_hot_data_preprocessed[1]
	# print "Mahal distance is " + str(spatial.distance.mahalanobis(obs_zero, obs_one, cov_inverse))

	# TODO: should return the Mahalanobis distance between the data at the two indices.
	# TODO TODO: should pass in a team, and return the sorted list of mahal distances at all points.

	pass

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
	# Will print out the entire matrix if necessary
	#np.set_printoptions(threshold=np.nan)

	tup = create_covariance_matrix()
	data = tup[0]
	covariance_matrix = tup[1]

	sq_cov = sqrt_covariance_matrix(covariance_matrix)
	inv_sq_cov = inverse_matrix(sq_cov)
	print inv_sq_cov
	#print "Square root of covariance matrix is: "
	#print sq_cov

	#print "Eigenvalues are: "
	#print linalg.eig(cov)

	# SANITY CHECKS for matrix square root
	#print "Eigenvalues of square root are:"
	#print linalg.eig(sq_cov)
	#c = np.multiply(sq_cov, sq_cov)
	#print "Covariance matrix is: "
	#print covariance_matrix
	#print "Sqrt multiplied by itself:"
	#print c
	#print "Covariance matrix minus sqrt*sqrt:"
	#print covariance_matrix - c
	#print (c == covariance_matrix)
	#inverse_matrix(sq_cov)




