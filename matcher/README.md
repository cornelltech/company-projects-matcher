Matcher
==================


###Configuration
--------------
The most important file in the classes folder is config.txt. Config.txt allows us to specify certain parameters, including team size, number of projects, number of rankings that students have, and paths to certain files that we will read data from. Various different files read from config.txt, including classes.py and ranked_teams_main.py

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

Data is included in this folder as well. We can specify which files to read from in config.txt, but files must follow the format shown by eighty_students.csv. The diverse subroutines will pull from config.txt also. 

We also must input the project name that corresponds with each ID, so that when we print the final results, we may see the project names and the students' names as well.

##Instructions

0. In diversity_main.py and ranked_teams_main.py, change the first line to be the appropriate location of Python on your computer.

1. Decide on the parameters for the problem, and set appropriate values in config.txt. How many MBA/MEng students would we like each team to have? What scales should our diversity metrics be on? For a complete list of parameters to consider, look at config.txt.

2. Assign an ID number for each project that students may rank. ID numbers must be in [1, number of projects], inclusive. 

3. Create a file (following the format of eighty_students.csv) with project IDs in the first column, and the corresponding project names in the second column. The information from this file will be extracted into a dictionary, and at the end of annealing, we will use this information to print the results in human-friendly manner.

4. Create or obtain data with information on students, their backgrounds, and their project rankings. Project rankings are entered in the form of Project ID. Make sure that this data follows the format of the example data in eighty_students.csv. All project rankings must be valid (described in #3) and students must select num_project_rankings *distinct* project IDs to include in his/her rankings.

	* If you are trying to create diverse teams, you can use the exact same file that you would use to match students to projects. The diversity algorithm also relies on Project and Student objects, but ignores the student rankings as part of the energy function. Each team is assigned to a "project" -- this name is purely for organizational purposes, so that we can group the students easily.

	* Note: when number of project rankings changes, so will the exact configuration of the input test file that you will have to input. eighty_students.csv is just a rough model of what the data should look like (with 10 examples, currently).

5. Run the main files -- for creating teams with the project rankings, the format is ./ranked_teams_main.py -i <inputfile> [-o <outputfile>]; for creating diverse teams, do ./diversity_main.py -i <inputfile> [-o <outputfile>].  


