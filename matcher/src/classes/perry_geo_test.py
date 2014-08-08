import util
import greedy_attempt_two
import perry_geo_annealing as pg
import ConfigParser
import sys
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
	#print "All students:"
	#print [s.ID for s in students]
	all_projects = util.generate_all_projects()
	#print "All projects:"
	#print [p.ID for p in all_projects]
	feasible_projects = util.create_feasible_projects(students, all_projects)
	#print [s.ID for s in feasible_projects]

	#Get projects from IDs 2860, 4225, 1820.
	#cur_project = util.get_project_from_ID(cur_project_ID, feasible_projects)
	# NOTE: the following code is problematic because we dont always know if these projects are feasible.
	proj_one = util.get_project_from_ID(2275, all_projects)
	#print util.get_num_ranked(proj_one, students)
	#proj_two = util.get_project_from_ID(1625, feasible_projects)
	#proj_three = util.get_project_from_ID(1235, all_projects)

	# Print the cost of this
	#fake_state = ([proj_one, proj_two, proj_three], [])
	#print pg.energy(fake_state)

	# Do we want to pass in only the feasible prjoects here?

#	sorted_projects = util.sort_projects_by_demand(students, all_projects)
	
	def make_data_for_80_students():
		sorted_projects = util.sort_projects_by_demand(students, all_projects, tup=True)
		print "Sorted projects is " + str(sorted_projects)

		# This is the number of total votes cast.
		print "There were " + str(sum([tup[0]*tup[1] for tup in sorted_projects])) + " total votes cast"
		print "There are " + str(sum([tup[1] for tup in sorted_projects])) + " total orig projects"

		#print "For project 1235: " + str(util.get_num_ranked(proj_three, students))

		# Input x is the number of students out of 13 who voted each project.
		# Comes from sorted_projects
		# This is number of students who would vote on the project but there are not the same 
		# # of projects

		def scale(tup):
			num_votes = tup[0]
			num_projects = tup[1]
			scaled_votes = round ((num_votes * (72.0 / 13.0)))
			scaled_projects = round ((num_projects) * (75.0 / 55.0))
			return (scaled_votes, scaled_projects)
		scaled_tups = map(scale, sorted_projects)

		for tup in scaled_tups:
			print "There were " + str(tup[1]) + " projects with " + str(tup[0]) + " votes"

		num_projects = sum([tup[1] for tup in scaled_tups])
		print "Scaled tups is " + str(scaled_tups)
		print "There are " + str(num_projects) + " final projects"
		print "There were " + str(sum([tup[0]*tup[1] for tup in scaled_tups])) + " total votes cast"

		return scaled_tups


	def random_solutions_and_goodness(num_times = 100000):
		min_energy = float("inf")
		min_sol = None
		for i in range (0, num_times):
			init = greedy_attempt_two.make_initial_solution(students, feasible_projects, num_MBAs, num_MEngs)
		#	print "There are  " + str(len(feasible_projects)) + " feasible projects"
			print "Random solution " + str(i) + ":"
			for p in init:
				print str(p.ID) + ":" + str([s.ID for s in p.students])
			cur_energy = pg.energy((init, []))
			if (cur_energy < min_energy):
				min_sol = init
		print cur_energy
		for p in min_sol:
				print str(p.ID) + ":" + str([s.ID for s in p.students])

	def test_random_solutions_and_goodness():
		#random_solutions_and_goodness
 		res = greedy_attempt_two.initial_solution(students, feasible_projects)
 		res_two = greedy_attempt_two.randomly_add_unmatched_students(res)
 		print res_two

 	def make_students_to_fit_data(scaled_projects):
 		all_projects = util.generate_all_projects()
 		remaining_num_MBAs = 37
 		remaining_num_MEngs = 35
 		projects_taken = []
 		for tup in scaled_projects:
 			num_votes = tup[0]
 			num_projects = tup[1]
 			for (i in range(0, num_projects)):
 				
 		pass


 	scaled_projects = make_data_for_80_students()
 	make_students_to_fit_data(scaled_projects)

	


