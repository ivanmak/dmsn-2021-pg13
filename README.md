# dmsn-2021-pg13

## Table of Contents
* [Introduction](#introduction)
* [Technologies](#technologies)
* [Files](#files)
* [References](#references)

## Introduction
This is the GitHub repository for the coursework of ECS757 Digital Media and Social Network of group PG13, in the Spring Semester of 2021.

It makes use of a data set of the ratings among users on Bitcoin OTC marketplace and simulates the effects of banning users based on their goodness scores, calculated by the REV2 algorithm (see below for references), instead of purely based on the ratings they received.

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
* [bitcoinotc.ipynb](https://github.com/ivanmak/dmsn-2021-pg13/blob/main/bitcoinotc.ipynb): Basic network visualisations and statistics generated during early stage of the coursework.
* [temporal_networkx/temporal_networkx.py](https://github.com/ivanmak/dmsn-2021-pg13/blob/main/temporal_networkx/temporal_networkx.py): A custom class that wraps the data set and NetworkX objects, with the functionality to slices the data to given interval, calculates fairness and goodness scores using REV2 algorithm, and draw network visualisation.
* [temporal_graph.ipynb](https://github.com/ivanmak/dmsn-2021-pg13/blob/main/temporal_graph.ipynb): Network statistics using the custom class.
* [fairness_goodness_visualisation.ipynb](https://github.com/ivanmak/dmsn-2021-pg13/blob/main/fairness_goodness_visualisation.ipynb): Network visualisation using the custom class.
* [simulation.ipynb](https://github.com/ivanmak/dmsn-2021-pg13/blob/main/simulation.ipynb): Simulation of identifying and banning bad users.
* [simulation_plots.ipynb](https://github.com/ivanmak/dmsn-2021-pg13/blob/main/simulation_plots.ipynb): Some plots of the simulation results in a separate notebook.
* [soc-sign-bitcoinotc.csv](https://github.com/ivanmak/dmsn-2021-pg13/blob/main/soc-sign-bitcoinotc.csv): The source data set.
* *.gpickle: The pickled MultiDiGraph objects for graph drawing without re-running the algorithms.
* *.csv and *.xlsx: Other network statistics derived from the data set, generated from the Jupyter Notebooks.
* graphs/: output directory of graphs
* old/ : history

## References
* S. Kumar, F. Spezzano, V.S. Subrahmanian, C. Faloutsos. [Edge Weight Prediction in Weighted Signed Networks](http://cs.stanford.edu/~srijan/pubs/wsn-icdm16.pdf). IEEE International Conference on Data Mining (ICDM), 2016.
* S. Kumar, B. Hooi, D. Makhija, M. Kumar, V.S. Subrahmanian, C. Faloutsos. [REV2: Fraudulent User Prediction in Rating Platforms](http://cs.stanford.edu/~srijan/pubs/rev2-wsdm18.pdf). 11th ACM International Conference on Web Searchand Data Mining (WSDM), 2018.