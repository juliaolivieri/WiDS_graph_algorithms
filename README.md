# WiDS Graph Algorithms Code

## Workshop information

This repository contains the code for the WiDS lecture "Graph Theory for Data Science, Part II: Graph algorithms: Traversing the tree and beyond":

Graph-based algorithms are essential for everything from tracking relationships in social networks to finding the shortest driving distance on google maps. In this workshop we will explore some of the most useful graph algorithms, from both the breadth-first and depth-first methods for searching graphs, to Kruskal’s algorithm for finding a minimum spanning tree of a weighted graph, to approximation methods for solving the traveling salesman problem. We will use hands-on examples in python to explore the computational complexity and accuracy of these algorithms, and discuss their broader applications. 

Video for this lecture: [Graph Theory for Data Science, Part II: Graph Algorithms: Traversing the tree and beyond](https://www.youtube.com/watch?v=45jNuN4DtPM&list=PLHAk3jHXWpxI7fHw8m5PhrpSRpR3NIjQo&index=3)

Previous lecture: [Graph Theory for Data Science, Part I: What is a graph and what can we do with it?](https://www.youtube.com/watch?v=KlzWjdaXYgA&list=PLHAk3jHXWpxI7fHw8m5PhrpSRpR3NIjQo&index=1)

Lecturer: Julia Olivieri (jolivier@stanford.edu)

## Running the code

Clone this repo and enter the folder:

    $ git clone https://github.com/juliaolivieri/WiDS_graph_algorithms.git
    $ cd WiDS_graph_algorithms/

Install any missing requirements with the following command (note that this will install the Python packages numpy, matplotlib, networkx, and jupyterlab; you can create a virtual environment if you don't want to install them in your base environment):

    $ pip install -r requirements.txt

Start a jupyter notebook:

    $ jupyter notebook

Open the python notebook `Graph_Search.ipynb`. Run every cell (you can run a cell by pressing Shift and Enter while it is selected). 

You can change the parameters in the blocks with the comment `CHANGE HERE` to test the algorithms on different random graphs. 

## Links mentioned in the lecture

* [Proof of correctness of Kruskal's algorithm](https://en.wikipedia.org/wiki/Kruskal's_algorithm#Proof_of_correctness)
* [Detecting a cycle with DFS](https://www.geeksforgeeks.org/detect-cycle-undirected-graph/)
* [Video of soap solving the Steiner Tree problem](https://www.youtube.com/watch?v=PI6rAOWu-Og)