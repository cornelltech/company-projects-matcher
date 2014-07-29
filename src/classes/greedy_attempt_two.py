import numpy as np 
import pandas as pd 
import random

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

def initial_solution(students, projects):
	# The index of the ranking that we are currently looking at.
	ranking_spot = 0

	# The IDs of the projects whose students were already removed from unmatched_students.
	matched_projects = []
	# The IDs of the students were already removed from unmatched_students.
	matched_students = []

	while (ranking_spot < classes.number_project_rankings):
		#random.shuffle(unmatched_students)
		for student in students:
			print "Student number " + str(student.ID)
			if (not (student.ID in matched_students)):
				cur_project_ID = student.project_rankings[ranking_spot]
				cur_project = all_pairs_sorted.get_project_from_ID(cur_project_ID, projects)
				print "     Student not matched (" + str(student.ID) + ")"
				print "     Rank " + str(ranking_spot) + " is project " + str(cur_project_ID)
				
				# Try to add student to the project.
				successful_add = cur_project.add_student(student)
				if (successful_add):
					print "     Successful add of student " + str(student.ID) + " to project " + str(cur_project.ID)
					print "     Project " + str(cur_project.ID) + "'s student list is now: "
					print "     " + str([s.ID for s in cur_project.students])

				# If there were no spots available, add this student to the waiting list.
				else:
					print "     Not successful. Adding to waiting list"
					cur_project.add_waiting_student(student)

				# If the project is full and its students havent been 
				# removed yet, then remove it and its students.
				if (not (cur_project.has_remaining_spots())):
					print "     For project " + str(cur_project_ID) + ":"
					print "     Project " + str(cur_project_ID) + " has no more spots."
					
					if (not (cur_project.ID in matched_projects)):
						print "     The students on this project are: ",
						print [s.ID for s in cur_project.students]
						remove_students_from_projects(cur_project.students, projects, cur_project_ID)

						print "     Before remove: "
						print "          Unmatched students is:"
						print [s.ID for s in students if not (s.ID in matched_students)]
						print "          Cur project students is: "
						print [s.ID for s in cur_project.students]
						# Remove students from unmatched_students
						for student in cur_project.students:
							matched_students.append(student.ID)

						print "     After remove: "
						print "          Unmatched students is:"
						print [s.ID for s in students if not (s.ID in matched_students)]

						matched_projects.append(cur_project.ID)
					else:
						pass

		ranking_spot += 1

	for project in projects:
		pass
		#if (not(project.students == [])):
		#	print "For project " + str(project.ID) + ":"
		#	print [s.ID for s in project.students]

			# For all projects
			# If this student ID is on the project
				# Remove the student from that project
			# If this student ID is on the waiting list
				# Remove the student fromt that waiting list.

def remove_students_from_projects(students_to_remove, projects, ID):
	for project in projects:
		if (not (project.ID == ID)):
			for student in students_to_remove:
				if student in project.students:
					project.students.remove(student)
				if student in project.waiting_students:
					project.waiting_students.remove(student)

# create all projects

if __name__ == "__main__":
	students = create_students_from_input("tests.csv")
	all_projects = all_pairs_sorted.generate_all_projects()
	initial_solution(students, all_projects)
	#feasible_projects = create_feasible_projects(students)


