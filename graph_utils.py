from collections import defaultdict
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
plt.rcParams.update({'font.size': 16})
fig_size = 10

def add_edge(adjacency_dict, weights,curr_edges):
    v1 = np.random.choice(list(adjacency_dict.keys()))
    v2 = np.random.choice(list(adjacency_dict.keys()))
    
    if ((v1 != v2) and (v1 not in adjacency_dict[v2])):
        adjacency_dict[v1].append(v2)
        adjacency_dict[v2].append(v1)
        weight = np.random.poisson(5) + 1
        weights[(v1,v2)] = weight
        weights[(v2,v1)] = weight
        curr_edges += 1
    return adjacency_dict, weights, curr_edges

def create_graph(num_vertices, num_edges, force_connected=True):
    weights = {}
    adjacency_dict = {k : [] for k in range(1,num_vertices + 1)}
    curr_edges = 0
    while (curr_edges < num_edges):
        adjacency_dict, weights, curr_edges = add_edge(adjacency_dict, weights, curr_edges)
    if force_connected:
        while not is_connected(adjacency_dict):
            adjacency_dict, weights, curr_edges = add_edge(adjacency_dict, weights, curr_edges)
    return adjacency_dict, weights

def contains_cycle(adjacency_dict):
    """Check whether a graph contains a cycle given an adjacency dictionary"""

    # keep track of all unvisited vertices
    unvisited = list(adjacency_dict.keys())

    # continue until all vertices have been visited
    while(len(unvisited) > 0):

        # Run DFS from an unvisited vertex and find all vertices reachable from that vertex (a component)
        _, _, visited = DFS(adjacency_dict, defaultdict(lambda : False), unvisited[0])

        # count the number of degrees in the component
        component_degrees = 0
        for k, v in adjacency_dict.items():
            if k in visited:
                component_degrees += len([i for i in v if i in visited])
        
        # number of degrees = 2 * number of edges
        component_edges = component_degrees/2

        # If a connected component on n vertices has n - 1 edges, it's a tree; otherwise, it has a cycle
        if component_edges > len(visited) - 1:
            return True
        unvisited = [i for i in unvisited if i not in visited]
    return False

def is_connected(adjacency_dict):
    """Given an adjacency dictionary determine whether the graph is connected"""

    # Run DFS from a vertex
    _, _, visited = DFS(adjacency_dict, defaultdict(lambda : False), list(adjacency_dict.keys())[0])
    
    # If DFS visits every vertex, the graph is connected; otherwise it's not
    if len(visited) < len(adjacency_dict):
        return False
    return True

def draw_adj(adjacency_dict,weights=defaultdict(lambda : 1),draw_weights=False, tree = defaultdict(lambda : [])):
    g = nx.Graph()
    for v1, val in adjacency_dict.items():
        for v2 in val:
            if v2 in tree[v1]:
                color = "orange"
            else:
                color = "black"
            g.add_edge(v1,v2,color = color,weight=weights[(v1,v2)])
        if len(val) == 0:
            g.add_node(v1)
    my_pos = nx.spring_layout(g, seed = 100)
    plt.figure(figsize=(fig_size,fig_size)) 
#     nx.draw(g, pos=my_pos,with_labels=True,node_color="silver")
    edges = g.edges()
    colors = [g[u][v]['color'] for u,v in edges]
    weights = [g[u][v]['weight'] for u,v in edges]
    nx.draw(g, pos=my_pos,  edge_color=colors, width=weights,with_labels=True,node_color = "silver")

    if draw_weights:
        labels = nx.get_edge_attributes(g,'weight')
        nx.draw_networkx_edge_labels(g,my_pos,edge_labels=labels)
    plt.show()

def create_search_tree(vertex_limit, poisson_param, p, seed, close_solutions):
    np.random.seed(seed)
    adjacency_dict = {1 : []}
    count = 1
    curr_vertex = 1


    colors = ["dodgerblue"]
    sizes = [100]
    vertex_color = {1: "lightgreen", 0: "white"}
    vertex_size = {1: 100, 0: 25}
    success_dict = {1 : True, 0 : False}
    layer = 1
    target = {1 : False}

    layer_vertices = [1]
    next_layer_vertices = []
    layer = 1



    while (count < vertex_limit):

        num_neighbors = np.random.poisson(lam=max(1,poisson_param - curr_vertex + 1)) + 1

        if curr_vertex in layer_vertices:

            next_layer_vertices += list(range(count + 1, count + 1 + num_neighbors))

        else:

            layer_vertices = next_layer_vertices
            next_layer_vertices = list(range(count + 1, count + 1 + num_neighbors))
            layer += 1

        for neighbor in range(num_neighbors):
            count += 1

            adjacency_dict[curr_vertex].append(count)
            adjacency_dict[count] = [curr_vertex]

            if close_solutions:
                success = np.random.binomial(1, p**layer)
            else:
                success = np.random.binomial(1, p**(max(1,6 - layer)))

            target[count] = success_dict[success]
            colors.append(vertex_color[success])
            sizes.append(vertex_size[success])

        curr_vertex += 1

    g = nx.Graph()
    for v1, val in adjacency_dict.items():
        for v2 in val:
            g.add_edge(v1,v2,)
        if len(val) == 0:
            g.add_node(v1)
    my_pos = nx.spring_layout(g, seed = 100)
    return adjacency_dict, target, colors, sizes, g, my_pos


def DFS(adjacency_dict, target, start = 1):
    return call_DFS(adjacency_dict, target,start=start, current = start, visited_dfs = [start])

def call_DFS(adjacency_dict, target, start=1, current = 1, visited_dfs = [1], backtrack = {}):
    """Perform depth first search for 'true' targets given adjacency dictionary"""
    
    # Find all unvisited neighbors of current vertex
    unvisited_neighbors = [x for x in adjacency_dict[current] if x not in visited_dfs]
    
    # if there are no unvisited neighbors, every vertex "further down" in the tree has been searched
    # Backtrack to the previous vertex and perform DFS from there
    if len(unvisited_neighbors) == 0:
        if current == start:
            return None, len(visited_dfs), visited_dfs
        return call_DFS(adjacency_dict, target, start = start,current = backtrack[current],visited_dfs = visited_dfs,backtrack = backtrack)

    # choose an unvisited vertex, neighbor of the current vertex, to visit next
    next_vertex = min(unvisited_neighbors)

    # keep track of the edge between the current vertex and the next vertex so 
    # we can backtrack in the future if necessary
    backtrack[next_vertex] = current
    
    # if the next vertex is 'true', return it
    if target[next_vertex]:
        return next_vertex, len(visited_dfs), visited_dfs
    
    # if not, mark that the next vertex has been visited, and continue the algorithm from there
    visited_dfs.append(next_vertex)
    return call_DFS(adjacency_dict, target, start=start,current = next_vertex,visited_dfs = visited_dfs,backtrack = backtrack)