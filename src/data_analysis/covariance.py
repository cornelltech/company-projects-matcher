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
def create_covariance_matrix(file = default_file, verbose = False):
	data_array = clustering.__init__(file)
	one_hot_data_preprocessed = clustering.do_preprocessing(data_array)
	
	if (verbose):
		print "One hot data preprocessed is: "
		print one_hot_data_preprocessed
		print one_hot_data_preprocessed.shape

	# rowvar = 0 because each column represents a variable, while the rows are observations
	covariance_matrix = np.cov(one_hot_data_preprocessed, rowvar = 0)
	if (verbose):
		print "Covariance matrix is:"
		print covariance_matrix
	shape = covariance_matrix.shape
	num_rows = shape[0]
	num_cols = shape[1]
	
	# Should never happen
	if (not(num_rows == num_cols)):
		raise CovarianceError("Covariance matrix is not a square matrix.")

	else:
		if (is_positive_semidefinite(covariance_matrix)):
			if (verbose):
				print "Pos semi def on the first try!"
			pass		
		# Our covariance matrix is not positive semidefinite -- an arithmetic error.
		# Will add (a small number * the identity matrix) to covariance matrix to fix this error.
		else:
			if (verbose):
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

	return (data_array, one_hot_data_preprocessed, covariance_matrix)

# Calcuate matrix square root using scipy linalg
def sqrt_covariance_matrix(covariance_matrix):	
 	matrix_square_root = linalg.sqrtm(covariance_matrix)
	return matrix_square_root

def inverse_matrix(sqrt_covariance_matrix, use_pseudo_inv = True, verbose = False):
	
	# Calculate real matrix inverse.
	if (not(use_pseudo_inv)):
	 	cov_inverse = linalg.inv(sqrt_covariance_matrix)
	 	if (verbose):
	 		print "(Real) inverse of the sqrt. covariance matrix is: "

	# Calculate the matrix pseudoinverse.
	else:
	 	cov_inverse = np.linalg.pinv(sqrt_covariance_matrix)
	 	if (verbose):
			print "(Pseudo) inverse of the sqrt. covariance matrix is: "

	#print cov_inverse
	return cov_inverse

# Implements:
# f(x, y) = 
# 	1 IF x = y
# 	0.75 IF abs(x - y) = 1
# 	1/(abs(x-y)) otherwise
# NOTE: x, y in [0, 4] for coding ability, and x, y in [0, 6] for work experience
def calc_numerical_difference(x, y):
	if (x == y):
		return 1.0
	elif (abs(x - y) == 1):
		return 0.75
	else:
		return (1.0 / ((abs(x-y))*1.0))

def subtract_vectors(s_one_properties, s_two_properties, verbose = False):

	# Extract the values of interest
	# ca_one = s_one_properties[10]
	# ca_two = s_two_properties[10]
	# work_one = s_one_properties[11]
	# work_two = s_two_properties[11]

	# s_one_properties[10] = 0
	# s_two_properties[10] = 0
	# s_one_properties[11] = 0
	# s_two_properties[11] = 0

	# Calculate our function for these values

	#coding_diff = calc_numerical_difference(ca_one, ca_two)
	#work_diff = calc_numerical_difference(work_one, work_two)

	a = np.subtract(s_one_properties, s_two_properties)
	a = np.absolute(a)

	print "Absolute value of subtracted vectors is:"
	print a
	
	#res = res + coding_diff + work_diff

	#return res

	
	
def do_mahal_distance(s_one_properties, s_two_properties, inv_sq_cov_mat, verbose = False, fixed_with_zeros = True):
	
	# Calculate the inverse of the covariance matrix.
	# 
	# TODO: not sure if we even want to use this. Could go through steps like Serge listed.
	# obs_zero = one_hot_data_preprocessed[0]
	# obs_one = one_hot_data_preprocessed[1]
	# print "Mahal distance is " + str(spatial.distance.mahalanobis(obs_zero, obs_one, cov_inverse))

	# TODO: should return the Mahalanobis distance between the data at the two indices.
	# TODO TODO: should pass in a team, and return the sorted list of mahal distances at all points.

	# Extract the values of interest
	ca_one = s_one_properties[10]
	ca_two = s_two_properties[10]
	work_one = s_one_properties[11]
	work_two = s_two_properties[11]

	if (fixed_with_zeros):
	# Reset these values in the original vectors to 0
	# so they don't affect the dot products.
		s_one_properties[10] = 0
		s_two_properties[10] = 0
		s_one_properties[11] = 0
		s_two_properties[11] = 0

	# Calculate our function for these values

	coding_diff = calc_numerical_difference(ca_one, ca_two)
	work_diff = calc_numerical_difference(work_one, work_two)

	a = np.dot(s_one_properties, inv_sq_cov_mat)
	res = np.dot(a, s_two_properties)
	if (verbose):
		print "Dotted value: " + str(res)
	
	if (fixed_with_zeros):
		res = res + coding_diff + work_diff

	if (verbose):
		print "Calculated values:",
		print coding_diff,
		print work_diff,

	return res

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

