import util
import greedy_attempt_two
import perry_geo_annealing as pg
import ConfigParser
import random_teams

from anneal import Annealer
import random
from classes import CompError
import perry_geo_main
import math

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
	#feasible_projects = util.create_feasible_projects(students, all_projects)
	
	
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
			#scaled_votes = round ((num_votes * (72.0 / 13.0) / 75 * 55) + 1)
			scaled_votes = round ((num_votes * (72.0 / 13.0)))
			scaled_projects = round ((num_projects) * (75.0 / 55.0))
			#scaled_projects = num_projects
			return (scaled_votes, scaled_projects)
		scaled_tups = map(scale, sorted_projects)

		for tup in scaled_tups:
			print "There were " + str(tup[1]) + " projects with " + str(tup[0]) + " votes"

		num_projects = sum([tup[1] for tup in scaled_tups])
		print "Scaled tups is " + str(scaled_tups)
		print "There are " + str(num_projects) + " final projects"

		print "There were " + str(sum([tup[0]*tup[1] for tup in scaled_tups])) + " total votes cast"

		return scaled_tups


	def random_solutions_and_goodness(students, feasible_projects, num_MBAs, num_MEngs, num_times = 100000):
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
				min_energy = cur_energy
		for p in min_sol:
			print str(p.ID) + ":" + str([s.ID for s in p.students])
		print "The minimum energy is " + str(min_energy)
		return [p for p in min_sol if len(p.students) > 0]

	def test_random_solutions_and_goodness():
		#random_solutions_and_goodness
 		res = greedy_attempt_two.initial_solution(students, feasible_projects)
 		res_two = greedy_attempt_two.randomly_add_unmatched_students(res)
 		print res_two

 	# Trying to make students to fit the data.
 	def make_students_to_fit_data(scaled_projects):
 		#all_projects = util.generate_all_projects()
 		remaining_num_MBAs = 37
 		remaining_num_MEngs = 35
 		MBAs = random_teams.create_random_MBAs(4, 4, remaining_num_MBAs, empty_ranks = True)
 		MEngs = random_teams.create_random_MEngs(4, 4, remaining_num_MEngs, empty_ranks = True)
 		random_teams.print_student_list(MBAs)
 		random_teams.print_student_list(MEngs)
 		projects_taken = []
 		students_taken = []
 		for tup in scaled_projects:
 			num_votes = tup[0]
 			num_projects = tup[1]
 			for i in range(0, int(num_projects)):
 				project = util.random_project(all_projects, projects_taken, reuse = False)
 				for i in range (0, int(num_votes)):
 					# These are the students that have already been assigned to this project.
 					already_picked = []
 					# Pick a random student
 					if (remaining_num_MBAs > 0 and remaining_num_MEngs > 0):
 						decider = random.randint(0, 1)
 						if (decider):
		 					lst = MBAs
		 					remaining_num_MBAs -= 1
		 				else:
		 					lst = MEngs
		 					remaining_num_MEngs -= 1
		 			elif (remaining_num_MBAs > 0):
		 				lst = MBAs
		 				remaining_num_MBAs -= 1
		 			elif (remaining_num_MEngs > 0):
		 				lst = MEngs
		 				remaining_num_MEngs -= 1
		 			else:
		 				error = "There are no students with empty ranking spots."
		 				raise CompError(error)

		 			student = util.random_student_lst(lst, already_picked, False)
		 			already_picked.append(student)
	 				
	 				# Get the student's ranking list
	 				# Get the top spot on the list
	 				# If the student is in students_taken, pick a new student.
	 				# If the student has spots left:
	 					# Assign this project's ID to the top spot on the list
	 				# If not:
	 					# Add this student to students_taken
 					pass
 		pass	

 	def print_final_solution(state):
		print "Final Solution:"
 		(projects, unmatched) = state
		for p in projects:
		 	print str(p.ID) + ": " + str([s.ID for s in p.students])

 	#scaled_projects = make_data_for_80_students()
 	#make_students_to_fit_data(scaled_projects)
 	def manual_schedule(sol):
		state = (sol, [])
		# Manually set the annealing schedule.
		state, e = annealer.anneal(state, 1000000, 0.01, 54000, updates=0)
		print_final_solution(state)
		print "Final energy is " + str(e)
		print "Calculated final energy is " + str(pg.energy(state))

	def do_random():
 		remaining_num_MBAs = 37
 		remaining_num_MEngs = 35
 		MBAs = random_teams.create_random_MBAs(4, 4, remaining_num_MBAs)
 		MEngs = random_teams.create_random_MEngs(4, 4, remaining_num_MEngs)
 		students = MBAs + MEngs

 		feasible_projects = util.create_feasible_projects(students, all_projects, verbose = True)
	 	sol = random_solutions_and_goodness(students, feasible_projects, 37, 35, num_times = 100000)
	 	
	 	manual_schedule(sol)

	make_data_for_80_students()

	


