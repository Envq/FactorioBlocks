#!/usr/bin/env python3
from __future__ import annotations
from collections import deque
from graphviz import Digraph



class DiGraph(object):
    def __init__(self, adjacencyList:dict = {}):
         self._graph = adjacencyList
    
    def get_nodes(self):
        return list(self._graph.keys())

    def get_edges(self):
        edges = []
        for node in self._graph:
            for (neighbour, weight) in self._graph[node]:
                edges.append((node, neighbour, weight))
        return edges
    
    def add_node(self, node:str):
        if node not in self._graph:
            self._graph[node] = list()
    
    def add_edge(self, node_from:str, node_to:str, weight:int):
        if node_from in self._graph:
            self._graph[node_from].append((node_to,weight))
        else:
            self._graph[node_from] = list((node_to,weight))
    
    def __str__(self):
        return f"nodes: {self.get_nodes()}\n" + \
               f"edges: {self.get_edges()}"





class GraphView(DiGraph):
    def __init__(self, name:str, adjacencyList:dict = {}):
        super().__init__(adjacencyList)
        self.name = name
        self.plt = Digraph(self.name, filename=f'graphs/{self.name}.gv')
        self.plt.graph_attr = {'size': '4,5'}


    def _createPlot(self):
        queue = deque([self])
        while len(queue) > 0:
            curr = queue.pop()
            # --- action ---
            # self.plt.node(str(id(curr)), '{'+f'{curr.num}x {curr.name} | MachineSpeed={curr.machine.value}'+'}', shape='record')
            # for e in curr.inputs:
            #     self.plt.edge(e.name, str(id(curr)), str(e.val))
            # for e in curr.outputs:
            #     self.plt.edge(str(id(curr)), e.name, str(e.val))
            # --- extract children ---
            for e in curr.blockInputs:
                queue.appendleft(e)
                # --- action ---
                out = e.outputs[0]
                self.plt.edge(out.name, str(id(curr)), str(out.val))
        
    
    def view(self):
        pass



# if __name__ == '__main__':
#     graph = { "A" : [("B",130), ("C",130)],
#               "B" : [("D",130)] }

#     g = GraphView(graph)
#     g.add_edge('B','C',130)
#     g.view()


