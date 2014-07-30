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

def create_feasible_projects(students, projects):
	return all_pairs_sorted.remove_infeasible_projects(students, projects)

def match_with_first_choice(students, projects):
	return greedy_student_and_fix.match_with_first_choice(students, projects)

def initial_solution(students, projects, verbose = True):
	feasible_projects = create_feasible_projects(students, projects)
	print "Feasible projects are:"
	print [f.ID for f in feasible_projects]

	# The index of the ranking that we are currently looking at.
	ranking_spot = 0

	# The IDs of the projects whose students were already removed from unmatched_students.
	matched_projects = []
	# The IDs of the students were already removed from unmatched_students.
	matched_students = []

	while (ranking_spot < classes.number_project_rankings):
		# TODO: change the order that students are selected.
		for student in students:
			if (verbose):
				print "Student number " + str(student.ID)
			if (not (student.ID in matched_students)):
				cur_project_ID = student.project_rankings[ranking_spot]
				try:
					cur_project = all_pairs_sorted.get_project_from_ID(cur_project_ID, feasible_projects)
					if (verbose):
						print "     Student not matched (" + str(student.ID) + ")"
						print "     Rank " + str(ranking_spot) + " is project " + str(cur_project_ID)
				
					# Try to add student to the project.
					successful_add = cur_project.add_student(student)
					if (successful_add and verbose):
						print "     Successful add of student " + str(student.ID) + " to project " + str(cur_project.ID)
						print "     Project " + str(cur_project.ID) + "'s student list is now: "
						print "     " + str([s.ID for s in cur_project.students])

					# If there were no spots available, add this student to the waiting list.
					else:
						if (verbose):
							print "     Not successful. Adding to waiting list"
						cur_project.add_waiting_student(student)

					# If the project is full and its students havent been 
					# removed yet, then remove it and its students.
					if (not (cur_project.has_remaining_spots())):
						if (verbose):
							print "     For project " + str(cur_project_ID) + ":"
							print "     Project " + str(cur_project_ID) + " has no more spots."
						
						if (not (cur_project.ID in matched_projects)):
							if (verbose):
								print "     The students on this project are: ",
								print [s.ID for s in cur_project.students]
							remove_students_from_projects(cur_project.students, feasible_projects, cur_project_ID)

							if (verbose):
								print "     Before remove: "
								print "          Unmatched students is:"
								print [s.ID for s in students if not (s.ID in matched_students)]
								print "          Cur project students is: "
								print [s.ID for s in cur_project.students]
							# Remove students from unmatched_students
							for student in cur_project.students:
								matched_students.append(student.ID)

							if (verbose):
								print "     After remove: "
								print "          Unmatched students is:"
								print [s.ID for s in students if not (s.ID in matched_students)]

							matched_projects.append(cur_project.ID)
						else:
							pass

				# The project that the student wants to match to is not feasible.
				# So, we do nothing.
				except (FieldError):
					pass
			else:
				if (verbose):
					print "Student is already matched"

		ranking_spot += 1

	# See the status after the initial process.
	for project in feasible_projects:
		#pass
		if (not(project.students == [])):
			if (verbose):
				print "For project " + str(project.ID) + ":"
				print "     Students: " + str([s.ID for s in project.students])
				print "     Waiting: " + str([(rank, s.ID) for (rank, s) in project.waiting_students])

	# NEW APPROACH

	# For each of the projects that are not full:
		# Add the students that are waiting 
			# (until all students are over or there is a full team)
			# Sort the students by the highest rank first
	for project in feasible_projects:
		print str(project.ID) + ": " + str(project.has_spot_for_one_more())
		
		# These projects are not full.
		if (project.has_remaining_spots()):
		 	if (project.has_waiting_students()):
		 		for (rank, waiting_student) in project.waiting_students:
		 			# Will add as many students as it can, and will return false and do nothing
		 			# when it cannot add any more waiting students.
		 			# This is already sorted by highest rank first. 
		 			project.add_student(waiting_student)
		else:
		 	pass
	

	# Sort the projects by number of spots remaining (lowest first).
	new_lst = sorted(feasible_projects, key = lambda x: len(x.students), reverse = True)
	feasible_projects = new_lst
	print [(p.ID, len(p.students)) for p in feasible_projects]

	# Allowable team size
	team_size = feasible_projects[0].num_MBAs + feasible_projects[0].num_MBAs
	allowable_team_size = team_size-1

	# If the team size is 3 (or some allowable number):
			# For all students
				# Remove the student from other waiting lists
				# Remove the student from other student lists

	for project in feasible_projects:
		if (len(project.students) >= allowable_team_size):
			remove_students_from_projects(project.students, feasible_projects, project.ID)

	# Creating a list of unfilled students
	# And will assign these to different projects
	unmatched_students = []


	# For all of the remaining projects that are not size 3:
	# Remove the students and add them to an unmatched list
	for project in feasible_projects:
		# These teams will not be full
		if (len(project.students) < allowable_team_size):
			# Add the project's students to the unmatched list
			unmatched_student_IDs = [s.ID for s in unmatched_students]
			for student in project.students:
				if (not(student.ID in unmatched_student_IDs)):
					unmatched_students.append(student)

	print "Unmatched students is :"
	print [s.ID for s in unmatched_students]

	for unmatched_student in unmatched_students:
		# If they are on the waiting list for some full teams:
			# Pick the highest rank that they gave a team whose waiting list they are on.
			# Add the student to that team.
		# If they are not on the waiting list:
			# Leave them unmatched.
		waiting_on = find_waiting_lists(unmatched_student, feasible_projects)
		if (len(waiting_on) > 0):
			top_project = waiting_on[0]
			top_project.students.append(unmatched_student)
			unmatched_students.remove(unmatched_student)
			# Remove this student from other projects
			remove_students_from_projects([unmatched_student], projects, top_project.ID)

	# Print:
	for project in feasible_projects:
		#pass
		if (len(project.students) >= allowable_team_size):
			if (verbose):
				print "For project " + str(project.ID) + ":"
				print "     Students: " + str([s.ID for s in project.students])
				print "     Waiting: " + str([(rank, s.ID) for (rank, s) in project.waiting_students])


	print "At the end the unmatched students are "
	print [s.ID for s in unmatched_students]


