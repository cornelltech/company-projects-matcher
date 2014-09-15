#!/usr/bin/env python

import util
import ConfigParser
import perry_geo_annealing_diversity as pgd
import perry_geo_test as test
import time
import initial_solution

import sys, getopt

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
	start_time = time.time()

	try:
		argv = sys.argv[1:]
		opts, args = getopt.getopt(argv, "i:o:n:", ["input", "output", "numteams"])
	except (getopt.GetoptError):
		print "Unrecognized arguments."
		print " usage: ./diversity_main.py -i <inputfile> [-o <outputfile>] -n <numteams>"
		sys.exit(2)

	set_input_file = False
	set_output_file = False
	set_num_teams = False

	for opt, arg in opts:
		if (opt == "-i"):
			input_file = arg
			set_input_file = True
		elif (opt == "-o"):
			output_file = arg
			set_output_file = True
		elif (opt == "-n"):
			num_teams = int(arg)
			set_num_teams = True

	if (not(set_input_file)):
		print "Please specify an input file."
		print " usage: ./diversity_main.py -i <inputfile> [-o <outputfile>] -n <numteams>"
		sys.exit(2)

	if (not(set_num_teams)):
		print "Please specify the number of teams to create."
		print " usage: ./diversity_main.py -i <inputfile> [-o <outputfile>] -n <numteams>"

	# Create config parser to get various fields.
	configParser = ConfigParser.ConfigParser()
	configFilePath = r'config.txt'
	configParser.read(configFilePath)

	project_id_mappings = configParser.get('files', 'project_id_mappings')
	num_MBAs = configParser.getint('valid_values', 'num_MBAs')
	num_MEngs = configParser.getint('valid_values', 'num_MEngs')
	team_size = num_MBAs + num_MEngs

	# Creating the annealer with our energy and move functions.
	annealer = Annealer(pgd.energy, pgd.move)
	all_projects = util.generate_all_projects()
	students = util.create_students_from_input(input_file)

	sol = initial_solution.random_initial_solution_for_diversity(students, all_projects, num_teams)	

	use_diversity = True
	use_file = False
	if (set_output_file):
		test.manual_schedule(use_file, students, sol, annealer, use_diversity, input_file, output_file)
	else:
		test.manual_schedule(use_file, students, sol, annealer, input_file, use_diversity)

	string =  "Program completed in " + str((time.time() - start_time)/60)
	string += " minutes."
	print string




