company-projects-matcher
========================

The matching algorithm for [Company Projects: CS 5999] (http://tech.cornell.edu/experience/company-projects/).

Dependencies
------------
This software requires an installation of Python. It was written and tested in Python 2.7.6. Earlier versions of Python seem to be ok, as Python 2.7 has some backwards compatibility. However, there are some key [differences](https://wiki.python.org/moin/Python2orPython3) between Python 2 and Python 3 that could cause problems. To be safe, install the same working version of Python as I have (2.7.6).


After installing Python itself, we must look to Python packages, or code extensions of the core functionality that python offers. This software relies on various Python packages, including numpy, pandas, and matplotlib, among others. Installing these packages separately and resolving the dependencies can be difficult; therefore, I recommend installing Anaconda Scientific Python distribution, which installs over 195 of the “most popular Python packages for science, math, engineering, data analysis” (according to their [homepage] (https://store.continuum.io/cshop/anaconda/)).

So, the first step is to install Anaconda for your appropriate platform. Information and instructions are [here](http://continuum.io/downloads).
Note: If you are having any issues, check out the [Anaconda FAQ] (http://docs.continuum.io/anaconda/faq.html#install-maclinux).

[data analysis:] (https://github.com/cornelltech/company-projects-matcher/tree/master/data_analysis) Contains the initial survey sent out to faculty and friends, and contains code and results of data analysis on the survey responses. 

[matcher] (https://github.com/cornelltech/company-projects-matcher/tree/master/matcher): Contains test data, classes, and code for performing the match. The matcher performs [simulated annealing] (http://en.wikipedia.org/wiki/Simulated_annealing), and uses [perrygeo](https://github.com/perrygeo)'s [implementation](https://github.com/perrygeo/python-simulated-annealing).