def remove_students_from_projects(students_to_remove, projects, ID):
	for project in projects:
		# Get the student objects from the tuples of (rank, student) in waiting_students
		objects_waiting_students = [tup[1] for tup in project.waiting_students]
		if (not (project.ID == ID)):
			for student in students_to_remove:
				if student in project.students:
					project.students.remove(student)

				# If the student was waiting
				if student in objects_waiting_students:
					# Get the index that the student is in the waiting_students list
					index_student = objects_waiting_students.index(student)
					# Remove the student & rank at that index
					project.waiting_students.pop(index_student)

# Find the waitings lists that student is on.
def find_waiting_lists(student, projects, verbose = False):
	waiting_lists = []
	for p in projects:
		lst = p.waiting_students
		matching = [tup for tup in lst if tup[1].ID == student.ID]
		if (verbose):
			print "For project " + str(p.ID) + ":"
			print matching
		# If this project is currently full
		if ((len(matching) > 0) and (len(p.students) == 4)):
			waiting_lists.append(p)

	# Sort the project list by the rank that this student gave the project
	new_lst = sorted(waiting_lists, key = lambda p: student.get_ranking(p.ID))
	if (verbose):
		print [p.ID for p in new_lst]
	return new_lst

if __name__ == "__main__":
	students = create_students_from_input("tests.csv")
	all_projects = all_pairs_sorted.generate_all_projects()
	initial_solution(students, all_projects)
	#feasible_projects = create_feasible_projects(students)


