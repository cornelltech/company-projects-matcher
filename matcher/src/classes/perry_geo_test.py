import util
import greedy_attempt_two
import perry_geo_annealing as pg
import ConfigParser
import random_teams

from anneal import Annealer
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
	all_projects = util.generate_all_projects()

	def random_solutions_and_goodness(use_file, students, feasible_projects, num_MBAs, num_MEngs, num_times = 100):
		'''
			Returns a list of projects.
		'''
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

	def pick_disjoint_seeds(use_file, students, feasible_projects, num_MBAs, num_MEngs, num_times = 10):
		# Make an initial random solution.
		# Record the projects that are on that solution.
		# Make another random solution without any of those projects.
		# Pick "best and different."
		pass

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

 	def manual_schedule(use_file, students, sol):
 		#def create_inv_cov_mat_from_data(use_file, students, file = default_file):

		inv_cov_mat_tup = distance.create_inv_cov_mat_from_data(use_file, students)
		state = (sol, inv_cov_mat_tup)
		# Manually set the annealing schedule.
		state, e = annealer.anneal(state, 1000000, 0.01, 54000, updates=0)
		print_final_solution(state)

		print "Final energy is " + str(e)
		print "Calculated final energy is " + str(pg.energy(state))

	def make_random_students():
		remaining_num_MBAs = 37
 		remaining_num_MEngs = 35
 		MBAs = random_teams.create_random_MBAs(4, 4, remaining_num_MBAs)
 		MEngs = random_teams.create_random_MEngs(4, 4, remaining_num_MEngs)
 		students = MBAs + MEngs
		return students

	def do_random_initial_solutions(students):
 		feasible_projects = util.create_feasible_projects(students, all_projects, verbose = True)
	 	sol = random_solutions_and_goodness(False, students, feasible_projects, 37, 35, num_times = 100)
	 	print "About to do manual schedule"
	 	manual_schedule(False, students, sol)

	def do_greedy_initial_solution(students, verbose = True):
		feasible_projects = util.create_feasible_projects(students, all_projects, verbose)
		sol = greedy_attempt_two.greedy_initial_solution_and_fill_unmatched(students, feasible_projects, verbose)
		print "About to do manual schedule"
	 	manual_schedule(False, students, sol)

	def test_project_diversities(students):
		project = util.random_project(all_projects, [], reuse = False)
		print "For project " + str(project.ID)
		for i in range(5):
			project.students.append(students[i])
			print (students[i].get_student_properties())
		print project.calculate_diversity()

		project_two = util.random_project(all_projects, [project], reuse = False)
		print "For project " + str(project_two.ID)
		for i in range(5, 10):
			project_two.students.append(students[i])
			print (students[i].get_student_properties())
		print project_two.calculate_diversity()	

	students = util.create_students_from_input("eighty_students.csv")
	#make_data_for_80_students(students)
	do_greedy_initial_solution(students)


