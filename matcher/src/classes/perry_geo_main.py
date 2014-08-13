import util
import initial_solution
import perry_geo_annealing as pg
import ConfigParser
from anneal import Annealer

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
	students = initial_solution.create_students_from_input(input_file)
	all_projects = util.generate_all_projects()
	feasible_projects = initial_solution.create_feasible_projects(students, all_projects)
	print [s.ID for s in feasible_projects]

	sorted_projects = util.sort_projects_by_demand(students, all_projects)

	sol = initial_solution.make_initial_solution(students, feasible_projects)	

	def print_final_solution(state):
		print "Final Solution:"
 		(projects, unmatched) = state
		for p in projects:
		 	print str(p.ID) + ": " + str([s.ID for s in p.students])

	# Automatically calculate the annealing schedule and anneal using this schedule.
	def auto_schedule():
		state = (sol, [])
		schedule = annealer.auto(state, 1)

		state, e = annealer.anneal(state, schedule['tmax'], schedule['tmin'], 
	    	                        schedule['steps'])

		print_final_solution(state)

		print "Annealing Schedule:"
		print "Tmax: " + str(schedule['tmax'])
		print "Tmin: " + str(schedule['tmin'])
		print "Steps: " + str(schedule['steps'])

		print "Final Energy: " + str(e) 

	def manual_schedule(sol):
		state = (sol, [])
		# Manually set the annealing schedule.
		state, e = annealer.anneal(state, 1000000, 0.01, 54000, updates=0)
		print_final_solution(state)

	manual_schedule(sol)
	
 
	



	
