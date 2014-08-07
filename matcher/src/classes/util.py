import random

import classes
from classes import Project
from classes import FieldError
from classes import CompError
from classes import Student
import pandas as pd
import numpy as np
import ConfigParser

student_ids = []

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

# Functions for randomness
def random_index(lst_length):
	'''
		Generate a random index for a list of length lst_length.
		Handles the case that the list length is 1, which can be
		problematic if using random.randint.
		Fails on empty lists.

		Parameters:
		-----------
		lst_length: length of the list (int).

		Returns:
		--------
		r: a random index in the range [0, lst_length - 1] (int).

	'''
	if (lst_length == 0):
		raise FunctionError("List has length of 0.")
	elif (lst_length == 1):
		r = 0
	else:
		r = random.randint(0, lst_length - 1)
	return r

def random_project(projects, already_picked, reuse, verbose = False):
	'''
		Pick a random project from the list of projects. If reuse = False,
		then we will pick a project that is not in already_picked.

		Parameters:
		-----------
		projects: the list of projects to choose from (Project list).

		already_picked: the projects that have already been assigned students (Project list).

		reuse: if False, then we would like to pick a project not included in already_picked (boolean).

		verbose: print updates.

		Returns:
		--------
		project: a project.

	'''
	rand_index = random_index(len(projects))
	if (verbose):
		print "Length of this project is " + str(len(projects[rand_index].students))
	if (not (reuse)):
		project_to_return = projects[rand_index]
		while (project_to_return in already_picked):
			rand_index = random_index(len(projects))
			project_to_return = projects[rand_index]
	
	return projects[rand_index]

def random_student(project):
	'''
		Picks a random student from a project.
		Fails on projects with no students.

		Parameters:
		-----------
		project: the project to pick a student from (Project).

		Returns:
		--------
		student: a student on this project (Student).

	'''
	rand_index = random_index(len(project.students))
	return project.students[rand_index]

def random_student_lst(student_lst):
	'''
		Picks a random student from a list of students.
		Fails on an empty list.

		Parameters:
		-----------
		student_lst: a list of students (Student list).

		Returns:
		--------
		student: a student in the list (Student).
	'''
	rand_index = random_index(len(student_lst))
	return student_lst[rand_index]

def random_two_choice():
	'''	
		Picks either 0 or 1, randomly.

		Returns
		-------
		number: either 0 or 1 (int).
	'''
	non_int = random.random()
	if (non_int > 0.5):
		return 1
	else:
		return 0

def generate_all_projects():
	'''
		Creates a project for every ID in classes.valid_projects.
		Takes the values for number of MBAs per team and number of
		MEngs per team from config.txt.

		Returns:
		--------
		projects_lst: a list of projects, on a one-to-one correspondence
		with the IDs in classes.valid_projects. 

	'''

	configParser = ConfigParser.ConfigParser()
	configFilePath = r'config.txt'
	configParser.read(configFilePath)

	num_MBAs = configParser.getint('valid_values', 'num_MBAs')
	num_MEngs = configParser.getint('valid_values', 'num_MEngs')
	projects_lst = []
	for ID in classes.vals_valid_projects:
		p = Project(ID, num_MBAs, num_MEngs)
		projects_lst.append(p)
	return projects_lst

def get_student_from_ID(ID, students):
	'''
		Given a student ID and a list of students, returns the
		Student object associated with the given ID.

		Parameters:
		-----------
		ID: ID for the student to search for (int).
		students: list of students (Student list).

		Returns:
		--------
		student: object whose ID is ID (Student).
	'''
	matching_ID_lst = filter(lambda x: x.ID == ID, students)
	# No matching IDs
	if (len(matching_ID_lst) == 0):
		error = "ID " + str(ID) + " does not match to a valid project."
		raise FieldError(error)
	# Multiple matching IDs
	elif (len(matching_ID_lst) > 1):
		error = "There is more than one matching project. Problem!"
		raise FieldError(error)
	# Otherwise, there is one element in the list and it matches our desired ID.
	else:
		return matching_ID_lst[0]


