#import teams
import numpy as np
from scipy import linalg
from scipy import spatial
import clustering
import math

default_file = "/Users/ameyaacharya/Documents/Projects/Company Projects/Code/company-projects-matcher/data_analysis/data/new_new_survey_responses.csv"

class DistanceError(Exception):
	def __init__(self, value):
		self.val = value
	def __str__(self):
		return repr(self.val)

def is_positive_semidefinite(cov_matrix, verbose = False):
#Calculates all eigenvalues of the matrix
# If there are negative eigenvalues, returns false.
	(eigenvalues, eigenvectors) = linalg.eig(cov_matrix)
	res = []
	#print eigenvalues.shape
	for e in eigenvalues:
		#print e
 		if (e < 0):
	 		res.append(e)
	if (verbose):
		print "Negative eigenvalues of covariance matrix are:"
		print res
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
		raise DistanceError("Covariance matrix is not a square matrix.")

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
				raise DistanceError("Fixed covariance matrix is not positive semidefinite.")
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
def calc_numerical_difference(x, y, verbose = False):
	if (verbose):
		print "In calc numer diff:"
		print "X is " + str(x)
		print "Y is " + str(y)
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
	
	# TODO: not sure if we even want to use this.
	# obs_zero = one_hot_data_preprocessed[0]
	# obs_one = one_hot_data_preprocessed[1]
	# print "Mahal distance is " + str(spatial.distance.mahalanobis(obs_zero, obs_one, cov_inverse))


	if (fixed_with_zeros):
	# Reset these values in copies the original vectors to 0
	# so they don't affect the dot products.

		# Copy the original vectors over, so that we don't modify them.
		# (When we loop through all of the data, we'll have to reuse it.)
		copy_s_one = s_one_properties.copy()
		copy_s_two = s_two_properties.copy()

		# Extract the values of interest
		ca_one = copy_s_one[10]
		ca_two = copy_s_two[10]
		work_one = copy_s_one[11]
		work_two = copy_s_two[11]
		
		copy_s_one[10] = 0
		copy_s_two[10] = 0
		copy_s_one[11] = 0
		copy_s_two[11] = 0

		# Calculate numerical differences using above function
		coding_diff = calc_numerical_difference(ca_one, ca_two)
		work_diff = calc_numerical_difference(work_one, work_two)

		# Dot the copied vectors
		a = np.dot(copy_s_one, inv_sq_cov_mat)
		res = np.dot(a, copy_s_two)

		if (verbose):
			print "Dotted value: " + str(res)
			print "Calculated values:",
			print coding_diff,
			print work_diff

		# Add the calculated differences.
		new_res = res + coding_diff + work_diff
		if (verbose):
			print "New res is " + str(new_res)
		return new_res

	else:

		a = np.dot(s_one_properties, inv_sq_cov_mat)
		res = np.dot(a, s_two_properties)

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

# This takes in the inverse of the cov mat, not the inverse sq cov mat.
def do_python_distance_data(student_one, student_two, inv_cov_mat):
	return spatial.distance.mahalanobis(student_one, student_two, inv_cov_mat)

# This takes in the inverse of the cov mat, not the inverse sq cov mat.
# TODO: make this actually return the result.
def do_all_python_distances_data(data, inv_cov_mat, unprocessed_data, start = 0, verbose = True):
	i = start
	j = start
	res = []
	for student_one in data:
		for student_two in data:
			d = do_python_distance_data(student_one, student_two, inv_cov_mat)
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

	if (verbose):
		 for i in res:
		 	tup = i[0]
		 	first_student = tup[0]
			second_student = tup[1]

			lst_first_student = unprocessed_data[first_student]
			lst_second_student = unprocessed_data[second_student]

			print lst_first_student
			print lst_second_student

			for x in range(0, 4):
				if (not(lst_first_student[x] == lst_second_student[x])):
					print "Diff at " + str(x)

			print i[1]

	#return res

def subtract_distances(student_one, student_two):
	def categorical_differences(index):
		if (student_one[index] == student_two[index]):
			return 0
		else:
			return 4

	def numerical_differences(index):
		if (student_one[index] == student_two[index]):
			return 0
		else:
			diff = abs(student_one[index] - student_two[index])
			return diff

	# Declare result
	res = 0

	# UG major
	res += categorical_differences(0)

	# Coding ability
	res += numerical_differences(1)

	# Degree pursuing
	res += categorical_differences(2)

	# Work experience
	res += numerical_differences(3)

	return res



