import util
import ConfigParser
import perry_geo_annealing_diversity as pgd
import perry_geo_test as test

from anneal import Annealer

if (__name__ == "__main__"):
	'''
		Simulated annealing solution to creating diverse teams.

		A format for describing the state of the system:
		------------------------------------------------
		'students' is a list of Students (created from the given input file).

		'state' is a tuple of (Project list, numpy.ndarray) where:
			- Project list:
				- Each project is assigned some number of students
				(can be changed in classes/Project.)
				- At any given point, 'state' tells us what the current state of
				  the system is (i.e. which Students are with which Projects.)
			- numpy.ndarray:
				- This is the inverse of the covariance matrix of the students' data.
				  This is necessary for calculating their Mahalanobis distance.

		Desired postconditions:
			- Each student is matched to exactly one project.
			- Each project has its desired number and makeup of students:
				Ex. 2 MBA, 2 MEng

		The function to be minimized is the energy of the state (energy(state)).
		In our case, energy calculates the similarity of teams.

	'''

	configParser = ConfigParser.ConfigParser()
	configFilePath = r'config.txt'
	configParser.read(configFilePath)

	input_file = configParser.get('files', 'perry_geo_main_file')
	num_MBAs = configParser.getint('valid_values', 'num_MBAs')
	num_MEngs = configParser.getint('valid_values', 'num_MEngs')
	team_size = num_MBAs + num_MEngs

	# Creating the annealer with our energy and move functions.
	annealer = Annealer(pgd.energy, pgd.move)
	all_projects = util.generate_all_projects()
	students = util.create_students_from_input("eighty_students.csv")

	sol = test.do_greedy_initial_solutions(students, all_projects, annealer)
	test.manual_schedule(False, students, sol, annealer)



