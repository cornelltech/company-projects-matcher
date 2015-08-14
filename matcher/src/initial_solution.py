import util

import classes
import random
from classes import CompError
from classes import FieldError
import numpy as np

student_ids = []

def print_students(projects):
	for project in projects:
		print "For project " + str(project.ID) + ":"
		print "     Students: " + str([(s.ID, s.degree_pursuing) for s in project.students])

def random_initial_solution_for_diversity(students, projects, num_teams):
	'''
		Using the inputs, creates a random set of initial Project-Student pairings.
	'''
	# If length of projects < num_teams, raise an error
	if (len(projects) < int(num_teams)):
		raise CompError("There are fewer projects than the number of desired teams.")
	# Otherwise, pick num_teams projects (the first ones)
	projects = projects[0:num_teams]

	# Get the MBAs and MEngs
	MBAs = filter(lambda student: student.degree_pursuing == 0 or student.degree_pursuing == "MBA", students)
	MEngs = filter(lambda student: student.degree_pursuing == 1 or student.degree_pursuing == "MEng", students)

	num_MBAs_per_team = len(MBAs) / num_teams
	num_MEngs_per_team = len(MEngs) / num_teams

	# Copying the students over.
	unmatched_students = students[:]
	matched_projects = []
	# If num MBAs per team == 0 or num Mengs per team == 0 raise an error
	if (num_MBAs_per_team == 0 or num_MEngs_per_team == 0):
		raise CompError ("There are not enough MBAs or MEngs to produce the desired teams.")

	# Sequentially go through the projects, and assign the proper number of MBAs and 
	# MEngs to each project.
	for project in projects:

		num_MBAs_needed_for_this_team = num_MBAs_per_team
		num_MEngs_needed_for_this_team = num_MEngs_per_team

		# Get the required number of MBAs.
		while (num_MBAs_needed_for_this_team > 0):
			cur_MBA = util.random_student_lst(MBAs, [], True)
			project.students.append(cur_MBA)
			MBAs.remove(cur_MBA)
			unmatched_students.remove(cur_MBA)
			num_MBAs_needed_for_this_team -= 1

		# Get the required number of MEngs.
		while (num_MEngs_needed_for_this_team > 0):
			cur_MEng = util.random_student_lst(MEngs, [], True)
			project.students.append(cur_MEng)
			MEngs.remove(cur_MEng)
			unmatched_students.remove(cur_MEng)
			num_MEngs_needed_for_this_team -= 1

		matched_projects.append(project)

	index = 0
	while (len(unmatched_students) > 0):
		project = projects[index]
		cur_student = util.random_student_lst(unmatched_students, [], True)
		project.students.append(cur_student)
		unmatched_students.remove(cur_student)
		if (index == len(projects) - 1):
			index = 0
		else:
			index += 1

	for p in projects:
		print str(p.ID) + ":" + str([s.ID for s in p.students])

	# Sanity check to make sure that all students were matched to projects.
	num_total_students = sum([len(project.students) for project in projects])
	if (not (len(students) == num_total_students)):
		raise CompError("Not all students were matched to projects.")

	return projects
	
def greedy_initial_solution(original_students, original_feasible_projects, verbose = False):
	students = original_students[:]
	feasible_projects = original_feasible_projects[:]

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

	while (ranking_spot < classes.alg_number_project_rankings):
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
							print "     Not successful. "

                                        #print ("Project " + str(cur_project.ID) + " has " + str(cur_project.remaining_spots) + " spots left ")
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
		print_students(feasible_projects)

	unmatched_students = [s for s in students if not(s.ID in matched_students)]

	if (verbose):
		print "Unmatched students:"
		print [s.ID for s in unmatched_students]

	return (feasible_projects, unmatched_students)

