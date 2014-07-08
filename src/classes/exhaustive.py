import numpy as np 
import pandas as pd 

import classes
import teams
from classes import Student
from classes import Team
from classes import Project
from classes import CompError
from classes import FieldError

student_ids = []

def normalize_bet_zero_and_one(lst):
	lst_max = lst.max()
	lst_min = lst.min()
	den = lst_max - lst_min
	num = [elm - lst_min for elm in lst]
	# TODO: get rid of this stupid error.
	if (den == 0):
		raise CompError("In normalizing our quantitative variables, all values are the same.")
	final = [(elm * 1.0) / den for elm in num]
	return final

def generate_all_projects(num_MBAs = 2, num_MEngs = 2):
	projects_lst = []
	for ID in classes.vals_valid_projects:
		p = Project(ID, num_MBAs, num_MEngs)
		projects_lst.append(p)
	return projects_lst

def exhaustive(projects, students):
	insufficient_IDs = []
	for p in projects:
		matched = filter(lambda x: p.ID in x.project_rankings, students)
		print "For project " + str(p.ID) + ":"
		print [s.ID for s in matched]
		MBAs_ranked = [s for s in matched if s.degree_pursuing == 0]
		MEngs_ranked = [s for s in matched if s.degree_pursuing == 1]
		print [s.ID for s in MBAs_ranked]
		print [s.ID for s in MEngs_ranked]

	 	if (len(MBAs_ranked) < 2 or len(MEngs_ranked) < 2):
	 		print "NOT ENOUGH MBAS OR MENGS"
	 		insufficient_IDs.append(p.ID)

	print len(insufficient_IDs)
	good_projects = filter(lambda p: not(p.ID in insufficient_IDs), projects)
	print [p.ID for p in good_projects]










































def read_input(file, normalize=True):
	data = pd.read_csv(file)
	data_array = np.array(data)
	shape = data_array.shape
	num_rows = shape[0]

	# Normalize our numerical variables to lie between 0 and 1.
	all_coding_abilities = data_array[:,3]
	all_work_experience = data_array[:,4]

	# TODO: instead of normalizing, should just scale it out of 1.
	# Normalization is too dependent on the values it's passed in with.
	scaled_coding_abilities = normalize_bet_zero_and_one(all_coding_abilities)
	scaled_yrs_work_experience = normalize_bet_zero_and_one(all_work_experience)
	
	students_lst = []

	# Extract rows
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

		scaled_coding_ability = scaled_coding_abilities[i]
		scaled_num_yrs_work_exp = scaled_yrs_work_experience[i]

		a = Student("Test", ID, degree_pursuing, cs_ug, coding_ability, num_yrs_work_exp, rankings)

		if (normalize):
			a = Student("Test", ID, degree_pursuing, cs_ug, scaled_coding_ability, scaled_num_yrs_work_exp, rankings, True)

		students_lst.append(a)

	projects = generate_all_projects()

	for p in projects:
		p.print_student_IDs()

	exhaustive(projects, students_lst)

if (__name__ == "__main__"):
		read_input("tests.csv")