def get_project_from_ID(ID, projects):
	'''
		Given a project ID and a list of projects, returns the
		Project object associated with the given ID.

		Parameters:
		-----------
		ID: ID for the project to search for (int).
		projects: list of projects (Project list).

		Returns:
		--------
		project: object whose ID is ID (Project).
	'''
	matching_ID_lst = filter(lambda x: x.ID == ID, projects)
	# No matching IDs
	if (len(matching_ID_lst) == 0):
		error = "ID " + str(ID) + " does not match to a valid project."
		raise FieldError(error)
	# Multiple matching IDs
	elif (len(matching_ID_lst) > 1):
		error = "There is more than one matching project. Problem!"
		raise FieldError(error)
	# Otherwise, there is one element in the list and it matches our desired ID.
	else:
		return matching_ID_lst[0]

# Filter out projects with insufficient rankings to get matched.
# Returns a list of projects which passed the test.
def create_feasible_projects(students, projects, verbose = True):
	'''
		Filters our the projects with insufficient rankings to get matched.

	'''
	insufficient_IDs = []
	for p in projects:
		matched = filter(lambda s: p.ID in s.project_rankings, students)
		if (verbose):
			print "For project " + str(p.ID) + ":"
			print [s.ID for s in matched]
		MBAs_ranked = [s for s in matched if s.degree_pursuing == "MBA" or s.degree_pursuing == 0]
		MEngs_ranked = [s for s in matched if s.degree_pursuing == "MEng" or s.degree_pursuing == 1]
		if (verbose):
			print "MBAs" + str([s.ID for s in MBAs_ranked])
			print "MEngs" + str([s.ID for s in MEngs_ranked])
			print "p.num_MBAs is " + str(p.num_MBAs)
			print "p.num_MEngs is " + str(p.num_MEngs)
			print str(len(MBAs_ranked)) + " MBAs ranked this project."
			print str(len(MEngs_ranked)) + " MEngs ranked this project."
			print str(len(MBAs_ranked)) + " < " + str(p.num_MBAs) + ":",
			print str(len(MEngs_ranked)) + " < " + str(p.num_MEngs) + ":",
			print "The comparison that we are checking: " + str((len(MBAs_ranked) < p.num_MBAs) or (len(MEngs_ranked) < p.num_MEngs))
	 
	 	if ((len(MBAs_ranked) < p.num_MBAs) or (len(MEngs_ranked) < p.num_MEngs)):
	 		if (verbose):
	 			string = "Not enough MBAs or MEngs ranked project "
	 			string += str(p.ID)
	 			string += " for it to be included."
	 			print string
	 		insufficient_IDs.append(p.ID)

	projects = filter(lambda p: not(p.ID in insufficient_IDs), projects)
	return projects

def better(students, projects):
	def is_insufficient(p):
		# All of the students who ranked this project:
		matched = filter(lambda s: p.ID in s.project_rankings, students)
		# All of the MBAs and MEngs who ranked this project
		MBAs_ranked = [s for s in matched if s.degree_pursuing == "MBA" or s.degree_pursuing == 0]
		MEngs_ranked = [s for s in matched if s.degree_pursuing == "MEng" or s.degree_pursuing == 1]
		if (len(MBAs_ranked) < p.num_MBAs):
			return True
		elif (len(MEngs_ranked) < p.num_MEngs):
			return True
		else:
			return False
	return filter(lambda p: not(is_insufficient(p)), projects)
#	pass

# For a specific project p, get the students' overall interest in the project.
# Higher interest means that more students ranked it highly on their lists.
# The "interest" variable determines if how high a student ranked the project on their
# list counts extra towards the ranking, or if it's just how many students ranked it.
# Currently set the default so that its just how many students ranked it.
def get_project_interest_from_rankings(p, students, verbose = False):

	# Check which students ranked this project.
	matched = filter(lambda s: p.ID in s.project_rankings, students)

	if (verbose):
		print "The following students ranked project " + str(p.ID) + ":"
		print [s.ID for s in matched]

	# For each student, get their interest in this project.
	# Add this to the sum of the overall interest.
	overall_interest = 0
	for s in matched:
		rank = s.get_ranking(p.ID)
		interest = s.get_interest_from_ranking(rank)
 		overall_interest = overall_interest + interest
	return overall_interest

