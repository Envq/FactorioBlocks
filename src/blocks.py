#!/usr/bin/env python3
from __future__ import annotations
from enum import Enum
from collections import deque
from math import prod
from graphviz import Digraph

from src.data_manager import DataManager
import src.utils as utils




class MachineType(Enum):
    AssemblingMachine1 = 0.50
    AssemblingMachine2 = 0.75
    AssemblingMachine3 = 1.25
    OilRefinery        = 1.00
    ChemicalPlant      = 1.00




class Resource():
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


    def isIntermediate(self) -> bool:
        return self.getType() == "X"


    def __str__(self) -> str:
        return f'{self.num}x {self.getType()}_{self.name}'
    

    def getId(self, merge=False) -> str:
        strid = ""
        if self.producer:
            if self.consumer:
                # strid = f'{self.producer.name}_{self.name}_{self.consumer.name}'
                strid = f'{self.name}'
            else:
                if merge:
                    strid = f'{self.name}_None'
                else:
                    strid = f'{self.producer.name}_{self.name}_None'
        else:
            if self.consumer:
                if merge:
                    strid = f'None_{self.name}'
                else:
                    strid = f'None_{self.name}_{self.consumer.name}'
            else:
                strid = f'None_{self.name}_None'
        return strid




class BlockNode(object):
    def __init__(self, name:str, machine:MachineType, num:int, inputs:list[Resource], outputs:list[Resource]):
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
    

    def addToViewer(self, viewer:Digraph, mergeResources:bool):
        # Add Machine
        viewer.node(self.getId(), '{'+f'{self.num}x {self.name} | MachineSpeed={self.machine.value}'+'}', shape='record', style='filled', fillcolor='grey')
        # Add Input Resource
        for e in self.inputs:
            if e.isIntermediate():
                viewer.node(e.getId(mergeResources), e.getId(mergeResources))
                viewer.edge(e.getId(mergeResources), self.getId(), str(e.num))
                # viewer.edge(e.producer.getId(), e.getId(mergeResources), str(e.num))
            else:
                viewer.node(e.getId(mergeResources), e.name, shape='invhouse', style='filled', fillcolor='springgreen3')
                viewer.edge(e.getId(mergeResources), self.getId(), str(e.num))
        # Add Output Resource
        for e in self.outputs:
            if e.isIntermediate():
                viewer.node(e.getId(mergeResources), e.getId(mergeResources))
                viewer.edge(self.getId(), e.getId(mergeResources), str(e.num))
                # viewer.edge(e.getId(mergeResources), e.consumer.getId(), str(e.num))
            else:
                viewer.node(e.getId(mergeResources), e.name, shape='invhouse', style='filled', fillcolor='tomato')
                viewer.edge(self.getId(), e.getId(mergeResources), str(e.num))


    def addRecipeTo(self, book:dict):
        # Add machine
        if self.name not in book['machines']:
            book['machines'][self.name] = {self.machine.name : self.num}
        elif self.machine.name not in book['machines'][self.name]:
            book['machines'][self.name][self.machine.name] = self.num
        else:
            book['machines'][self.name][self.machine.name] += self.num

        # Add inputs
        for i in self.inputs:
            if not i.isIntermediate():
                book['inputs'][i.name] = book['inputs'].get(i.name, 0) + i.num
        # Add outputs
        for o in self.outputs:
            if not o.isIntermediate():
                book['outputs'][o.name] = book['outputs'].get(o.name, 0) + o.num


    def addIfProduceThis(self, product:str, arg:list):
        for o in self.outputs:
            if o.name == product:
                arg[0].append(o)  #group
                arg[1] += o.num   #sum




class BlockGraph():
    def __init__(self) -> None:
        self._DM = DataManager()
        self._roots = list()
    

    def _processData(self, data, machine:MachineType) -> tuple:
        # Normalize phase: normalize to 1 sec
        time = data['sec'] / machine.value
        norm = utils.getSmallestFactor(time)
        num = int(time * norm)
        inputs = list()
        numbers = {num}
        for k, v in data['inputs'].items():
            val = v * norm
            inputs.append(Resource(k, val))
            numbers.add(val)
        outputs = list()
        for k, v in data['outputs'].items():
            val = v * norm
            outputs.append(Resource(k, val))
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
        b = BlockNode(name, machine, n, i, o)
        self._roots.append(b)
        return b


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


    def print(self, block:BlockNode) -> None:
        self._bfs(block, lambda b : print(b))


    def multiply(self, block:BlockNode, val:int) -> None:
        self._bfs(block, lambda b : b.multiply(val))


    def connect(self, producer:BlockNode, consumer:BlockNode) -> None:
        for product in producer.outputs:
            for request in consumer.inputs:
                if product.name == request.name:
                    # Get the block that product this resource
                    product_arg = [list(), 0]
                    self._bfs(producer, lambda b : b.addIfProduceThis(product.name, product_arg))
                    product_group = product_arg[0]
                    agg_product   = product_arg[1]

                    # Get LeastMinimumMultiply
                    lcm = utils.lcm(agg_product, request.num)
                    # print(f'target: {agg_product} vs {request.num} -> {lcm}')
                    product_adj = lcm // agg_product
                    request_adj = lcm // request.num
                    # print(f'adj: {product_adj} vs {request_adj}')

                    # Adjust blocks
                    self._bfs(producer, lambda b : b.multiply(product_adj))
                    self._bfs(consumer, lambda b : b.multiply(request_adj))

                    # Connect blocks
                    for p in product_group:
                        p.consumer = consumer
                    request.producer = producer





                    # # Get total number of target resource producted
                    # outputs = dict()
                    # self._bfs(producer, lambda b : b.addOutputsTo(outputs))
                    # agg_product = outputs[product.name]
                    # # Get LeastMinimumMultiply
                    # lcm = utils.lcm(agg_product, request.num)
                    # print(f'target: {agg_product} vs {request.num} -> {lcm}')
                    # product_adj = lcm // agg_product
                    # request_adj = lcm // request.num
                    # print(f'adj: {product_adj} vs {request_adj}')
                    # # Adjust blocks
                    # self._bfs(producer, lambda b : b.multiply(product_adj))
                    # self._bfs(consumer, lambda b : b.multiply(request_adj))
                    # # Connect blocks
                    # product.consumer = consumer
                    # request.producer = producer
        # merge roots
        if producer in self._roots:
            self._roots.remove(producer)
        else:
            self._roots.remove(consumer)


    def getRecipes(self) -> dict:
        books = list()
        for e in self._roots:
            book = {'inputs':{}, 'outputs':{}, 'machines':{}}
            self._bfs(e, lambda b : b.addRecipeTo(book))
            books.append(book)
        return books


    def printRecipes(self) -> None:
        books = self.getRecipes()
        for book in books:
            print('Inputs:')
            for k,v in book['inputs'].items():
                print(f'  - {k}: {v}')
            print('Outputs:')
            for k,v in book['outputs'].items():
                print(f'  - {k}: {v}')
            print('Machines:')
            for e in book['machines']:
                print(f'  - {e}:')
                for k,v in book['machines'][e].items():
                    print(f'     - {k}: {v}')
            print('=============================\n')


    def view(self, name='blockGraph', mergeResources=True, size=5) -> None:
        # Create viewer
        viewer = Digraph(name, filename=f'graphs/{name}.gv')
        viewer.graph_attr = {'size': f'{size}'}
        # Create graph view
        for e in self._roots:
            self._bfs(e, lambda b : b.addToViewer(viewer, mergeResources))
        # Visualize it
        viewer.view()

