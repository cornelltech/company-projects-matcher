import util
import perry_geo_annealing as pg
import ConfigParser
import perry_geo_test as test

from anneal import Annealer

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
	#Create a ConfigParser to get the filename.
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

	students = util.create_students_from_input("eighty_students.csv")
	sol = test.do_greedy_initial_solutions(students, all_projects, annealer)
	use_file = False
	use_diversity = False
	test.manual_schedule(use_file, students, sol, annealer,use_diversity)