def do_all_subtracted_distances_data(data, unprocessed_data, start = 0, verbose = True):
	i = start
	j = start
	res = []
	for student_one in data:
		for student_two in data:
			d = subtract_distances(student_one, student_two)
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

	if (verbose):
		 for i in res:
		 	tup = i[0]
		 	first_student = tup[0]
			second_student = tup[1]

			lst_first_student = unprocessed_data[first_student]
			lst_second_student = unprocessed_data[second_student]

			print lst_first_student
			print lst_second_student

			for x in range(0, 4):
				if (not(lst_first_student[x] == lst_second_student[x])):
					print "Diff at " + str(x)
					pass

			#print i[1] - minimum
			print i[1]

	#return res

# Uses the function that I defined (do_mahal_distance).
def do_all_my_distances_data(data, inv_sq_cov_mat, unprocessed_data, start = 0, verbose = True):
	i = start
	j = start
	res = []
	for student_one in data:
		for student_two in data:
			d = do_mahal_distance(student_one, student_two, inv_sq_cov_mat, fixed_with_zeros = True)
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

	if (verbose):
		 for i in res:
		 	tup = i[0]
		 	first_student = tup[0]
			second_student = tup[1]

			lst_first_student = unprocessed_data[first_student]
			lst_second_student = unprocessed_data[second_student]

			print lst_first_student
			print lst_second_student

			for x in range(0, 4):
				if (not(lst_first_student[x] == lst_second_student[x])):
					print "Diff at " + str(x)
					pass

			#print i[1] - minimum
			print i[1]

	#return res

if (__name__ == "__main__"):
	# Will print out the entire matrix if necessary
	np.set_printoptions(threshold=np.nan)

	tup = create_covariance_matrix()
	unprocessed_data = tup[0]
	processed_data = tup[1]
	covariance_matrix = tup[2]

	sq_cov = sqrt_covariance_matrix(covariance_matrix)
	inv_cov = inverse_matrix(covariance_matrix)
	inv_sq_cov = inverse_matrix(sq_cov)

	# print "d unprocessed " + str(unprocessed_data[1])
	# print "d processed " + str(processed_data[1])

	# print "e unprocessed " + str(unprocessed_data[34])
	# print "e processed " + str(processed_data[34])


	#print "unprocessed_data " + str(unprocessed_data)
	#print "processed_data " + str(processed_data)
	#d_clustered = clustering.do_preprocessing(unprocessed_data[1])
	
	# d_u = unprocessed_data[11]
	# d_p = processed_data[11]
	# e = processed_data[18]
	# f = processed_data[15]
	# small_processed_data = (d_p, d_p, d_p)
	# small_unprocessed_data = (d_u, d_u, d_u)
	# print small_processed_data
	# print small_unprocessed_data
	#print "Before inputing to mahal distances " + str(small_data)
	# #f = processed_data[32]
	# print "d " + str(unprocessed_data[1])
	# print "e " + str(unprocessed_data[34])
	# #print "f" + str(f)
	#print "(d, d)",
	#print do_mahal_distance(d, d, inv_sq_cov)
	#print "(d, e)",
	#print do_mahal_distance(d, e, inv_sq_cov)

	# print "Small data is: " + str(small_data)

	# SMALL DATA: to test something
	#do_all_distances_data(small_processed_data, inv_sq_cov, small_unprocessed_data, verbose = True)

	# BIG DATA: for reals
	#do_all_python_distances_data(processed_data, inv_cov, unprocessed_data)
	#do_all_subtracted_distances_data(processed_data, unprocessed_data)


	#fst = [1, 2, 1, 3]
	#snd = [0, 4, 1, 1]
	fst = processed_data[2]
	snd = processed_data[4]
	print do_python_distance_data(fst, snd, inv_cov)


	#a = [1, 0, 0, 4]
	#b = [0, 3, 1, 4]
	#print subtract_distances(a, b)

	# Testing weighted interest
	#for i in range (1, 11):
		#print str(i) + ": " + str(weight_interest(i))
	

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