def greedy_initial_solution_team_first(original_students, original_feasible_projects, offset, verbose = False):
        ''' 
                Greedily matches students to projects in a team-first strategy, where
                lower-popularity projects are filled first to minimize the chance that a student is
                unmatched to a project on his/her ranking list
        '''
        students = original_students[:]
        feasible_projects = original_feasible_projects[:]
        if (verbose):
                print "Feasible projects are:"
		print [f.ID for f in feasible_projects]
        # The IDs of the projects whose students were already removed from unmatched_students.
	matched_projects = []
	# The IDs of the students were already removed from unmatched_students.
	matched_students = []
        num_required_teams = len(students)/feasible_projects[0].capacity
        print num_required_teams
        #iterate in reverse popularity order
        for project in reversed(feasible_projects[num_required_teams + offset + 1:] + feasible_projects[:num_required_teams + offset]):
                #get all the students interested in this project who have yet to be matched
                unmatched_interested =  [s for s in filter(lambda s: project.ID in s.project_rankings and not s.ID in matched_students, students)]
                if len(unmatched_interested) >= project.capacity:
                        unmatched_interested.sort(key = project.inv_get_ranking)
                        #get the students who want this project most and put them on this project
                        selected_unmatched = unmatched_interested[:5]
                        for s in selected_unmatched:
                                project.add_student(s, False)
                        remove_students_from_projects(project.students, feasible_projects, project.ID)
                        # Remove students from unmatched_students
                        for student in project.students:
                                matched_students.append(student.ID)
                        matched_projects.append(project.ID)
                else:
                        pass
        unmatched_students = [s for s in students if not(s.ID in matched_students)]
        return (feasible_projects, unmatched_students)

def randomly_add_unmatched_students((original_feasible_projects, original_unmatched_students), verbose = False):
	'''
		To be used after initial_solution. Initial_solution leaves some students unmatched
		because all of their top choices were either non-feasible or were full by the time
		that they got to the projects.

		This function will check the list of unmatched students.
		While the size of the list is greater than the team size, this function will create
		teams. 
		With the leftover students, the function will add them randomly to existing teams.

	'''
	feasible_projects = original_feasible_projects[:]
	unmatched_students = original_unmatched_students[:]

	team_size = feasible_projects[0].capacity

	# If there are any teams that are not full, remove all students from them.
	for project in feasible_projects:
		if (not(len(project.students) == team_size)):
			project.students = []

	matched_projects = [project for project in feasible_projects if len(project.students) >= team_size]
	
	def can_make_team_with_waiting(u_students):
                overall_number = (len(u_students)/ team_size) > 0
		return overall_number
	
	while (len(unmatched_students) > 0):
		if (can_make_team_with_waiting(unmatched_students)):
			# Pick a random project that does not have any students on it. 
			project = util.random_project(feasible_projects, matched_projects, False)
                        for i in range(team_size):
                                st = util.random_student_lst(unmatched_students, [], False)
                                unmatched_students.remove(st)
                                project.students.append(st)
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
		print_students(feasible_projects)

	if (verbose):
		print "Unmatched students:"
		print [s.ID for s in unmatched_students]

	return feasible_projects

def greedy_initial_solution_and_fill_unmatched(students, feasible_projects, verbose = False):
	initial_res = greedy_initial_solution(students, feasible_projects, verbose)
	feasible_projects = randomly_add_unmatched_students(initial_res, verbose)
	return [p for p in feasible_projects if len(p.students) > 0]

# ID is the ID of the project that we don't want them to be removed from.
def remove_students_from_projects(students_to_remove, projects, ID, remove_from_waiting = False):
	'''
		students_to_remove: a list of Students that we would like to remove from other projects.
	'''
	for project in projects:
		# Get the student objects from the tuples of (rank, student) in waiting_students
		objects_waiting_students = [tup[1] for tup in project.waiting_students]
		# If we encounter a project that is not of the given ID 
		# (meaning we DO want to remove students from this project):
		if (not (project.ID == ID)):
			for student in students_to_remove:
				# If the student was on the project, remove it.
				if student in project.students:
					project.remove_student(student)

				# If the student was waiting, remove it.
				if student in objects_waiting_students:
					# Get the index that the student is in the waiting_students list
					if (remove_from_waiting):
						index_student = objects_waiting_students.index(student)
						# Remove the student & rank at that index
						project.waiting_students.pop(index_student)
					else:
						pass
