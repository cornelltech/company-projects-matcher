import util
import initial_solution
import perry_geo_annealing as pg
import perry_geo_annealing_diversity as diversity

import distance
import numpy as np
import copy
import ConfigParser

class CompError(Exception):
	def __init__(self, value):
		self.val = value
	def __str__(self):
		return repr(self.val)

def manual_schedule(use_file, students, sol, annealer, use_diversity, filename, output_file = "output.csv"):
	'''
		Parameters
		----------
		use_file: indicates if we want to use the data from the file or not (bool).
		students: student attributes (2d numpy array of ints).
		sol: a solution (a Project list).
		annealer: the Annealer object (Annealer).
		use_diversity: indicates which energy function we want to use (bool).
		    If use_diversity is True, then we use the energy function from
		    perry_geo_annealing_diversity.
		    If use_diversity is False, then we use the energy function from 
		    perry_geo_annealing.py.
		filename: file that the input should come from (string).
		output_file: file that the output should go to (string).

		Returns
		-------
		Nothing. Writes to the output file and prints updates and solution
		to console.
		

	'''

	inv_cov_mat_tup = distance.create_inv_cov_mat_from_data(use_file, students, filename)
	if (len(sol) < 2):
		error = "There is only one team, so we cannot perform simulated annealing."
		raise CompError(error)

	state = (sol, inv_cov_mat_tup)
	print "Initial energy is " + str(pg.energy(state))
	# Manually set the annealing schedule.
	state, e = annealer.anneal(state, 10000, 0.01, 54000, updates=0)

	print "Final energy is " + str(e)
	if (use_diversity):
		print "Calculated final energy is " + str(diversity.energy(state))
	else:
		print "Calculated final energy is " + str(pg.energy(state))

	util.print_final_solution(state, use_diversity, output_file)

	# Only print the unranked students if we a care about the students' rankings.
	if (not(use_diversity)):
		util.list_unranked_students(state)
		util.list_low_interest_students(state)

def greedy_solutions_and_goodness(students, feasible_projects, num_times = 1000):
		'''
			Optimizes the average student ranking, not including diversity.
			Then, annealing will optimize a function of the two.
			Returns a list of projects.
		'''
		min_rank = float("inf")
		min_sol = None

		def calculate_avg_rank(solution, verbose = True):
				avgs = []
				for p in solution:
					if (verbose):
						print str(p.ID) + ":" + str([s.ID for s in p.students])
						print "Ranks:",
					rankings = [s.get_ranking(p.ID) for s in p.students]
					if (verbose):
						print rankings
					avg_rank = np.mean(rankings)
					if (verbose):
						print "Average rank: " + str(avg_rank)
					avgs.append(avg_rank)
				overall_average_rank = np.mean(avgs)
				return overall_average_rank

		for i in range (0, num_times):
			#Reset the feasible projects.
			for project in feasible_projects:
				project.students = []
			
			cur_sol = initial_solution.greedy_initial_solution_and_fill_unmatched(students, feasible_projects)
			print "Greedy solution " + str(i) + ":"

			cur_avg_rank = calculate_avg_rank(cur_sol)
			
			print "Solution " + str(i) + " average rank: " + str(cur_avg_rank)

			# Compare the average ranks.
			if (cur_avg_rank < min_rank):
				min_rank = cur_avg_rank
				min_sol = copy.deepcopy(cur_sol)

		print "The minimum avg rank is " + str(min_rank)
		min_sol_projects = [p for p in min_sol if len(p.students) > 0]
		print "The returned solution has an avg rank of " + str(calculate_avg_rank(min_sol_projects, verbose = False))
		return min_sol_projects

def do_greedy_initial_solutions(students, all_projects, annealer, project_id_mappings, verbose = False):
		'''
			Creates the feasible projects, and iterates 1000 (default number) of greedy 
			solutions, randomizing the order in which students get their "first pick."

			Returns the solution with the lowest initial energy.
			Result is usually very good.
		'''

		configParser = ConfigParser.ConfigParser()
		configFilePath = r'config.txt'
		configParser.read(configFilePath)

		# Declaring valid values for all fields.
		num_MBAs = configParser.getint('valid_values', 'num_MBAs')
		num_MEngs = configParser.getint('valid_values', 'num_MEngs')

		feasible_projects = util.create_feasible_projects(students, all_projects, verbose)
		util.input_checks(students, feasible_projects, num_MBAs, num_MEngs, project_id_mappings, sorted = False) 

		sol = greedy_solutions_and_goodness(students, feasible_projects)
		print [p.ID for p in sol]
		return sol