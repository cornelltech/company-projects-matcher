Data Analysis
=====

[data](https://github.com/cornelltech/company-projects-matcher/tree/master/data_analysis/data): I sent out a survey to friends and faculty (included [here](https://github.com/cornelltech/company-projects-matcher/blob/master/data_analysis/data/info/link_to_survey.txt)), which asked questions about a variety of factors that I thought would differentiate students. Various versions of the responses to this survey are included in this folder.

[results](https://github.com/cornelltech/company-projects-matcher/tree/master/data_analysis/results): contains some results from runs of the data analysis files included in src. Results are displayed in text files.

[src](https://github.com/cornelltech/company-projects-matcher/tree/master/data_analysis/src): contains the code for analyses I performed.

Numerical
---------
[Clustering](http://en.wikipedia.org/wiki/Cluster_analysis): performs [k-means analysis](http://en.wikipedia.org/wiki/K-means_clustering) to partition data into clusters, where each data point is "similar" or "close" to the mean of its cluster. Performs [one-hot encoding](http://en.wikipedia.org/wiki/One-hot) on categorical data before analyzing.

[Distance](http://en.wikipedia.org/wiki/Mahalanobis_distance): calculates the [Mahalanobis distance](http://en.wikipedia.org/wiki/Mahalanobis_distance) between the students' feature vectors. Performs [one-hot encoding](http://en.wikipedia.org/wiki/One-hot) on categorical data before analyzing.

[Regression](http://en.wikipedia.org/wiki/Regression_analysis): aims to predict one variable based on the other variables. Performs [Ordinary Least Squares Analysis](http://en.wikipedia.org/wiki/Ordinary_least_squares) to calculate the relationships between variables.


Visualization
--------------
[Histogram](http://en.wikipedia.org/wiki/Histogram): creates histograms of the data (plots numerical data and color codes by the categorical data).

[Scatterplot](http://en.wikipedia.org/wiki/Scatterplot): creates scatterplots of data. Plots pairs of data against each other, to view how the individual variables correlate with one another.
