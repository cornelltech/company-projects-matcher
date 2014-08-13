import numpy as np 
import pandas as pd 
import util

import classes
import ConfigParser
import greedy_student_and_fix
import random
from classes import Student
from classes import CompError
from classes import FieldError

student_ids = []

def print_students_and_waiting(projects):
	for project in projects:
		#pass
	#	if (len(project.students) >= allowable_team_size):
		print "For project " + str(project.ID) + ":"
		print "     Students: " + str([(s.ID, s.degree_pursuing) for s in project.students])
		print "     Waiting: " + str([(rank, s.ID) for (rank, s) in project.waiting_students])

def match_with_first_choice(students, projects):
	return greedy_student_and_fix.match_with_first_choice(students, projects)

# Matches projects in the order of highest interest first.


# Creates a random initial initial solution from only the feasible projects.
# Have the option to sort the projects by the highest interest first, so there is a 
# higher chance that the students matched to it actually ranked it.
def make_initial_solution(students, unsorted_projects, num_MBAs, num_MEngs, sorted = False, verbose = False):

	util.input_checks(students, unsorted_projects, num_MBAs, num_MEngs, sorted = False) 

	MBAs = filter(lambda student: student.degree_pursuing == 0 or student.degree_pursuing == "MBA", students)
	MEngs = filter(lambda student: student.degree_pursuing == 1 or student.degree_pursuing == "MEng", students)
	
	# Copying the students over.
	unmatched_students = students[:]

	matched_projects = []
	projects_copy = unsorted_projects[:]
	sorted_projects = util.sort_projects_by_demand(students, projects_copy)

	index = 0

	# Remove all students from these projects if there are students already there
	# Should not already have students be here
	for project in sorted_projects:
		if (not(len(project.students) == 0)):
			project.students = []

	while (len(unmatched_students) > 0):
		if (verbose):
			print "Len unmatched students is",
			print len(unmatched_students)
			print "There are " + str(len(MBAs)) + " MBAs"
			print "There are " + str(len(MEngs)) + " MEngs"
		
		if (len(unmatched_students) >= 4 and len(MBAs) >= 2 and len(MEngs) >= 2):
			if (sorted):
				project = sorted_projects[index]
			else:
				# Need to check if this project has already been matched.
				project = util.random_project(sorted_projects, matched_projects, False)
			
			# def random_student_lst(student_lst, already_picked, reuse):

			# Need to fix error here with popping from an empty list.
			MBA_one = util.random_student_lst(MBAs, [], True)
			MBAs.remove(MBA_one)
			
			MBA_two = util.random_student_lst(MBAs, [], True)
			MBAs.remove(MBA_two)
			
			MEng_one = util.random_student_lst(MEngs, [], True)
			MEngs.remove(MEng_one)
			
			MEng_two = util.random_student_lst(MEngs, [], True)
			MEngs.remove(MEng_two)

			project.students.append(MBA_one)
			project.students.append(MBA_two)
			project.students.append(MEng_one)
			project.students.append(MEng_two)

			unmatched_students.remove(MBA_one)
			unmatched_students.remove(MBA_two)
			unmatched_students.remove(MEng_one)
			unmatched_students.remove(MEng_two)

			matched_projects.append(project)
			if (verbose):
				print "Len of matched projects is " + str(len(matched_projects))
		else:
			# Less than 4 students left
			for student in MBAs:
				# Pick a random project and add this student to that project.
				if (sorted):
					project = sorted_projects[index]
				else:
					project = util.random_project(matched_projects, [], True)
				project.students.append(student)
				MBAs.remove(student)
				unmatched_students.remove(student)

				# Just trying to make sure that this project doesn't receive more than 1 extra person.
				if (len(matched_projects) > 1):
					if (verbose):
						print "Should remove project " + str(project.ID)
					matched_projects.remove(project)
			for student in MEngs:
				project = util.random_project(matched_projects, [], True)
				project.students.append(student)
				MEngs.remove(student)
				unmatched_students.remove(student)

				# Just trying to make sure that this project doesn't receive more than 1 extra person.
				if (len(matched_projects) > 1):
					if (verbose):
						print "Should remove project " + str(project.ID)
					matched_projects.remove(project)
		index += 1
		if (verbose):
			print [p.ID for p in sorted_projects if len(p.students) > 0]

	# Sanity check to make sure that all students were matched to projects.
	num_total_students = sum([len(project.students) for project in sorted_projects])
	if (not (len(students) == num_total_students)):
		raise CompError("Not all students were matched to projects.")


	return [p for p in sorted_projects if len(p.students) > 0]

