#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Practice Exercises for Python
Network Analysis
Ernesto Monroy

Here we explore the basics of network analysis by creating a unidirectional non
weighted graph (network). We use 2 methods for searching a network for a node
given a starting point. The Breadth First Search and The Depth First Search.


At the end, this concept is applied to the analysis of movie data to find the 
maximum distance between Kevin Bacon and any other actor in the list.

"""
from GraphStructures import Graph, Queue

#### 
# Search Algorithms

def breadthFirstSearch(graph, start):
    """ 
    Breadth-first search using Queue data structure, keeping track of paths
    
    Parameter: 
        graph (Digraph/Graph), 
        start: starting node in the graph
    
    Returns:
        dists, a dictionary of distances to all explored nodes:
            key - node, value - distance from start to that node 
        prev_nodes, a dictionary containing the previous node on the path to each node:
            key - node, value - the node from which we found this node; None for starting node
        
    Example use:
    >>> ex_graph = create_sample_graph()
    >>> bfs_dists, prev_nodes = breadthFirstSearch(ex_graph, 'John')
    >>> [prev_nodes['Donald'], prev_nodes['Helena'], prev_nodes['John']]
    ['Jared', 'John', None]
    """
    
    # Keep track of queue of nodes to explore next
    q = Queue() # Initialize an empty queue
    q.enqueue(start) # add start to queue
    
    # Keep track of explored nodes
    explored = set() # Initialize explored nodes as an empty set
    explored.add(start) # Mark starting node explored
    
    # Keep track of distances from start to all other nodes
    dists = dict() # Initialize distances as an empty dictionary
    dists[start] = 0 # Zero distance from start node to itself
    
    # Keep track of the previous node for each node
    prev_nodes= dict() # Initialize previous nodes as an empty dictionary
    prev_nodes[start]=None # None is the previous node from the start
    
    # Main loop
    while not q.is_empty(): # Loop while queue not empty
        v = q.dequeue() # Pop the first item from the queue 
        # Explore all adjacent nodes of v
        for w in graph.children_of(v): # loop through adjacent nodes
            if w not in explored: # If w not explored yet
                explored.add(w) # Mark w explored
                dists[w] = dists[v]+1 # Calculate distance from start to w based on v's distance
                prev_nodes[w]=v # Record the previous node
                q.enqueue(w) # Add w to queue to explore from in the future
    return dists, prev_nodes

def depthFirstSearch(graph, start, explored = set(), prev_nodes = dict(), pop_order = dict()):
    """
    Depth first search on graph from node start using recursion
    
    Parameters: 
        graph (Digraph/Graph), 
        start: starting node in the graph
        explored: nodes already explored (used only by the recursion)
        prev_nodes: nodes already travelled and distance (used only by the recursion)
        pop_order: order in which nodes are explored (used only by the recursion)
    Returns:
        prev_nodes: dictionary:
            key: node, value: node where this node was reached from
        pop_order: dictionary:
            key: node, value: the order in which this node was removed from the list
         
    Example use:
    >>> ex_graph = create_sample_graph()
    >>> explored, dfs_paths, pop_order = depthFirstSearch(lec_graph, 'John')
    >>> abs(pop_order['Chris'] - pop_order['Helena']) > 1
    True
    """
    #If the current position (start) is not explored, we havent completed searching
    #the graph
    if not start in explored:
        #Mark current node as explored
        explored.add(start)
        #Remember the order in which the current node was explored
        pop_order[start]=len(pop_order)+1
        #Recurse on all children of the current node (v)
        for v in graph.children_of(start):
            #If the child has been explored, avoid re-exploring
            if not v in explored:
                #Mark the current node, as the previous node for its child
                prev_nodes[v]=start
                #Recurse on each child
                explored, prev_nodes,pop_order=depthFirstSearch(graph, v, explored, prev_nodes,pop_order)
    #If the current node is explored, it means we are done. Return the result 
    #This will bubble up the recursion
    return explored, prev_nodes,pop_order

##### 
# Use Case: Length Kevin Bacons Longest Connection
    
def find_kevins_longest_connection():
    g = read_movie_data("movies.txt")
    s = 'Bacon, Kevin'
    dists, prev_nodes = breadthFirstSearch(g, s)
    #Loop to find longest
    longest = None
    nodesToLongest=0
    for key in dists:
        if dists[key]>nodesToLongest:
            longest=key
            nodesToLongest=dists[key]
            
    return longest, nodesToLongest

#### 
# Helper Functions


def read_movie_data(filename):
    """ 
    Reads movie data from text file into a graph data structure
    
    Reads each line as connections from first instance of line to other instances
    Assumes file is delimited by /
    
    Returns Graph object
    """
    graph = Graph()
    delimiter = '/'
    with open(filename, "r", encoding="utf8") as ins:
        for line in ins:
            names = line.split(delimiter)
            for i in range(1, len(names)):
                graph.add_edge(names[0], names[i])
    return graph

def print_path(prev_nodes, v):
    """ 
    Based on bfs result prev_nodes, prints out path from starting node to v
    """
    path = ''
    while v is not None:
        path += str(v) + ' -> ' 
        v = prev_nodes[v]
    path = path[:-3] # remove last '-> ' 
    print(path)

def print_children(graph, v = None):
    """
    Prints out children nodes
    """
    if v == None: v = input('Enter name: ')
    print(v)
    if graph.has_node(v):
        for w in graph.children_of(v):
            print('  ' + w)
            
def create_sample_graph():
    """
    Initializes the undirected graph
    
    Uses the add_edge method
    
    Returns Graph object of the lecture graph
    Example use:
    >>> ex_graph = create_sample_graph()
    >>> [x in ex_graph.children_of('Jared') for x in ['John', 'Helena', 'Donald', 'Paul']]
    [False, False, True, True]
    >>> ex_graph = create_sample_graph()
    >>> [x in ex_graph.children_of('Helena') for x in ['John', 'Helena', 'Donald', 'Paul']]
    [True, False, False, True]
    """
    g = Graph()
    g.add_edge('John', 'Helena')
    g.add_edge('John', 'Chris')
    g.add_edge('Helena', 'Chris')
    g.add_edge('Helena', 'Paul')
    g.add_edge('Paul', 'Jared')
    g.add_edge('Chris', 'Vicki')
    g.add_edge('Vicki', 'Jared')
    g.add_edge('Jared', 'Donald') 
    return g