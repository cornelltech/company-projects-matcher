#!/usr/bin/env python 

import util
import classes
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
			- Each project is sufficiently diverse
				Ex. >=1 MBA, 1 MEng per team, at least one person with >=3 years of work exp, etc.

		The function to be minimized is the energy of the state (energy(state)).
		In our case, energy calculates the cost of assigning people to projects.

	'''
	start_time = time.time()

	try:
		argv = sys.argv[1:]
		opts, args = getopt.getopt(argv, "i:o:m:c:", ["input", "output", "mode", "config"])
	except (getopt.GetoptError):
		print "Unrecognized arguments."
		print " usage: ./ranked_teams_main.py -i <inputfile> [-o <outputfile>] -m [cc|co] -c <configfile>"
		sys.exit(2)

	set_input_file = False
	set_output_file = False
        set_mode = False
        set_config = False

	for opt, arg in opts:
		if (opt == "-i"):
			input_file = arg
			set_input_file = True
		elif (opt == "-o"):
			output_file = arg
			set_output_file = True
                elif (opt == "-m"):
                        mode = arg
                        set_mode = True
                elif (opt == "-c"):
                        config = arg
                        set_config = True
	if (not(set_input_file)):
		print "Please specify an input file."
		print " usage: ./ranked_teams_main.py -i <inputfile> [-o <outputfile>] -m [cc|co] -c <configfile>"
		sys.exit(2)
        if (not(set_mode)):
                print "Please specify a mode."
                print " usage: ./ranked_teams_main.py -i <inputfile> [-o <outputfile>] -m [cc|co] -c <configfile>"
                sys.exit(2)
        if (not(set_config)):
                print "Please specify a config file."
                sys.exit(2)
	# Create a ConfigParser to get various fields from the config file.
	configParser = ConfigParser.ConfigParser()
	configFilePath = config
	configParser.read(configFilePath)

        classes.init_classes(config)
        project_id_mappings = configParser.get('files', 'project_id_mappings')
        capacity = configParser.getint('valid_values', 'capacity')
        capacity_w = configParser.getint('valid_values', 'capacity_w')
        team_size = capacity

        # Creating the annealer with our energy and move functions.
        if mode == "cc":
                annealer = Annealer(pg.energy, pg.move)
        elif mode == "co":
                annealer = Annealer(pg.energy_co, pg.move_co)
        else:
                raise FieldError("Unknown algorithm mode")
        all_projects = util.generate_all_projects(config)

        students = util.create_students_from_input(input_file, config)
        feasibles = util.create_feasible_projects(students, all_projects)

        sol = test.do_greedy_initial_solutions(students, all_projects, annealer, project_id_mappings, config)
        use_file = False
        use_diversity = False
        if (set_output_file):
                test.manual_schedule(use_file, students, sol, feasibles,  annealer, use_diversity, input_file, output_file)
        else:
                test.manual_schedule(use_file, students, sol, feasibles,  annealer, use_diversity, input_file)

        string =  "Program completed in " + str((time.time() - start_time)/60)
        string += " minutes."
        print string