# Note: these projects are the feasible ones.
def greedy_initial_solution(students, feasible_projects, verbose = True):
	if (verbose):
		print "Feasible projects are:"
		print [f.ID for f in feasible_projects]

	# The index of the ranking that we are currently looking at.
	ranking_spot = 0

	# The IDs of the projects whose students were already removed from unmatched_students.
	matched_projects = []
	# The IDs of the students were already removed from unmatched_students.
	matched_students = []
	random.shuffle(students)

	while (ranking_spot < classes.number_project_rankings):
		for cur_student in students:
			if (verbose):
				print "Student number " + str(cur_student.ID)

			# If the current student has not been matched yet:
			if (not (cur_student.ID in matched_students)):
				# Get the student's top ranking.
				cur_project_ID = cur_student.project_rankings[ranking_spot]

				# Try to get the project, assuming it's feasible.
				try:
					cur_project = util.get_project_from_ID(cur_project_ID, feasible_projects)
					if (verbose):
						print "     Student not matched (" + str(cur_student.ID) + ")"
						print "     Rank " + str(ranking_spot) + " is project " + str(cur_project_ID)
				
					# Try to add student to the project.
					wiggle = False
					successful_add = cur_project.add_student(cur_student, wiggle)
					if (successful_add and verbose):
						print "     Successful add of student " + str(cur_student.ID) + " to project " + str(cur_project.ID)
						print "     Project " + str(cur_project.ID) + "'s student list is now: "
						print "     " + str([s.ID for s in cur_project.students])

					# If there were no spots available, add this student to the waiting list.
					else:
						if (verbose):
							print "     Not successful. Adding to waiting list"
						cur_project.add_waiting_student(cur_student)

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

							# Remove students from unmatched_students
							for student in cur_project.students:
								matched_students.append(student.ID)

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
	if (verbose):
		print "AFTER INITIAL MATCHING PROCESS:"
		print_students_and_waiting(feasible_projects)

	unmatched_students = [s for s in students if not(s.ID in matched_students)]

	if (verbose):
		print "Unmatched students:"
		print [s.ID for s in unmatched_students]

	return (feasible_projects, unmatched_students)

