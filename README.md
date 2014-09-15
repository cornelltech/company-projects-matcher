company-projects-matcher
========================

The matching algorithm for [Company Projects: CS 5999] (http://tech.cornell.edu/experience/company-projects/).

Dependencies
------------
###Installation of Python
This software requires an installation of Python. It was written and tested in Python 2.7.6. Earlier versions of Python seem to be ok, as Python 2.7 has some backwards compatibility. However, there are some key [differences](https://wiki.python.org/moin/Python2orPython3) between Python 2 and Python 3 that could cause problems. To be safe, Python 2.7 (specifically 2.7.6) is recommended.

###Packages
This software also relies on various Python packages, including numpy and pandas, among others. Installing these packages separately and resolving the dependencies can be difficult; therefore, a tool like Anaconda Scientific Python distribution is helpful. Anaconda is a collection of over 195 of the “most popular Python packages for science, math, engineering, data analysis” (according to their [homepage] (https://store.continuum.io/cshop/anaconda/)). 

To install Anaconda for your appropriate platform, view [information and instructions](http://continuum.io/downloads).
For help with installation questions, check out the [Anaconda FAQ] (http://docs.continuum.io/anaconda/faq.html#install-maclinux).

As of August 14, 2014, Anaconda comes with installers for Python 2.7 and 3.4. When running the scripts that depend on Anaconda packages, make sure to use the version of Python installed by Anaconda. To find out which version of Python you are running, run "which python."

Folders
--------

[matcher] (https://github.com/cornelltech/company-projects-matcher/tree/master/matcher): Contains test data, classes, and code for performing the match. Contains files for creating teams of students matched to projects, or diverse teams of a given size. The matcher performs [simulated annealing] (http://en.wikipedia.org/wiki/Simulated_annealing), and uses [perrygeo](https://github.com/perrygeo)'s [implementation](https://github.com/perrygeo/python-simulated-annealing).