def use_python_distance_data(student_one, student_two, inv_sq_cov_mat):
	return spatial.distance.mahalanobis(student_one, student_two, inv_sq_cov_mat)
	
# The input "python" decides if we use the built-in mahalanobis distance or not
def do_all_distances_data(data, inv_sq_cov_mat, unprocessed_data, start = 0, verbose = False, python = False):
	i = start
	j = start
	res = []
	for student_one in data:
		for student_two in data:
			# Even this doesn't give every vector dotted with itself to be zero.
			#d = np.dot(student_one, student_two)
			if (not(python)):
				d = do_mahal_distance(student_one, student_two, inv_sq_cov_mat)
			else:
				d = use_python_distance_data(student_one, student_two, inv_sq_cov_mat)
			tup = ((i, j), d)
			keys = [t[0] for t in res]
			if ((j, i) in keys):
				pass
			else:
				res.append(tup)
			j += 1
		i += 1
		j = start
	res.sort(key = lambda tup: tup[1])
	#minimum_tuple = res[0]
	#minimum = minimum_tuple[1]
	if (verbose):
		 for i in res:
		 	tup = i[0]
		 	first_student = tup[0]
			second_student = tup[1]

			lst_first_student = unprocessed_data[first_student]
			lst_second_student = unprocessed_data[second_student]

			#print "(",
			# print "UG major: " + str((lst_first_student[0], lst_second_student[0]))
			# print "Coding ability: " + str((lst_first_student[1], lst_second_student[1]))
			# print "Degree pursuing: " + str((lst_first_student[2], lst_second_student[2]))
			# print "Work exp. (yrs) " + str((lst_first_student[3], lst_second_student[3]))

			# print "Coding ability: " + str((unprocessed_data[first_student])[1]) + str((unprocessed_data[second_student])[1]),
			# print "Degree pursuing: " + str((unprocessed_data[first_student])[2]) + str((unprocessed_data[second_student])[2]),
			# print "Num. years work experience: " + str((unprocessed_data[first_student])[3]) + str((unprocessed_data[second_student])[3]),
			# for elm in unprocessed_data[first_student]:
			# 	print elm,
			# print ";",
			# for elm in unprocessed_data[second_student]:
			# 	print elm,
			# print ")",

			print lst_first_student
			print lst_second_student

			#print i[1] - minimum
			print i[1]

	return res

if (__name__ == "__main__"):
	# Will print out the entire matrix if necessary
	#np.set_printoptions(threshold=np.nan)

	tup = create_covariance_matrix(file = "/Users/ameyaacharya/Documents/Projects/Company Projects/Code/company-projects-matcher/data/survey_responses_altered.csv")
	unprocessed_data = tup[0]
	processed_data = tup[1]
	covariance_matrix = tup[2]

	sq_cov = sqrt_covariance_matrix(covariance_matrix)
	inv_sq_cov = inverse_matrix(sq_cov)
	#print inv_sq_cov

	d = processed_data[1]
	e = processed_data[36]
	#f = processed_data[32]
	print "d " + str(d)
	print "e " + str(e)
	#print "f" + str(f)
	print "(d, d)",
	print do_mahal_distance(d, d, inv_sq_cov, verbose = True)
	print "(d, e)",
	print do_mahal_distance(d, e, inv_sq_cov, verbose = True)

	#do_all_distances_data(processed_data, inv_sq_cov, unprocessed_data, verbose = True)

	

	#print "Square root of covariance matrix is: "
	#print sq_cov

	#print "Eigenvalues are: "
	#print linalg.eig(cov)

	# SANITY CHECKS for matrix square root
	#print "Eigenvalues of square root are:"
	#print linalg.eig(sq_cov)

	# STUPID NP.MULTIPLY WAS GIVING ME THE WRONG ANSWERS
	#c = np.dot(sq_cov, sq_cov)
	#print "Covariance matrix is: "
	#print covariance_matrix
	#print "Sqrt multiplied by itself:"
	#print c
	#print "Covariance matrix minus sqrt*sqrt:"
	#print covariance_matrix - c
	#print (c == covariance_matrix)
	#inverse_matrix(sq_cov)