def randomly_add_unmatched_students((feasible_projects, unmatched_students), verbose = True):
	'''
		To be used after initial_solution. Initial_solution leaves some students unmatched
		because all of their top choices were either non-feasible or were full by the time
		that they got to the projects.

		This function will check the list of unmatched students.
		While the size of the list is greater than the team size, this function will create
		teams. 
		With the leftover students, the function will add them randomly to existing teams.

	'''
	team_size = 4 

	# If there are any teams that are not full, remove all students from them.
	for project in feasible_projects:
		if (not(len(project.students) == team_size)):
			project.students = []

	matched_projects = [project for project in feasible_projects if len(project.students) >= 4]
	
	def can_make_team_with_waiting(u_students):
		unmatched_MBAs = [s for s in u_students if s.degree_pursuing == 0 or s.degree_pursuing == "MBA"]
		unmatched_MEngs = [s for s in u_students if s.degree_pursuing == 1 or s.degree_pursuing == "MEng"]

		MBAs_ok = len(unmatched_MBAs) >= 2
		MEngs_ok = len(unmatched_MEngs) >= 2
		overall_number = (len(u_students)/ team_size) > 0
		return overall_number and MBAs_ok and MEngs_ok

	unmatched_MBAs = [s for s in unmatched_students if s.degree_pursuing == 0 or s.degree_pursuing == "MBA"]
	unmatched_MEngs = [s for s in unmatched_students if s.degree_pursuing == 1 or s.degree_pursuing == "MEng"]
	
	while (len(unmatched_students) > 0):
		if (can_make_team_with_waiting(unmatched_students)):
			# Pick a random project that does not have any students on it. 
			project = util.random_project(feasible_projects, matched_projects, False)

			MBA_one = util.random_student_lst(unmatched_MBAs, [], False)
			unmatched_students.remove(MBA_one)
			unmatched_MBAs.remove(MBA_one)
			
			MBA_two = util.random_student_lst(unmatched_MBAs, [], False)
			unmatched_students.remove(MBA_two)
			unmatched_MBAs.remove(MBA_two)

			MEng_one = util.random_student_lst(unmatched_MEngs, [], False)
			unmatched_students.remove(MEng_one)
			unmatched_MEngs.remove(MEng_one)
			
			MEng_two = util.random_student_lst(unmatched_MEngs, [], False)
			unmatched_students.remove(MEng_two)
			unmatched_MEngs.remove(MEng_two)

			project.students.append(MBA_one)
			project.students.append(MBA_two)
			project.students.append(MEng_one)
			project.students.append(MEng_two)

			matched_projects.append(project)
		else:
			#pass
			feasible_projects = filter(lambda project: len(project.students) == team_size, feasible_projects)
			available_projects = feasible_projects[:]
			for student in unmatched_students:
				project = util.random_project(available_projects, [], True)
				project.add_student(student, True)
				available_projects.remove(project)
			unmatched_students = []
	
	if (verbose):
		print "AFTER SECONDARY MATCHING PROCESS:"
		print_students_and_waiting(feasible_projects)

	if (verbose):
		print "Unmatched students:"
		print [s.ID for s in unmatched_students]

	return feasible_projects

def greedy_initial_solution_and_fill_unmatched(students, feasible_projects, verbose = True):
	initial_res = greedy_initial_solution(students, feasible_projects, verbose)
	feasible_projects = randomly_add_unmatched_students(initial_res, verbose)
	return feasible_projects	

def post_processing(feasible_projects, students, verbose = True):


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
	while (len(unmatched_IDs) > 0):
		# TODO: this is hacky and was a way to only affect the first project.
		index = util.random_index(len(unmatched_IDs))
		tup = sorted_unfilled[index]
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
				r = util.random_index(len(project_ranks))
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
				r = util.random_index(len(project_ranks))
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
	if (verbose):
		print_students_and_waiting(feasible_projects)


	print "At the end the unmatched students are "
	print [s.ID for s in unmatched_students]

	# Maybe try this approach
	# For the unmatched students:
		# For project in their list of rankings:
			# If done is false
				# List all students who ranked this project.
				# Form a team with these students.
				# If 

	return (feasible_projects, unmatched_students)

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

# NOTE: this is where the issue with indices and randomness came up.
# ID is the ID of the project that we don't want them to be removed from.
def remove_students_from_projects(students_to_remove, projects, ID, remove_from_waiting = False):
	for project in projects:
		# Get the student objects from the tuples of (rank, student) in waiting_students
		objects_waiting_students = [tup[1] for tup in project.waiting_students]
		# If we encounter a project that is not of the given ID 
		# (meaning we DO want to remove students from this project):
		if (not (project.ID == ID)):
			for student in students_to_remove:
				# If the student was on the project, remove it.
				if student in project.students:
					project.students.remove(student)

				# If the student was waiting, remove it.
				if student in objects_waiting_students:
					# Get the index that the student is in the waiting_students list
					if (remove_from_waiting):
						index_student = objects_waiting_students.index(student)
						# Remove the student & rank at that index
						project.waiting_students.pop(index_student)
					else:
						pass

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

	configParser = ConfigParser.ConfigParser()
	configFilePath = r'config.txt'
	configParser.read(configFilePath)

	input_file = configParser.get('files', 'greedy_attempt_two_file')

	students = util.create_students_from_input("tests.csv")
	all_projects = util.generate_all_projects()
	initial_solution(students, all_projects)
	#feasible_projects = util.create_feasible_projects(students)


