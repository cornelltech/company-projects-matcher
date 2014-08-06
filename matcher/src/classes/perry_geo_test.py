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
	num_MBAs = configParser.getint('valid_values', 'num_MBAs')
	num_MEngs = configParser.getint('valid_values', 'num_MEngs')
	team_size = num_MBAs + num_MEngs

	# Creating the annealer with our energy and move functions.
	annealer = Annealer(pg.energy, pg.move)

	# Format for describing the state of the system.
	students = util.create_students_from_input(input_file)
	print "All students:"
	print [s.ID for s in students]
	all_projects = util.generate_all_projects()
	print "All projects:"
	print [p.ID for p in all_projects]
	# Bug in create_feasible_projects
	feasible_projects = greedy_attempt_two.create_feasible_projects(students, all_projects)
	#print [s.ID for s in feasible_projects]

	#Get projects from IDs 2860, 4225, 1820.
	#cur_project = util.get_project_from_ID(cur_project_ID, feasible_projects)
	# NOTE: the following code is problematic because we dont always know if these projects are feasible.
	proj_one = util.get_project_from_ID(2275, all_projects)
	print util.get_num_ranked(proj_one, students)
	#proj_two = util.get_project_from_ID(1625, feasible_projects)
	#proj_three = util.get_project_from_ID(1235, all_projects)

	# Print the cost of this
	#fake_state = ([proj_one, proj_two, proj_three], [])
	#print pg.energy(fake_state)

	# Do we want to pass in only the feasible prjoects here?

	sorted_projects = util.sort_projects_by_demand(students, all_projects)
	
	def make_data_for_80_students():
	
		# This is the number of total votes cast.
		print sum(sorted_projects)

		#print "For project 1235: " + str(util.get_num_ranked(proj_three, students))

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
		print "There are " + str(a) + "projects"
		print "Number of votes: number of projects"
		for i in range(0, len(calculated)):	
			if (not(calculated[i] is None)):
				print "There should be " + str(int(calculated[i])) + " projects with " + str(int((mapped[i]))) + " votes"	

	def random_solutions_and_goodness(num_times = 1):
		for i in range (0, num_times):
			init = greedy_attempt_two.make_initial_solution(students, feasible_projects, num_MBAs, num_MEngs)
			print "There are  " + str(len(feasible_projects)) + " feasible projects"
			print "This random solution is: "
			for p in init:
				print str(p.ID) + ":" + str([s.ID for s in p.students])

	random_solutions_and_goodness()







