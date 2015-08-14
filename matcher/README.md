Matcher
==================


###Configuration
--------------
You are now required to pass in your own configuration file as a command line argument to the main program.
The config file allows us to specify certain parameters, including team size, number of projects, number of rankings that students have, and paths to certain files that we will read data from. Various different files read from the config file, including classes.py and ranked_teams_main.py.

The configuration file must comply with the following format:

[valid_values]
use_binary = True|False
duplicate_rankings = True|False
match_all = True|False
max_work_experience = [int]
max_coding_ability = [int]

max_business_ability = [int]
num_valid_projects = [int]
number_project_rankings = [int]
capacity = [int]
capacity_w = [int >= capacity]

[files]
project_id_mappings = [*.csv]

use_binary indicates whether the program should give the students an extra binary field (like gender and other things) for the purposes of diversity.
Only one binary field is supported at this time. Future versions may allow for multiple binary fields (e.g. gender AND native NYer/nonlocal) 

duplicate_rankings indicates whether the program should duplicate each student's rankings. This should be set True in the case of company challenges, where each
project may have up to two teams that match to it. Future versions may allow for the user to prohibit specific projects from having two teams.

match_all indicates whether the program needs to match all the students to a project/group. This should be set True if we require all students to match.

max_work_experience, max_coding_ability, and max_business_ability: self-explanatory

capacity is the absolute minimum number of students required to form a valid team.
capacity_w ("wiggle" capacity) is the absolute maximum of students that may be on a valid team.

project_id_mappings should be the name of a csv file containing a single column of project/group IDs and a second column for their associated names.

An example of a valid configuration file can be found in the src folder.

###Code
-----

Currently, all code for the algorithm is included in the srcs folder. 

There are four different types of modules in the classes folder:

* perrygeo's modules: i.e. anneal.py. I am using the simulated annealing implementation written by perrygeo (linked to in the project README.md). So, I have copied and pasted his modules into this folder so that I may include and import them in my files.

* Class modules: i.e. classes.py. These modules contain implementations of classes that will be useful to our algorithm. Classes.py, for example, contains the Student and Project classes, which are functional wrappers for the data that we would like to input to our algorithm.

* Function implementations: i.e. util.py, perry_geo_test.py, initial_solution.py. These files mainly contain implementations of functions, like creating all valid projects, reading students from input, and creating initial solutions for the simulated annealing algorithm.

* Main modules: i.e. diversity_main.py, ranked_teams_main.py. These modules contain the code that will extract data from relevant places and actually run the algorithms and functions written in the function implementation modules.


###Data
-----

Data is included in this folder as well. We can specify which files to read from in the config file, but files must follow the format shown by students.csv. The diverse subroutines will pull from config.txt also. 

We also must input the project name that corresponds with each ID, so that when we print the final results, we may see the project names and the students' names as well.

##Instructions

0. In ranked_teams_main.py, change the first line to be the appropriate location of Python on your computer.

1. Decide on the parameters for the problem, and set appropriate values in config.txt. How many MBA/MEng students would we like each team to have? What scales should our diversity metrics be on? For a complete list of parameters to consider, look at config.txt.

2. Assign an ID number for each project that students may rank. ID numbers must be in [1, number of projects], inclusive. 

3. Create a file (following the format of eighty_students.csv) with project IDs in the first column, and the corresponding project names in the second column. The information from this file will be extracted into a dictionary, and at the end of annealing, we will use this information to print the results in human-friendly manner.

4. Create or obtain data with information on students, their backgrounds, and their project rankings. Project rankings are entered in the form of Project ID. 

Make sure your input data is formatted correctly! Due to time constraints, the ONLY optional column for the student file input is the binary field column. All others are required. If you do not care about some fields, fill the columns with zeroes.

Example: Conversations in the studio cares only about gender and program for diversity. So fill in the work experience, business ability, and coding ability columns with zeroes.

All project rankings must be valid (described in #3) and students must select num_project_rankings *distinct* project IDs to include in his/her rankings.

	* If you are trying to create diverse teams, you can use the exact same file that you would use to match students to projects. The diversity algorithm also relies on Project and Student objects, but ignores the student rankings as part of the energy function. Each team is assigned to a "project" -- this name is purely for organizational purposes, so that we can group the students easily.

	* Note: when number of project rankings changes, so will the exact configuration of the input test file that you will have to input. eighty_students.csv is just a rough model of what the data should look like (with 10 examples, currently).

5. Run the main files -- for creating teams with the project rankings, the format is ./ranked_teams_main.py -i <inputfile> [-o <outputfile>] -m [cc|co] -c <configfile>.

cc and co tell the annealer which energy+move functions to use. cc is based on company challenges, and so moves involve both students and projects; co is based on conversations in the studio, so moves involve only students.

Use cc if you are using the algorithm for company challenges. Use co if you are using the algorithm for conversations in the studio.  


