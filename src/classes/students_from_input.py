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
		rankings = student[5:15]

		scaled_coding_ability = scaled_coding_abilities[i]
		scaled_num_yrs_work_exp = scaled_yrs_work_experience[i]

		a = Student("Test", ID, degree_pursuing, cs_ug, coding_ability, num_yrs_work_exp, rankings)

		if (normalize):
			a = Student("Test", ID, degree_pursuing, cs_ug, scaled_coding_ability, scaled_num_yrs_work_exp, rankings, True)

		students_lst.append(a)

	# TODO: Fix this error (team size must be 4 or 5.)
	# t = Team(students_lst)
	# Team.print_team(t)

	
	#p = Project(1300, 2, 3)
	# # Test 1
	# print p.ID
	# print p.num_MEngs
	# print p.num_MBAs
	# print "p has " + str(p.remaining_MEng_spots) + " MEng spots remaining."
	# p.add_student_to_MEngs(students_lst[0])
	# print "After add, p has " + str(p.remaining_MEng_spots) + " MEng spots remaining."
	# print [s.get_student_properties() for s in p.MEng_list]

	# #p.add_student_to_MEngs(students_lst[0])
	# p.add_student_to_MEngs(students_lst[1])
	# p.add_student_to_MEngs(students_lst[3])
	# print [s.get_student_properties() for s in p.MEng_list]
	# print len(p.MEng_list)

	# Test 2

	# print p.is_empty()

	# for student in students_lst:
	# 	print "Student " + str(student.ID) + "'s type is " + str(student.degree_pursuing)
	# 	p.add_student(student)
	# 	print "Adding student to project"
	# 	print p.is_empty()

	# print p.MEng_list
	# print p.MBA_list

	# Test 3
	# p.add_team(t)
	
	projects = generate_all_projects()
	IDs = [p.ID for p in projects]
	print IDs
	greedy_match(students_lst, projects)

	for p in projects:
		p.print_project_members()
	
# NOTE: this exact code is duplicated in student.py. If you make changes here, change there as well.
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

# Scales based on range between -1 and 1.
def scale_inputs_based_on_range(lst):
	b = lst.max() - lst.min()
	if (b == 0):
		raise CompError("In normalizing our quantitative variables, all values are the same.")

	a = lst - lst.mean()

	# print (lst - lst.mean()) / (lst.max() - lst.min())
	normalized = a / b
	return normalized

# Scales between -1 and 1, with mean 0 and variance 1.
def calc_z_score(lst):
	m = lst.mean()
	sd = np.std(lst)
	return (lst - m) / sd

def generate_all_projects(num_MBAs = 2, num_MEngs = 2):
	projects_lst = []
	for ID in classes.vals_valid_projects:
		p = Project(ID, num_MBAs, num_MEngs)
		projects_lst.append(p)
	return projects_lst

def get_project_from_ID(ID, projects):
	matching_ID_lst = filter(lambda x: x.ID == ID, projects)
	if (len(matching_ID_lst) == 0):
		error = "ID " + str(ID) + " does not match to a valid project."
		raise FieldError(error)
	elif (len(matching_ID_lst) > 1):
		error = "There is more than one matching project. Problem!"
		raise FieldError(error)
	
	# Otherwise, there is one element in the list and it matches our desired ID.
	else:
		return matching_ID_lst[0]

def greedy_match(students_lst, projects):
	while(len(students_lst) > 0):
		print "Students list is " + str([s.get_student_properties() for s in students_lst])
		r = teams.random_index(len(students_lst))
		print "Current index is: " + str(r)
		cur_student = students_lst[r]
		print "Student " + str(cur_student.ID) + "'s list is ",
		print cur_student.project_rankings

		# Current spot in the student's ranking
		cur_spot = 0
		matched = False

		while (not(matched)):
			ranks = cur_student.project_rankings
			if (cur_spot >= len(ranks)):
				error = "Student " + str(cur_student.ID) + " could not match to any of its desired projects."
				raise CompError(error)
			cur_spot_proj_ID = ranks[cur_spot]
			print "cur_spot_proj_ID is " + str(cur_spot_proj_ID)
			top_project = get_project_from_ID(cur_spot_proj_ID, projects)

			matched = top_project.add_student(cur_student)
			print "Matched is " + str(matched)
			if (not(matched)):
				cur_spot += 1
			else:
				students_lst.pop(r)	

if __name__ == "__main__":
	read_input("new_name.csv")



