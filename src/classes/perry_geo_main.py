import all_pairs_sorted
import greedy_attempt_two
import perry_geo_annealing as pg

input_file = "tests.csv"

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
	# Format for describing the state of the system.
	students = greedy_attempt_two.create_students_from_input(input_file)
	
	# Do we want to pass in only the feasible prjoects here?
	all_projects = all_pairs_sorted.generate_all_projects()

	# state = greedy_attempt_two.initial_solution(students, all_projects)
	# print perry_geo_annealing.energy(state)
	# perry_geo_annealing.move(state)
	# projects = state[0]
	# unmatched_students = state[1]
	# greedy_attempt_two.print_students_and_waiting(projects)
	# print "Unmatched"
	# print [s.ID for s in unmatched_students]

	sol = greedy_attempt_two.random_initial_solution(students, all_projects)
	print "INITIAL SOLUTION:"
	for p in sol:
		print str(p.ID) + ": " + str([s.ID for s in p.students])
	state = (sol, [])
	projects = pg.move(state)
	sol = state[0]
	# print "AFTER MOVE:"
	# for p in projects:
	# 	print str(p.ID) + ": " + str([s.ID for s in p.students])



	# print perry_geo_annealing.energy(state)

	# n = 500
	# while (n > 0):
	# 	perry_geo_annealing.move(state)
	# 	sol = state[0]
	# 	print perry_geo_annealing.energy(state)
	# 	n -= 1






