#import teams
import numpy as np
from scipy import linalg
from scipy import spatial
import clustering

default_file = "/Users/ameyaacharya/Documents/Projects/Company Projects/Code/company-projects-matcher/matcher/src/classes/eighty_students.csv"

class DistanceError(Exception):
	def __init__(self, value):
		self.val = value
	def __str__(self):
		return repr(self.val)

def is_positive_semidefinite(cov_matrix, verbose = False):
	'''
		Calculates all eigenvalues of the matrix
		If there are negative eigenvalues, returns false.
	'''
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

def create_covariance_matrix(use_file, students, file = default_file, verbose = False):
	'''
		Reads the data from the file (if we need to fix how the data is read, change clustering init.)
		Preprocesses data with one hot encoding (changes categorical variables into numerical.)
		Fixes matrix if it's not positive semidefinite (adds a small version of the identity.)
		Returns (data, covariance matrix.)
	'''
	if (use_file):
		data_array_tup = clustering.__init__(file)
	# Create covariance matrix from students themselves.
	else:
		multi_array = []
		for student in students:
 			# add their attributes to multi array
 			attributes = student.get_numerical_student_properties()
 			multi_array.append(attributes)
 		IDs = [s.ID for s in students]
 		data_array = np.array(multi_array)
 		if (verbose):
	 		print "Multi array is " + str(data_array)
 		data_array_tup = (data_array, IDs)

	data_array = data_array_tup[0]

	data_array = data_array_tup[0]
	one_hot_data_preprocessed_tup = clustering.do_preprocessing(data_array_tup)

	one_hot_data_preprocessed = one_hot_data_preprocessed_tup[0]
	dict_key_vals = one_hot_data_preprocessed_tup[1]
	
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

	return (data_array, one_hot_data_preprocessed, covariance_matrix, dict_key_vals)

def sqrt_matrix(matrix):
	'''
		Calcuate matrix square root using scipy linalg.

	'''	
 	matrix_square_root = linalg.sqrtm(matrix)
	return matrix_square_root

def inverse_matrix(matrix, use_pseudo_inv = True, verbose = False):
	'''
		Can calculate real matrix inverse or pseudoinverse.

	'''
	# Calculate real matrix inverse.
	if (not(use_pseudo_inv)):
	 	cov_inverse = linalg.inv(matrix)
	 	if (verbose):
	 		print "(Real) inverse of the input matrix is: "
	# Calculate the matrix pseudoinverse.
	else:
	 	cov_inverse = np.linalg.pinv(matrix)
	 	if (verbose):
			print "(Pseudo) inverse of the input matrix is: "
	return cov_inverse

def do_python_distance_data(student_one, student_two, inv_cov_mat):
	'''
		NOTE: this takes in the inverse of the cov mat, not the inverse sq cov mat.

	'''
	return spatial.distance.mahalanobis(student_one, student_two, inv_cov_mat)

def create_inv_cov_mat_from_data(use_file, students, file = default_file):
	quadruple = create_covariance_matrix(use_file, students, file)
	cov_mat = quadruple[2]
	dict_key_vals = quadruple[3]
	inv_cov_mat = inverse_matrix(cov_mat)
	return (inv_cov_mat, dict_key_vals)

def do_all_python_distances_data(data, inv_cov_mat, unprocessed_data, start = 0, verbose = True):
	'''
		NOTE: this takes in the inverse of the cov mat, not the inverse sq cov mat.

	'''
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

if (__name__ == "__main__"):
	# Will print out the entire matrix if necessary
	np.set_printoptions(threshold=np.nan)

	tup = create_covariance_matrix()
	unprocessed_data = tup[0]
	processed_data = tup[1]
	covariance_matrix = tup[2]

	sq_cov = sqrt_matrix(covariance_matrix)
	inv_cov = inverse_matrix(covariance_matrix)
	inv_sq_cov = inverse_matrix(sq_cov)