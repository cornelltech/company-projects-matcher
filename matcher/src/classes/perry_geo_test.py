import util
import greedy_attempt_two
import perry_geo_annealing as pg
import ConfigParser
import random_teams

from anneal import Annealer
import random
import classes
from classes import CompError
import perry_geo_main
import math
import distance
import numpy as np
#input_file = "tests.csv"

# Framework to use perrygeo's python-simulated-annealing library.
if (__name__ == "__main__"):
	'''
		A format for describing the state of the system:
		------------------------------------------------
		'students' is a list of Students (created from the given input file).

		'unmatched_students' is a list of Students who are not currently matched
		to a project.

		'state' is a tuple of (Project list, Student list) where:
			- Project list:
				- Each project is assigned some number of students
				(can be changed in classes/Project.)
				- At any given point, 'state' tells us what the current state of
				  the system is (i.e. which Students are with which Projects.)
			- Student list:
				- These are the unmatched students (students who are not on any
					proje ct). 

		Desired postconditions:
			- Each student is matched to exactly one project.
			- Each project has its desired number and makeup of students:
				Ex. 2 MBA, 2 MEng

		The function to be minimized is the energy of the state (energy(state)).
		In our case, energy calculates the cost of assigning people to projects.

	'''
	# Create a ConfigParser to get the filename.
	configParser = ConfigParser.ConfigParser()
	configFilePath = r'config.txt'
	configParser.read(configFilePath)

	input_file = configParser.get('files', 'perry_geo_main_file')
	num_MBAs = configParser.getint('valid_values', 'num_MBAs')
	num_MEngs = configParser.getint('valid_values', 'num_MEngs')
	team_size = num_MBAs + num_MEngs

	# Creating the annealer with our energy and move functions.
	annealer = Annealer(pg.energy, pg.move)

	# Format for describing the state of the system.
	#print "All students:"
	#print [s.ID for s in students]
	all_projects = util.generate_all_projects()
	#print "All projects:"
	#print [p.ID for p in all_projects]
	#feasible_projects = util.create_feasible_projects(students, all_projects)
	
	
	def make_data_for_80_students(students):
		sorted_projects = util.sort_projects_by_demand(students, all_projects, tup=True)
		print "Sorted projects is " + str(sorted_projects)

		# This is the number of total votes cast.
		print "There were " + str(sum([tup[0]*tup[1] for tup in sorted_projects])) + " total votes cast"
		print "There are " + str(sum([tup[1] for tup in sorted_projects])) + " total orig projects"

		#print "For project 1235: " + str(util.get_num_ranked(proj_three, students))

		# Input x is the number of students out of 13 who voted each project.
		# Comes from sorted_projects
		# This is number of students who would vote on the project but there are not the same 
		# # of projects

		def scale(tup):
			num_votes = tup[0]
			num_projects = tup[1]
			#scaled_votes = round ((num_votes * (72.0 / 13.0) / 75 * 55) + 1)
			scaled_votes = round ((num_votes * (72.0 / 13.0)) / 1.31)
			scaled_projects = round ((num_projects) * (75.0 / 55.0))
			#scaled_projects = num_projects
			return (scaled_votes, scaled_projects)
		scaled_tups = map(scale, sorted_projects)

		for tup in scaled_tups:
			print "There were " + str(tup[1]) + " projects with " + str(tup[0]) + " votes"

		num_projects = sum([tup[1] for tup in scaled_tups])
		tup_to_change = scaled_tups[8]
		fst = tup_to_change[0]
		snd = tup_to_change[1]
		scaled_tups[8] = (fst - 1, snd)

		print "Scaled tups is " + str(scaled_tups)
		print "There are " + str(num_projects) + " final projects"

		print "There were " + str(sum([tup[0]*tup[1] for tup in scaled_tups])) + " total votes cast"

		return scaled_tups


	def random_solutions_and_goodness(use_file, students, feasible_projects, num_MBAs, num_MEngs, num_times = 100000):
		min_energy = float("inf")
		min_sol = None
		for i in range (0, num_times):
			init = greedy_attempt_two.make_initial_solution(students, feasible_projects, num_MBAs, num_MEngs)
		#	print "There are  " + str(len(feasible_projects)) + " feasible projects"
			print "Random solution " + str(i) + ":"
			for p in init:
				print str(p.ID) + ":" + str([s.ID for s in p.students])
			inv_cov_mat_tup = distance.create_inv_cov_mat_from_data(use_file, students)
			#inv_cov_mat = inv_cov_mat_tup[0]
			cur_energy = pg.energy((init, inv_cov_mat_tup))
			if (cur_energy < min_energy):
				min_sol = init
				min_energy = cur_energy
		for p in min_sol:
			print str(p.ID) + ":" + str([s.ID for s in p.students])
		print "The minimum energy is " + str(min_energy)
		return [p for p in min_sol if len(p.students) > 0]

	def test_random_solutions_and_goodness(students, feasible_projects):
		#random_solutions_and_goodness
 		res = greedy_attempt_two.initial_solution(students, feasible_projects)
 		res_two = greedy_attempt_two.randomly_add_unmatched_students(res)
 		print res_two

 	# Trying to make students to fit the data.
 	def make_students_to_fit_data(scaled_tups):
 		remaining_num_MBAs = 37
 		remaining_num_MEngs = 35

 		# Creating our actual MBA and MEng Student objects.
 		# Creating them with empty student ranking lists ([]) so we can call append
 		# desired values onto them.
 		MBAs = random_teams.create_random_MBAs(4, 4, remaining_num_MBAs, empty_ranks = True)
 		MEngs = random_teams.create_random_MEngs(4, 4, remaining_num_MEngs, empty_ranks = True)
 		students_choices = MBAs + MEngs
 		random.shuffle(students_choices)
 		random_teams.print_student_list(MBAs)
 		random_teams.print_student_list(MEngs)
 		
 		# Empty lists showing which projects and students are already taken.
 		projects_taken = []
 
 		for tup in scaled_tups:
 			num_votes = tup[0]
 			num_projects = tup[1]

 			# For each number of projects:
 			for i in range(0, int(num_projects)):
 				print "Num_projects is " + str(num_projects)
 				print "Each of these projects needs " + str(num_votes) + " votes"
 				# Pick a random project that hasn't been picked already.
 				project = util.random_project(all_projects, projects_taken, reuse = False, verbose = True)
 				print "Project ID: " + str(project.ID)
 				
 				already_picked = []
 				# For the number of votes that this project needs:
 				for i in range (0, int(num_votes)):
 					print "Current num votes achieved is: " + str(i)
 					# These are the students that have already ranked this project.

 					print "Already picked is " + str([p.ID for p in already_picked])
 					if (len(students_choices) > 0):
 						print "Length of students_choices is " + str(len(students_choices))
 						student = util.random_student_lst(students_choices, already_picked, reuse = False)
 						print "Student ID is " + str(student.ID)
 						print "Student in already_picked " + str(student in already_picked)
		 			else:
		 				error = "There are no students with empty ranking spots."
		 				raise CompError(error)

		 			# If the student is full: we should not pick them.
		 			# This should be taken care of by the second "if" below this.

		 			# This student has spots open.
		 			if (len(student.project_rankings) < classes.number_project_rankings):
		 				# Add this project's ID to the student's rankings.
		 				print "Student " + str(student.ID) + " has spots available"
		 				student.project_rankings.append(project.ID)
		 				print "Added project " + str(project.ID) + " to student " + str(student.ID) + "'s rankings."
		 				already_picked.append(student)
		 				print "Student " + str(student.ID) + "'s project rankings are now " + str(student.project_rankings)
		 				print "Already picked is now " + str([p.ID for p in already_picked])

	 				# If the student does not have spots left:
	 				# Don't want this to be an else because this could be the same student as above.
	 				if (len(student.project_rankings) >= classes.number_project_rankings):
	 					print "Student " + str(student.ID) + "'s rankings are full."
	 					print "Removing this student from student_choices."
	 					students_choices.remove(student)


 				projects_taken.append(project)
 		
 		for student in MBAs:
 			print "Student " + str(student.ID) + "'s choices: " + str(student.project_rankings)
 		for student in MEngs:
 			print "Student " + str(student.ID) + "'s choices: " + str(student.project_rankings)


 	def print_final_solution(state):
		print "Final Solution:"
 		(projects, inv_cov_mat_tup) = state
		for p in projects:
		 	print str(p.ID) + ": " + str([s.ID for s in p.students])
		 	print "Student attributes: " + str([s.get_numerical_student_properties()])
		 	print "Diversity: " + str(p.calculate_diversity(inv_cov_mat_tup))
			ranks = []
			# NOTE: get ranking returns 100 if the student did not rank the project.
		 	for student in p.students:
				rank = student.get_ranking(p.ID)
				print "rank"
				#cost = student.get_cost_from_ranking(rank)
				ranks.append(rank)
			avg_project_rank = np.mean(ranks)
			print "Average project rank: " + str(avg_project_rank)

 	#scaled_projects = make_data_for_80_students()
 	#make_students_to_fit_data(scaled_projects)
 	def manual_schedule(use_file, students, sol):
 		#def create_inv_cov_mat_from_data(use_file, students, file = default_file):

		inv_cov_mat_tup = distance.create_inv_cov_mat_from_data(use_file, students)
		state = (sol, inv_cov_mat_tup)
		# Manually set the annealing schedule.
		state, e = annealer.anneal(state, 1000000, 0.01, 54000, updates=0)
		print_final_solution(state)

		print "Final energy is " + str(e)
		print "Calculated final energy is " + str(pg.energy(state))

	def do_random():
 		remaining_num_MBAs = 37
 		remaining_num_MEngs = 35
 		MBAs = random_teams.create_random_MBAs(4, 4, remaining_num_MBAs)
 		MEngs = random_teams.create_random_MEngs(4, 4, remaining_num_MEngs)
 		students = MBAs + MEngs

 		feasible_projects = util.create_feasible_projects(students, all_projects, verbose = True)
	 	sol = random_solutions_and_goodness(False, students, feasible_projects, 37, 35, num_times = 1)
	 	
	 	print "about to do manual schedule"
	 	manual_schedule(False, students, sol)

	def test_project_diversities(students):
		project = util.random_project(all_projects, [], reuse = False)
		print "For project " + str(project.ID)
		for i in range(5):
			project.students.append(students[i])
			print (students[i].get_student_properties())
			#do_preprocessing[2]
		print project.calculate_diversity()

		project_two = util.random_project(all_projects, [project], reuse = False)
		print "For project " + str(project_two.ID)
		for i in range(5, 10):
			project_two.students.append(students[i])
			print (students[i].get_student_properties())
		print project_two.calculate_diversity()	

	#scaled_tups = [(0.0, 10.0), (4.0, 18.0), (8.0, 18.0), (13.0, 15.0), (17.0, 8.0), (21.0, 1.0), (25.0, 1.0), (30.0, 3.0), (37.0, 1.0)]
	#make_students_to_fit_data(scaled_tups)


	# def create_inv_cov_mat_from_data(use_file, students, file = default_file):
	# quadruple = create_covariance_matrix(use_file, file)
	# #def create_covariance_matrix(use_file, students, file = default_file, verbose = False):

	# cov_mat = quadruple[2]
	# dict_key_vals = quadruple[3]
	# inv_cov_mat = inverse_matrix(cov_mat)
	# return (inv_cov_mat, dict_key_vals)

	# Just create the inverse cov mat from data once. 
	
	#inv_cov_mat = distance.create_inv_cov_mat_from_data(use_file, students)
	#print inv_cov_mat
	# Pass this into energy every time.

	# This could be the second part of the tuple
	# Unmatched students is just always an empty list now anyways

	do_random()



