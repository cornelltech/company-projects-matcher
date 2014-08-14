Matcher
==================

##Overview
[classes.py](https://github.com/cornelltech/company-projects-matcher/blob/master/matcher/src/classes/classes.py)

###Configuration
--------------
The most important file in the classes folder is config.txt. Config.txt allows us to specify certain parameters, including team size, number of projects, number of rankings that students have, and paths to certain files that we will read data from. Various different files read from config.txt, including classes.py and ranked_teams_main.py

###Code
-----

Currently, all code for the algorithm is included in the classes folder. This might change soon.

There are four different types of modules in the classes folder:

* perrygeo's modules: i.e. anneal.py. I am using the simulated annealing implementation written by perrygeo (linked to in the project README.md). So, I have copied and pasted his modules into this folder so that I may include and import them in my files.

* Class modules: i.e. classes.py. These modules contain implementations of classes that will be useful to our algorithm. Classes.py, for example, contains the Student and Project classes, which are functional wrappers for the data that we would like to input to our algorithm.

* Function implementations: i.e. util.py, perry_geo_test.py, initial_solution.py. These files mainly contain implementations of functions, like creating all valid projects, reading students from input, and creating initial solutions for the simulated annealing algorithm.

* Main modules: i.e. diversity_main.py, ranked_teams_main.py. These modules contain the code that will extract data from relevant places and actually run the algorithms and functions written in the function implementation modules.


###Data
-----

Data is included in this folder as well. We can specify which files to read from in config.txt, but files must follow the format shown by eighty_students.csv. The diverse subroutines will pull from config.txt also (the exact same file as perry_geo_main_file). 

We also must input the project name that corresponds with each ID, so that when we print the final results, we may see the project names and the students' names as well.

##Instructions