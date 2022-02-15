#!/usr/bin/env python3
from __future__ import annotations
from enum import Enum
from collections import deque
from graphviz import Digraph
from copy import deepcopy
import time

from src.data_manager import DataManager
import src.utils as utils




class MachineType(Enum):
    AssemblingMachine1 = 0.50
    AssemblingMachine2 = 0.75
    AssemblingMachine3 = 1.25
    OilRefinery        = 1.00
    ChemicalPlant      = 1.00




class BlockIO():
    def __init__(self, name:str, num) -> None:
        self.name = name
        self.num  = num
        self.producer = None
        self.consumer = None
    
    
    def getType(self) -> str:
        if self.producer:
            if self.consumer:
                return "X"
            else:
                return "O"
        else:
            if self.consumer:
                return "I"
            else:
                return "Null"


    def isIntermediateBlock(self) -> bool:
        return self.getType() == "X"


    def __str__(self) -> str:
        return f'{self.num}x {self.getType()}_{self.name}'
    

    def getId(self) -> str:
        before = f'{self.producer.name}' if self.producer else 'None'
        after = f'{self.consumer.name}' if self.consumer else 'None'
        return f'{before}_{self.name}_{after}'



class BlockNode(object):
    def __init__(self, name:str, machine:MachineType, num:int, inputs:list[BlockIO], outputs:list[BlockIO]):
        self.name         = name
        self.machine      = machine
        self.num          = num
        self.inputs       = inputs
        self.outputs      = outputs

        # Connect I/O
        for i in self.inputs:
            i.consumer = self
        for o in self.outputs:
            o.producer = self

    
    def getId(self) -> str:
        return f'{id(self)}'


    def __str__(self) -> str:
        return f'     id: {self.getId()}\n' + \
               f'   name: {self.name}\n' + \
               f'machine: {self.machine.name}\n' + \
               f'    num: {self.num}\n' + \
               f' inputs: {[str(e) for e in self.inputs]}\n' + \
               f'outputs: {[str(e) for e in self.outputs]}\n' + \
               f'----------------------------------------\n'


    def multiply(self, val):
        # Adjust the number of machines
        self.num *= val
        # Adjust the number of needed I/O
        for l in [self.inputs, self.outputs]:
            for e in l:
                e.num *= val
    

    def addToViewer(self, viewer:Digraph):
        # Add Machine
        viewer.node(self.getId(), '{'+f'{self.num}x {self.name} | MachineSpeed={self.machine.value}'+'}', shape='record', style='filled', fillcolor='grey')
        # Add Input blockIO
        for e in self.inputs:
            if e.isIntermediateBlock():
                viewer.node(e.getId(), e.name)
                viewer.edge(e.getId(), self.getId(), str(e.num))
            else:
                viewer.node(e.getId(), e.name, shape='invhouse', style='filled', fillcolor='springgreen3')
                viewer.edge(e.getId(), self.getId(), str(e.num))
        # Add Output blockIO
        for e in self.outputs:
            if e.isIntermediateBlock():
                viewer.node(e.getId(), e.name)
                viewer.edge(self.getId(), e.getId(), str(e.num))
            else:
                viewer.node(e.getId(), e.name, shape='invhouse', style='filled', fillcolor='tomato')
                viewer.edge(self.getId(), e.getId(), str(e.num))



class BlockManager():
    def __init__(self) -> None:
        self._DM = DataManager()
        self.n = 1
    

    def _processData(self, data, machine:MachineType) -> tuple:
        # Normalize phase: normalize to 1 sec
        time = data['sec'] / machine.value
        norm = utils.getSmallestFactor(time)
        num = int(time * norm)
        inputs = list()
        numbers = {num}
        for k, v in data['inputs'].items():
            val = v * norm
            inputs.append(BlockIO(k, val))
            numbers.add(val)
        outputs = list()
        for k, v in data['outputs'].items():
            val = v * norm
            outputs.append(BlockIO(k, val))
            numbers.add(val)
        # Minimize phase: reduce to minimum terms
        GCD = utils.gcd(*numbers)
        if GCD != 1:
            num = int(num / GCD)
            for l in [inputs, outputs]:
                for e in l:
                    e.num = int(e.num / GCD)
        return num, inputs, outputs


    def create(self, name, machine:MachineType) -> BlockNode:
        data = self._DM.getBasicBlock(name)
        n, i, o = self._processData(data, machine)
        return BlockNode(name, machine, n, i, o)


    def _bfs(self, block:BlockNode, action) -> None:
        queue = deque([block])
        explorated = set()
        while len(queue) > 0:
            curr = queue.pop()
            action(curr)
            explorated.add(curr)
            for e in curr.inputs:
                if e.producer and e.producer not in explorated:
                    queue.appendleft(e.producer)
            for e in curr.outputs:
                if e.consumer and e.consumer not in explorated:
                    queue.appendleft(e.consumer)
        self.n += 1


    def print(self, block:BlockNode) -> None:
        self._bfs(block, lambda b : print(b))


    def multiply(self, block:BlockNode, val:int) -> None:
        self._bfs(block, lambda b : b.multiply(val))


    def connect(self, producer:BlockNode, consumer:BlockNode) -> None:
        for product in producer.outputs:
            for request in consumer.inputs:
                if product.name == request.name:
                    # Get LeastMinimumMultiply
                    lcm = utils.lcm(product.num, request.num)
                    product_adj = lcm // product.num
                    request_adj = lcm // request.num
                    # Adjust blocks
                    self._bfs(producer, lambda b : b.multiply(product_adj))
                    self._bfs(consumer, lambda b : b.multiply(request_adj))
                    # Connect blocks
                    product.consumer = consumer
                    request.producer = producer


    def view(self, block:BlockNode, name=None) -> None:
        # Create viewer
        viewer = Digraph(block.name, filename=f'graphs/{name if name else block.name}.gv')
        viewer.graph_attr = {'size': '5'}
        # Create graph view
        self._bfs(block, lambda b : b.addToViewer(viewer))
        # Visualize it
        viewer.view()


