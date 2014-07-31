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

	# Adds students to form teams of 5.
	# for unmatched_student in unmatched_students:
	# 	# If they are on the waiting list for some full teams:
	# 		# Pick the highest rank that they gave a team whose waiting list they are on.
	# 		# Add the student to that team.
	# 	# If they are not on the waiting list:
	# 		# Leave them unmatched.
	# 	waiting_on = find_waiting_lists(unmatched_student, feasible_projects)
	# 	if (len(waiting_on) > 0):
	# 		top_project = waiting_on[0]
	# 		top_project.students.append(unmatched_student)
	# 		for w_tuple in top_project.waiting_students:
	# 			if (w_tuple[1].ID == unmatched_student.ID):
	# 				top_project.waiting_students.remove(w_tuple)
	# 		unmatched_students.remove(unmatched_student)
	# 		# Remove this student from other projects
	# 		remove_students_from_projects([unmatched_student], projects, top_project.ID)

	unfilled_projects_with_ranks = []
	for project in feasible_projects:
		# If the project is not full
		if (len(project.students) < team_size):
			# List all of the students who ranked it
			project_ranks = []
			for student in students:
				if (project.ID in student.project_rankings):
					rank = student.get_ranking(project.ID)
					# These are the unmatched students who ranked the projects.
					# Add the student, rank, and degree to project ranks.
					project_ranks.append((student, rank, student.degree_pursuing))
			# If any students ranked these projects:	
			if (len(project_ranks) > 0):
				# Add them to our list.
				unfilled_projects_with_ranks.append((project, project_ranks))


	# Print the unfilled projects that were ranked
	for tup in unfilled_projects_with_ranks:
		ID = tup[0]
		project_ranks = tup[1]
		print str(ID) + ":"
		print [(rank, s.ID, deg) for (s, rank, deg) in project_ranks]
		
	print "Starting the sorted"
	# Sort the unfilled projects by the number of students that they have (largest first)
	# Then going to "steal" students who also ranked these from other projects
	# And see if that resolves things
	sorted_unfilled = sorted(unfilled_projects_with_ranks, 
		key = lambda x: len(x[0].students), reverse = True)
	for proj in sorted_unfilled:
		students = proj[0].students
		print str(proj[0].ID) + ":" + str(len(students))
	print "Ending the sorted"

	unmatched_IDs = [s.ID for s in unmatched_students]
	#feasible_project_IDs = [s.ID for s in feasible_projects]

	#for tup in sorted_unfilled:
	for i in range (0, 1):
		# TODO: this is hacky and was a way to only affect the first project.
		tup = sorted_unfilled[0]
		project = tup[0]
		project_ranks = tup[1]
		# [(rank, s.ID, deg) for (s, rank, deg) in project_ranks]
		# Find out what type of student the project requires
		num_MBAs = filter(lambda s: s.degree_pursuing == "MBA" or s.degree_pursuing == 0, project.students)
		print [s.ID for s in project.students]
		num_MBAs_needed = 2 - len(num_MBAs)
		num_MEngs = filter(lambda s: s.degree_pursuing == "MEng" or s.degree_pursuing == 1, project.students)
		num_MEngs_needed = 2 - len(num_MEngs)

		for i in range(0, num_MBAs_needed):
			# Pick a random MBA from the list of students who ranked.
			need_new_student = True
			while (need_new_student):
				r = random_teams.random_index(len(project_ranks))
				random_triple = project_ranks[r]
				new_student = random_triple[0]
				student_type = random_triple[2]
				if (student_type == "MBA" or student_type == 0):
					IDs_already_on_project = [s.ID for s in project.students]
					# Check that this student is not already on this project
					if (new_student.ID in IDs_already_on_project):
						# If they are, then pick another random student.
						pass
					else:
						# They're not on the project, so don't need to look for another student.
						need_new_student = False
						# Add the student to the project.
						print "FOUND A SUITABLE MBA TO ADD "
						print "SUITABLE MBA's ID IS " + str(new_student.ID)
						boolean = project.add_student(new_student, verbose = True) 
						# If this new student is on the waiting list.
						waiting_list_IDs = [s.ID for (rank, s) in project.waiting_students]
						if (new_student.ID in waiting_list_IDs):
							# Remove the student from the project
							project.waiting_students.remove(new_student)
						print boolean

						matched = not (new_student.ID in unmatched_IDs)
						print "Student " + str(new_student.ID) + " is matched: " + str(matched)

						# If this student was already matched, remove this student from their other project.
						if (matched):
							# Find the project that this student was on
							project_to_remove = find_students_project(new_student, 
								feasible_projects, project.ID)
							# Remove this student from that project.
							project_to_remove.students.remove(new_student)
							# (HARD) Add that project to the list of projects that are fill.
							
							# Change to a while loop. ^^^^^
							pass

						# If they weren't matched, remove them from the unmatched list.
						else:
							# Remove the student from the unmatched students list
							unmatched_students.remove(new_student)
							unmatched_IDs.remove(new_student.ID)
				else:
					pass

		print "Project needed " + str(num_MBAs_needed) + " MBAs. And now is "
		print str(project.ID) + ": " + str([s.ID for s in project.students])	 	

		for i in range(0, num_MEngs_needed):
			# Pick a random MBA from the list of students who ranked.
			need_new_student = True
			while (need_new_student):
				r = random_teams.random_index(len(project_ranks))
				random_triple = project_ranks[r]
				student = random_triple[0]
				student_type = random_triple[2]
				if (student_type == "MEng" or student_type == 1):
					IDs_already_on_project = [s.ID for s in project.students]
					# Check that this student is not already on this project
					if (student.ID in IDs_already_on_project):
						# If they are, then pick another random student.
						pass
					else:
						# They're not on the project, so don't need to look for another student.
						need_new_student = False
						# Add the student to the project.
						project.add_student(student) 
				else:
					pass

		print "Project needed " + str(num_MEngs_needed) + " MEngs. And now is "
		print str(project.ID) + ": " + str([s.ID for s in project.students])	

	# Printing things
	for project in feasible_projects:
		#pass
	#	if (len(project.students) >= allowable_team_size):
			if (verbose):
				print "For project " + str(project.ID) + ":"
				print "     Students: " + str([s.ID for s in project.students])
				print "     Waiting: " + str([(rank, s.ID) for (rank, s) in project.waiting_students])


	print "At the end the unmatched students are "
	print [s.ID for s in unmatched_students]

	# Maybe try this approach
	# For the unmatched students:
		# For project in their list of rankings:
			# If done is false
				# List all students who ranked this project.
				# Form a team with these students.
				# If 

# For the given student, find the project that it was on.
def find_students_project(student, projects, newly_added_ID):
	#project_IDs = [p.ID for p in projects]
	matched_projects = []
	for project in projects:
		# This is the project that we just added our student to,
		# so we don't do anything in this way.
		if (project.ID == newly_added_ID):
			pass
		else:
			student_IDs = [s.ID for s in project.students]
			if (student.ID in student_IDs):
				matched_projects.append(project)
	if (len(matched_projects) > 1):
		raise CompError("More than one project that is not the newly added one.")
	elif (len(matched_projects) == 0):
		raise CompError("No project that is not the newly added one.")
	else:
		# There is only one project in matched_projects.
		print "The project that " + str(student.ID) + " matched was:" + str(matched_projects[0].ID)
		return matched_projects[0]	

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


