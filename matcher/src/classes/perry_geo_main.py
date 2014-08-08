import util
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
	all_projects = util.generate_all_projects()
	feasible_projects = greedy_attempt_two.create_feasible_projects(students, all_projects)
	print [s.ID for s in feasible_projects]


	#Get projects from IDs 2860, 4225, 1820.
	#cur_project = util.get_project_from_ID(cur_project_ID, feasible_projects)
	proj_one = util.get_project_from_ID(2275, feasible_projects)
	proj_two = util.get_project_from_ID(1625, feasible_projects)
	proj_three = util.get_project_from_ID(1820, feasible_projects)

	# Get students from IDs.
	# Project one students
	s_one = util.get_student_from_ID(4102938, students)
	s_two = util.get_student_from_ID(8291021, students)
	s_three = util.get_student_from_ID(4990324, students)
	s_four = util.get_student_from_ID(6249314, students)
	#s_five = util.get_student_from_ID(5092102, students)

	proj_one.students.append(s_one)
	proj_one.students.append(s_two)
	proj_one.students.append(s_three)
	proj_one.students.append(s_four)
	#proj_one.students.append(s_five)

	t_one = util.get_student_from_ID(5467123, students)
	t_two = util.get_student_from_ID(7894231, students)
	t_three = util.get_student_from_ID(8888888, students)
	t_four = util.get_student_from_ID(5092102, students)
	t_five = util.get_student_from_ID(3333333, students)

	proj_two.students.append(t_one)
	proj_two.students.append(t_two)
	proj_two.students.append(t_three)
	proj_two.students.append(t_four)
	proj_two.students.append(t_five)


	r_one = util.get_student_from_ID(3922650, students)
	r_two = util.get_student_from_ID(2886650, students)
	r_three = util.get_student_from_ID(1678231, students)
	r_four = util.get_student_from_ID(9191919, students)
	#r_five = util.get_student_from_ID(6666666, students)

	proj_three.students.append(r_one)
	proj_three.students.append(r_two)
	proj_three.students.append(r_three)
	proj_three.students.append(r_four)
	#proj_three.students.append(r_five)

	# Print the cost of this
	fake_state = ([proj_one, proj_two, proj_three], [])
	#print pg.energy(fake_state)

	# Do we want to pass in only the feasible prjoects here?
	

	sorted_projects = util.sort_projects_by_demand(students, all_projects)

	sol = greedy_attempt_two.make_initial_solution(students, feasible_projects)	
	

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
	
 
	



	
