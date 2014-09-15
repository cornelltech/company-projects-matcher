#!/usr/bin/env python 

import util
import perry_geo_annealing as pg
import ConfigParser
import perry_geo_test as test
import time

import sys, getopt

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
	start_time = time.time()

	try:
		argv = sys.argv[1:]
		opts, args = getopt.getopt(argv, "i:o:", ["input", "output"])
	except (getopt.GetoptError):
		print "Unrecognized arguments."
		print " usage: ./ranked_teams_main.py -i <inputfile> [-o <outputfile>]"
		sys.exit(2)

	set_input_file = False
	set_output_file = False

	for opt, arg in opts:
		if (opt == "-i"):
			input_file = arg
			set_input_file = True
		elif (opt == "-o"):
			output_file = arg
			set_output_file = True

	if (not(set_input_file)):
		print "Please specify an input file."
		print " usage: ./ranked_teams_main.py -i <inputfile> [-o <outputfile>]"
		sys.exit(2)

	# Create a ConfigParser to get various fields from the config file.
	configParser = ConfigParser.ConfigParser()
	configFilePath = r'config.txt'
	configParser.read(configFilePath)

	project_id_mappings = configParser.get('files', 'project_id_mappings')
	num_MBAs = configParser.getint('valid_values', 'num_MBAs')
	num_MEngs = configParser.getint('valid_values', 'num_MEngs')
	team_size = num_MBAs + num_MEngs

	# Creating the annealer with our energy and move functions.
	annealer = Annealer(pg.energy, pg.move)
	all_projects = util.generate_all_projects()
	students = util.create_students_from_input(input_file)
	
	sol = test.do_greedy_initial_solutions(students, all_projects, annealer, project_id_mappings)
	use_file = False
	use_diversity = False
	if (set_output_file):
		test.manual_schedule(use_file, students, sol, annealer, use_diversity, input_file, output_file)
	else:
		test.manual_schedule(use_file, students, sol, annealer, use_diversity, input_file)

	string =  "Program completed in " + str((time.time() - start_time)/60)
	string += " minutes."
	print string




