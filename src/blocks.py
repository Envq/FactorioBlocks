#!/usr/bin/env python3
from __future__ import annotations
from curses import color_content, color_pair
from enum import Enum
from collections import deque
from graphviz import Digraph
from copy import deepcopy

from src.data_manager import DataManager
import src.utils as utils




class MachineType(Enum):
    assemblingMachine1 = 0.50
    assemblingMachine2 = 0.75
    assemblingMachine3 = 1.25
    oilRefinery        = 1.00
    chemicalPlant      = 1.00




class BlockIO():
    def __init__(self, name:str, num) -> None:
        self.name = name
        self.num  = num
        self.producer = None
    

    def addProducer(self, block:BlockNode):
        self.producer = block
    

    def __str__(self):
        return f'{self.num}x {self.name}'




class BlockNode(object):
    def __init__(self, name:str, machine:MachineType, num:int, inputs:list[BlockIO], outputs:list[BlockIO]):
        self.name         = name
        self.machine      = machine
        self.num          = num
        self.inputs       = inputs
        self.outputs      = outputs

      
    def _bfs(self, action):
        queue = deque([self])
        while len(queue) > 0:
            curr = queue.pop()
            action(curr)
            for e in curr.inputs:
                if e.producer:
                    queue.appendleft(e.producer)

    def printState(self):
        print('   name: ', self.name)
        print('machine: ', self.machine)
        print('    num: ', self.num)
        print(' inputs: ', [str(e) for e in self.inputs])
        print('outputs: ', [str(e) for e in self.outputs])
        print('----------------------------------------')


    def printRecipe(self):
        self._bfs(lambda b: b.printState())


    def _multiplyRawIO(self, val):
        self.num *= val
        for l in [self.inputs, self.outputs]:
            for e in l:
                e.num *= val
    

    def multiplyInputs(self, val):
        self._bfs(lambda b: b._multiplyRawIO(val))
    

    def addInputBlock(self, b:BlockNode):
        block = deepcopy(b)
        for product in block.outputs:
            for request in self.inputs:
                if product.name == request.name:
                    # Get LeastMinimumMultiply and adjust blocks
                    lcm = utils.lcm(product.num, request.num)
                    block.multiplyInputs(lcm // product.num)
                    self.multiplyInputs(lcm // request.num)
                    request.addProducer(block)



class BlockManager():
    def __init__(self):
        self.DM = DataManager()
    
    def _processData(self, data, machine:MachineType):
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
    

    def getBlock(self, name, machine:MachineType) -> BlockNode:
        data = self.DM.getBasicBlock(name)
        n, i, o = self._processData(data, machine)
        return BlockNode(name, machine, n, i, o)
    

    def viewBlock(self, block):
        plt = Digraph(block.name, filename=f'graphs/{block.name}.gv')
        plt.graph_attr = {'size': '4,5'}
        queue = deque([block])
        while len(queue) > 0:
            curr = queue.pop()
            # --- action ---
            plt.node(str(id(curr)), '{'+f'{curr.num}x {curr.name} | MachineSpeed={curr.machine.value}'+'}', shape='record', style='filled', fillcolor='grey')

            for e in curr.inputs:
                if not e.producer:
                    plt.node(str(id(e)), e.name, shape='invhouse', style='filled', fillcolor='springgreen3')
                else:
                    plt.node(str(id(e)), e.name)
                plt.edge(str(id(e)), str(id(curr)), str(e.num))

            for e in curr.outputs:
                if curr == block:
                    plt.node(str(id(e)), e.name, shape='invhouse', style='filled', fillcolor='springgreen3')
                else:
                    plt.node(str(id(e)), e.name)
                plt.edge(str(id(curr)), str(id(e)), str(e.num))
                
            # --- extract children ---
            for e in curr.inputs:
                if e.producer:
                    queue.appendleft(e.producer)
        plt.view()




if __name__ == '__main__':
    root = BlockNode(10)
    root.PrintTree()


