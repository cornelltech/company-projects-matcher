import numpy as np 
import pandas as pd 

import classes
import random_teams
import all_pairs_sorted
import greedy_student_and_fix
from classes import Student
from classes import Team
from classes import Project
from classes import CompError
from classes import FieldError

student_ids = []

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

def create_feasible_projects(students):
	return all_pairs_sorted.remove_infeasible_projects(students)

def match_with_first_choice(students, projects):
	return greedy_student_and_fix.match_with_first_choice(students, projects)



# create all projects

if __name__ == "__main__":
	students = create_students_from_input("tests.csv")
	all_projects = all_pairs_sorted.generate_all_projects()
	#feasible_projects = create_feasible_projects(students)
	first_choice_matches = match_with_first_choice(students, all_projects)
	#print [names_projects[p.ID] for p in create_feasible_projects(students)]


