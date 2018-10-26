import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import random

V=9
def minDistance(dist, sptSet): 
    min = 99999
    min_index=0 
    for v in range(0,V):
        if (sptSet[v] == 0 and dist[v] <= min): 
            min = dist[v]
            min_index = v 
    return min_index

def printPath(parent, j, path):   
    if (parent[j] == - 1): 
        return;
    printPath(parent, parent[j],path) 
    path.append(j) 
   
def printSolution (dist, n, parent): 
    src=0
    paths=[]
    for i in range(1,V):
        path=[0] 
        printPath(parent, i,path)
        paths.append(path)
    return paths

def djikstra(graph,src):
    dist=[] 
    sptSet=[]
    parent=[None]*10
    parent[0]=-1
    for i in range(0,V): 
        dist.append(99999)
        sptSet.append(0) 
    dist[src] = 0
    for count in  range(0,V-1):   
        u = minDistance(dist, sptSet) 
        sptSet[u] = 1
        for v in range(0,V): 
            if (sptSet[v]==0 and graph[u][v] and dist[u] != 99999  and dist[u]+graph[u][v] < dist[v]): 
                parent[v] = u;
                dist[v] = dist[u] + graph[u][v];
    return printSolution(dist, V, parent)

if __name__=="__main__":
    graph = [[0, 4, 0, 0, 0, 0, 0, 8, 0], 
                      [4, 0, 8, 0, 0, 0, 0, 11, 0], 
                      [0, 8, 0, 7, 0, 4, 0, 0, 2], 
                      [0, 0, 7, 0, 9, 14, 0, 0, 0], 
                      [0, 0, 0, 9, 0, 10, 0, 0, 0], 
                      [0, 0, 4, 14, 10, 0, 2, 0, 0], 
                      [0, 0, 0, 0, 0, 2, 0, 1, 6], 
                      [8, 11, 0, 0, 0, 0, 1, 0, 7], 
                      [0, 0, 2, 0, 0, 0, 6, 7, 0] 
                     ]
    paths=djikstra(graph,0)
    connections=[]
    for path in paths:
        connections.append((path[-1],path[-2]))
    print (connections)
    G = nx.Graph()
    G.add_edges_from(connections)
    val_map={}
    counter=0.0
    for i in range(0,V):
        val_map[i]=counter
        counter=counter+0.01

    values = [val_map.get(node, 0.25) for node in G.nodes()]
    print (values)
    nx.draw(G, cmap = plt.get_cmap('jet'), node_color = values, with_labels=True)
    plt.savefig('path.png')
