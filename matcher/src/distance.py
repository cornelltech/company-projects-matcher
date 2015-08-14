#import teams
import numpy as np
from scipy import linalg
from scipy import spatial
import clustering

class DistanceError(Exception):
	def __init__(self, value):
		self.val = value
	def __str__(self):
		return repr(self.val)

def is_positive_semidefinite(cov_matrix, verbose = False):
	'''
		Checks if the input matrix is positive semidefinite.
		(If there are negative eigenvalues of the matrix, returns false.)

		Parameters
		----------
		cov_matrix: the covariance matrix of the given data (2d numpy array of floats).

		Returns
		-------
		is_positive_semidefinite: indicates if the given matrix is positive
		                          semidefinite (bool).

	'''
	(eigenvalues, eigenvectors) = linalg.eig(cov_matrix)
	res = []
	for e in eigenvalues:
 		if (e < 0):
	 		res.append(e)
	if (verbose):
		print "Negative eigenvalues of covariance matrix are:"
		print res
	return len(res) == 0

def create_covariance_matrix(use_file, students, file, verbose = False):
	'''
		Reads the data from the file (if we need to fix how the data is read, change clustering init.)
		Preprocesses data with one hot encoding (changes categorical variables into numerical.)
		Fixes matrix if it's not positive semidefinite (adds a small version of the identity.)
		Returns (data, covariance matrix.)

	    Parameters
	    ----------
	    use_file: indicates if we want to use the input from the file (bool).
	    students: students to include in calculation (Student list).
	    file: file to use (if use_file = True).

	    Returns
	    --------
	    covariance_matrix: the covariance matrix of the data (either from file or students).
	
	'''
	if (use_file):
		data_array_tup = clustering.__init__(file)
	# Create covariance matrix from students themselves.
	else:
		multi_array = []
		for student in students:
 			attributes = student.get_numerical_student_properties()
 			multi_array.append(attributes)
 		IDs = [s.ID for s in students]
 		data_array = np.array(multi_array)
 		if (verbose):
	 		print "Multi array is " + str(data_array)
 		data_array_tup = (data_array, IDs)

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

		Parameters
		----------
		matrix: matrix (numpy 2d array of floats).

		Returns
		-------
		sqrt_matrix: the matrix square root of the input matrix.

	'''	
 	matrix_square_root = linalg.sqrtm(matrix)
	return matrix_square_root

def inverse_matrix(matrix, use_pseudo_inv = True, verbose = False):
	'''
		Calculates matrix inverse -- either true inverse or pseudoinverse.

		Parameters
		----------
		matrix: matrix (numpy 2d array of floats).
		use_pseudo_inv: indicates if we want to calculate the pseudoinverse (bool).
		                If use_pseudo_inv = False, then we calculate the true inverse.
		verbose: indicates whether we want to print updates.

		Returns
		-------
		inverse_matrix: the (pseudo or real) inverse of the input matrix
		                (numpy 2d array of floats).

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
		Parameters
		----------
		student_one: data for first student (must be all numerical) (numpy 1D array).
		student_two: data for second student (must be all numerical) (numpy 1D array).
		inv_cov_mat: the inverse covariance matrix of the given data
		             (2d numpy array of floats).

		Returns
		-------
		distance: the distance between student_one and student_two (float).

	'''
	return spatial.distance.mahalanobis(student_one, student_two, inv_cov_mat)

def create_inv_cov_mat_from_data(use_file, students, file_name):
	'''
		Creates inverse covariance matrix from the input file.
	'''
	quadruple = create_covariance_matrix(use_file, students, file_name)
	cov_mat = quadruple[2]
	dict_key_vals = quadruple[3]
	inv_cov_mat = inverse_matrix(cov_mat)
	return (inv_cov_mat, dict_key_vals)
