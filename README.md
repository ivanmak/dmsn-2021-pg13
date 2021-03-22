# dmsn-2021-pg13

## Table of Contents
* [Introduction](#introduction)
* [Technologies](#technologies)
* [Files](#files)
* [References](#references)

## Introduction
This is the GitHub repository for the coursework of ECS757 Digital Media and Social Network of group PG13, in the Spring Semester of 2021.

### Credits
This coursework makes use of the following works:
* Bitcoin OTC data set from https://snap.stanford.edu/data/soc-sign-bitcoin-otc.html
* REV2 algorithm from https://github.com/horizonly/Rev2-model (This coursework has modified the code so that it runs smoothly on Python 3)

## Technologies
The coursework is done with Python 3 withe the use of the following libraries:
* Pandas
* NumPy
* NetworkX
* Matplotlib
* Seaborn

## Files
Some notable files:
* bitcoinotc.ipynb: Basic network visualisations.
* temporal_networkx/temporal_networkx.py: A custom class that wraps the data set and NetworkX objects, with the functionality to slices the data to given interval, calculates fairness and goodness scores using REV2 algorithm, and draw network visualisation.
* temporal_graph.ipynb: Network statistics using the custom class.
* fairness_goodness_visualisation.ipynb: Network visualisation using the custom class.
* fairness_goodness_analysis.ipynb: Simulation of identifying and banning bad users.
* soc-sign-bitcoinotc.csv: The source data set.
* *.csv and user_stats.xlsx: Other network statistics derived from the data set.
* graphs/: output directory of graphs
* old/: history

## References
* S. Kumar, F. Spezzano, V.S. Subrahmanian, C. Faloutsos. Edge Weight Prediction in Weighted Signed Networks. IEEE International Conference on Data Mining (ICDM), 2016.
* S. Kumar, B. Hooi, D. Makhija, M. Kumar, V.S. Subrahmanian, C. Faloutsos. REV2: Fraudulent User Prediction in Rating Platforms. 11th ACM International Conference on Web Searchand Data Mining (WSDM), 2018.