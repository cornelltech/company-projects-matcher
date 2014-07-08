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
	names_projects = {3705: 'Goldman Sachs',
				2990: 'American Express',
				4225: 'Google',
				2860: 'Facebook',
				2145: '500px',
				1820: 'FlightCar',
				3055: 'Flatiron',
				1040: 'Realize',
				1950: 'Shapeways',
				1625: 'charity:water',
				3445: 'Bonobos',
				3900: 'Bloomberg'}

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
		name = student[10]

		scaled_coding_ability = scaled_coding_abilities[i]
		scaled_num_yrs_work_exp = scaled_yrs_work_experience[i]

		a = Student(name, ID, degree_pursuing, cs_ug, coding_ability, num_yrs_work_exp, rankings)

		if (normalize):
			a = Student(name, ID, degree_pursuing, cs_ug, scaled_coding_ability, scaled_num_yrs_work_exp, rankings, True)

		students_lst.append(a)

	print "Our student IDs are: "
	print "---------------------"
	for s in students_lst:
		print str(s.ID) + ": " + s.name
	

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

	simple_greedy_match(students_lst, projects)
	rearrange_spots(students_lst, projects)

	print ""
	print "After matching, we have:"
	print "---------------------"
	for p in projects:
		students = p.MBA_list + p.MEng_list
		if (len(students) > 0 and p.ID in names_projects.keys()):
			#print str(names_projects[p.ID]) + ":"
			p.print_student_IDs(num=False, name = True, dct = names_projects)
			print ""



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
	


	# def do():
	# 	filterable = []
	# 	for p in projects:
	# 		rem_spots = p.remaining_MEng_spots + p.remaining_MBA_spots
	# 		if (rem_spots > 0 and not (rem_spots == 4)):
	# 			filterable.append(p)
	# 	while (len(filterable) > 0):
	# 		rearrange_spots(students_lst, projects)

	# do()

	# Test 4
	# for p in projects:
	# 	students = p.MBA_list + p.MEng_list
	# 	if (not(len(students) == 0)):
	# 		for s in students:
	# 			rank = s.get_ranking(p.ID)
	# 			print s.get_interest_from_ranking(rank)
		#student_list = p.MBA_list + p.MEng_list
		#print "Length of student list is " + str(len(student_list))

	# Test 5
	# for p in projects:
	# 	lst_one = p.MBA_list + p.MEng_list
	# 	if (len(lst_one) > 0):	
	# 		print lst_one
	# 	p.remove_student_from_project(2006650)
	# 	lst_two = p.MBA_list + p.MEng_list
	# 	if (len(lst_two) > 0 and not(len(lst_one) == len(lst_two))):	
	# 		print lst_two

	
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

def simple_greedy_match(students_lst, projects):
	while(len(students_lst) > 0):
		#print "Students list is " + str([s.ID for s in students_lst])
		r = teams.random_index(len(students_lst))
		cur_student = students_lst[r]
		#print "Current student is: " + str(cur_student.ID)
		#print "Student " + str(cur_student.ID) + "'s list is ",
		#print cur_student.project_rankings

		# Current spot in the student's ranking
		cur_spot = 0
		matched = False

		while (not(matched)):
			ranks = cur_student.project_rankings
			if (cur_spot >= len(ranks)):
				error = "Student " + str(cur_student.ID) + " could not match to any of its desired projects."
				raise CompError(error)
			cur_spot_proj_ID = ranks[cur_spot]
			#print "Current student's " + str(cur_spot) + " choice project is " + str(cur_spot_proj_ID)
			top_project = get_project_from_ID(cur_spot_proj_ID, projects)

			# print "Current student's type is: ",
			# if (cur_student.degree_pursuing == 0):
			# 	print "MBA"
			# else:
			# 	print "MEng"
			#print "Before add: choice project's members are",
			#top_project.print_project_members()

			matched = top_project.add_student(cur_student)
			#print "After add: choice project's members are",
			#top_project.print_project_members()

			#print "Matched is " + str(matched)
			if (not(matched)):
				cur_spot += 1
			else:
				students_lst.pop(r)
	return projects

def rearrange_spots(students_lst, projects):

	def has_empty_spot(x):
		return ((x.remaining_MEng_spots + x.remaining_MBA_spots) > 0)

	#print "In rearrange spots:"
	unfilled_projects = []
	unfilled_students = []
	for x in projects:
		num_remaining_spots = x.remaining_MEng_spots + x.remaining_MBA_spots
		if (num_remaining_spots > 0):
			unfilled_projects.append((num_remaining_spots, x))
	for tup in unfilled_projects:
		proj = tup[1]
		student_list = proj.MBA_list + proj.MEng_list
		for s in student_list:
			unfilled_students.append(s)

	# Sort by least spots left first.
	projects.sort(key = lambda x: x.remaining_MEng_spots + x.remaining_MBA_spots)

	# print "Before matching the extras:"
	# for p in projects:
	# 	p.print_student_IDs()

	# print "Unfilled students is:"
	# print unfilled_students

	for proj in projects:
		if (has_empty_spot(proj)):
			students = proj.MBA_list + proj.MEng_list
			# The students who are already on the project
			existing_students_IDs = [s.ID for s in students]
			ranked_students = []
			for student in unfilled_students:
				# Find the students not already on the team who ranked this project
				if (proj.ID in student.project_rankings and student.ID not in existing_students_IDs):
					ranked_students.append((student.get_ranking(proj.ID), student))
			ranked_students.sort()
			cur_index = 0
			while (proj.has_remaining_MBA_spots() or proj.has_remaining_MEng_spots()):
				if (cur_index >= len(ranked_students)):
					break
					# TODO: do something above
				else:
					cur_student = (ranked_students[cur_index])[1]
					if (proj.add_student(cur_student)):
						unfilled_students.remove(cur_student)
					cur_index += 1


	# print "After matching the extras:"
	# for p in projects:
	# 	p.print_student_IDs()

	# print "Unfilled students is now:"
	# print unfilled_students


	
	# for proj in unfilled_projects:
	# 	students = proj.MBA_list + proj.MEng_list
	# 	print [s.ID for s in students]


if __name__ == "__main__":
	#read_input("new_name.csv")
	read_input("tests.csv")



