import all_pairs_sorted
import greedy_attempt_two
import perry_geo_annealing as pg
import ConfigParser
from anneal import Annealer

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

	# Creating the annealer with our energy and move functions.
	annealer = Annealer(pg.energy, pg.move)

	# Format for describing the state of the system.
	students = greedy_attempt_two.create_students_from_input(input_file)

	for student in students:
		rank = student.get_ranking(1820)
		print str(student.ID) + ": " + str(rank)
		print "\t Cost : " + str(student.get_cost_from_ranking(rank))

	
	# Do we want to pass in only the feasible prjoects here?
	all_projects = all_pairs_sorted.generate_all_projects()

	# sorted_projects = all_pairs_sorted.sort_projects_by_demand(students, all_projects)

	# print [project.ID for project in sorted_projects]

	feasible_projects = greedy_attempt_two.create_feasible_projects(students, all_projects)

	sol = greedy_attempt_two.make_initial_solution(students, feasible_projects)	
	state = (sol, [])

	# Automatically calculate the annealing schedule and anneal using this schedule.
	schedule = annealer.auto(state, 1)


	state, e = annealer.anneal(state, schedule['tmax'], schedule['tmin'], 
	                             schedule['steps'], updates=6)


	# Manually set the annealing schedule.
	#state, e = annealer.anneal(state, 1000000, 0.01, 54000, updates=0)
	#state, e = annealer.anneal(randState, 10000000, 0.01,
     #  18000 * len(randState), 9)
	
 	# state is the "final" solution
 	print "Final Solution:"
 	(projects, unmatched) = state
	for p in projects:
	 	print str(p.ID) + ": " + str([s.ID for s in p.students])
	print "Final Energy: " + str(e) 


	print "Annealing Schedule:"
	print "Tmax: " + str(schedule['tmax'])
	print "Tmin: " + str(schedule['tmin'])
	print "Steps: " + str(schedule['steps'])
