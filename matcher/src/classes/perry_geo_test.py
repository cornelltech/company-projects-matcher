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
	#print [s.ID for s in feasible_projects]


	#Get projects from IDs 2860, 4225, 1820.
	#cur_project = util.get_project_from_ID(cur_project_ID, feasible_projects)
	proj_one = util.get_project_from_ID(2275, feasible_projects)
	proj_two = util.get_project_from_ID(1625, feasible_projects)
	proj_three = util.get_project_from_ID(1235, all_projects)

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
	#print "Student 3922650 has rankings" + str(r_one.project_rankings)
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
	
	# This is the number of total votes cast.
	print sum(sorted_projects)

	print "For project 1235: " + str(util.get_num_ranked(proj_three, students))

	def calc(x):
		return round((x/13.0) * 72)
	mapped =  map(calc, sorted_projects)
	#print mapped
	#print "There are " + str(len(filter(lambda v: v == 0.0, mapped))) + "zeros"

	# How many students out of 72 would rank it
	#print mapped

	# If there were x occurrences of a # of times ranked for 13 students, scale up to 80
	# TODO: what is this magical fraction i'm multiplying by?
	already_seen = []
	def count(x, lst = mapped):
		if (not(x in already_seen)):
			contained = filter(lambda v: x == v, lst)
		#	print "length of contained is " + str(len(contained))
			already_seen.append(x)
			return round(len(contained) * (75.0/60.0))
	
	calculated = map(count, mapped)
	no_nones = filter(lambda x: not(x is None), calculated)
	#print "Calculated is " + str(no_nones)
	a = sum(no_nones)
	#print "There are " + str(a) + "projects"
	print "Number of votes: number of projects"
	for i in range(0, len(calculated)):
		if (not(calculated[i] is None)):
			print "There should be " + str(int(calculated[i])) + " projects with " + str(int((mapped[i]))) + " votes"

	# sol = greedy_attempt_two.make_initial_solution(students, feasible_projects)	
	# state = (sol, [])

	# # Automatically calculate the annealing schedule and anneal using this schedule.
	# schedule = annealer.auto(state, 1)

	# state, e = annealer.anneal(state, schedule['tmax'], schedule['tmin'], 
	#                              schedule['steps'])


	# # Manually set the annealing schedule.
	# #state, e = annealer.anneal(state, 1000000, 0.01, 54000, updates=0)
	
 # 	# state is the "final" solution
 # 	print "Final Solution:"
 # 	(projects, unmatched) = state
	# for p in projects:
	#  	print str(p.ID) + ": " + str([s.ID for s in p.students])
	# print "Final Energy: " + str(e) 


	# print "Annealing Schedule:"
	# print "Tmax: " + str(schedule['tmax'])
	# print "Tmin: " + str(schedule['tmin'])
	# print "Steps: " + str(schedule['steps'])