# Get the number of students who ranked this project in their top 10.
def get_num_ranked(p, students):
	matched = filter(lambda s: p.ID in s.project_rankings, students)
	return len(matched)

# Sort projects by highest demand to lowest demand.
def sort_projects_by_demand(students, projects, tup = False):
	def liking (p):
		return get_num_ranked(p, students)
	projects.sort(key = liking, reverse = True)
	if (tup):
		return [liking(p) for p in projects]
	else:
		return projects


def are_unique(l1, l2):
	''' 
		Checks if two given lists are unique.

		Parameters
		----------
		l1, l2: two arbitrary lists.

		Returns
		-------
		are_unique: a boolean value indicating if these lists are unique.

	'''
	return (set(l1).intersection(set(l2)) == set([]))

def create_students_from_input(file):
	data = pd.read_csv(file)
	data_array = np.array(data)
	shape = data_array.shape
	num_rows = shape[0]

	students_lst = []

	# Extract rows and create students
	for i in range(0, num_rows):
		student = data_array[i,:]
		ID 	= student[0]
		if (ID in student_ids):
			raise CompError("Student IDs must be unique.")
		student_ids.append(ID)
		
		degree_pursuing = student[1]
		cs_ug = student[2]
		coding_ability = student[3]
		num_yrs_work_exp = student[4]

		# Only take the desired number of project rankings that we want.
		rankings = student[5:(5 + classes.number_project_rankings)]
		name = student[10]

		a = Student(name, ID, degree_pursuing, cs_ug, coding_ability, num_yrs_work_exp, rankings)
		students_lst.append(a)

	return students_lst

# num_MBAs and num_MEngs are the numbers required per team.
def input_checks(students, projects, num_MBAs, num_MEngs, sorted = False):
	if (len(projects) == 0):
		raise FieldError ("Cannot make an initial solution with an empty project list.")

	elif (len(students) == 0):
		raise FieldError ("Cannot make an initial solution with an empty student list.")

	team_size = num_MBAs + num_MEngs

	MBAs = filter(lambda student: student.degree_pursuing == 0 or student.degree_pursuing == "MBA", students)
	MEngs = filter(lambda student: student.degree_pursuing == 1 or student.degree_pursuing == "MEng", students)

	# Make sure that there are no overlapping student IDs.
	MBA_IDs = [s.ID for s in MBAs]
	MEng_IDs = [s.ID for s in MEngs]

	if (not (are_unique(MBA_IDs, MEng_IDs))):
		raise FieldError('Student ID lists must not overlap.')

	# Make sure that team size is not zero.
	if (team_size == 0):
		raise FieldError('Team size cannot be 0.')

	# Number of teams is not actually just the total students divided by the team size.
	# It's the smaller of total mbas and total mbas divided by num mbas or num mengs.

	if (len(MBAs) < len(MEngs)):
	 	smaller = MBAs
	 	num_req_per_team = num_MBAs
	else:
	 	smaller = MEngs
	 	num_req_per_team = num_MEngs
	
	num_teams = len(smaller)/num_req_per_team




	# num_MBAs_needed = num_MBAs * num_teams
	# num_MEngs_needed = num_MEngs * num_teams

	# if (len(MBAs) < num_MBAs_needed):
	# 	raise FieldError ("Not enough MBA students to produce teams of the desired makeup.")
	# elif (len(MEngs) < num_MEngs_needed):
	# 	raise FieldError ("Not enough MEng students to produce teams of the desired makeup.")

	# If team size is too big for input.
	if (num_teams == 0):
		raise FieldError ("Team size is too large for given input.")

	# If none of these errors are raised, then the input is fine.
	else:
		pass



