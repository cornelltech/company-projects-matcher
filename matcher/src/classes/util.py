import random

class InputError(Exception):
	def __init__(self, value):
		self.val = value
	def __str__(self):
		return repr(self.val)

class FunctionError(Exception):
	def __init__(self, value):
		self.val = value
	def __str__(self):
		return repr(self.val)

# FUNCTIONS FOR RANDOMNESS

# TODO: Make this work for arbitrary number of student types. 
# 		Can apply these (functions that apply to two teams) apply to 
#		three or more teams by taking input in a list, and then
# 		using map.
# TODO: Make this work with more than one team size.

def random_index(lst_length):
	if (lst_length == 0):
		raise FunctionError("List has length of 0.")
	elif (lst_length == 1):
		r = 0
	else:
		r = random.randint(0, lst_length - 1)
	return r

# This method is used to perform the swap of the students. 
# Need to find a non-empty random project so that we can swap
# one of the students on the project. 
def random_project(projects, verbose = False):
	# Pick a random project
	rand_index = random_index(len(projects))
	# Ensures that the project that we pick is not empty
	if (verbose):
		print "Length of this project is " + str(len(projects[rand_index].students))
	#while (len(projects[rand_index].students) == 0):
	#	rand_index = random_index(len(projects))
	return projects[rand_index]

# From a project
def random_student(project):
	rand_index = random_index(len(project.students))
	return project.students[rand_index]

# From a list of students
def random_student_lst(student_lst):
	rand_index = random_index(len(student_lst))
	return student_lst[rand_index]


def random_two_choice():
	non_int = random.random()
	if (non_int > 0.5):
		return 1
	else:
		return 0