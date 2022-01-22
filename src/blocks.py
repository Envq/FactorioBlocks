#!/usr/bin/env python3
from __future__ import annotations
from enum import Enum
from collections import deque

from src.data_manager import DataManager
import src.utils as utils


class MachineType(Enum):
    assemblingMachine1 = 0.50
    assemblingMachine2 = 0.75
    assemblingMachine3 = 1.25
    oilRefinery        = 1.00
    chemicalPlant      = 1.00



class BlockIO():
    def __init__(self, name:str, val) -> None:
        self.name = name
        self.val  = val



class BlockNode():
    def __init__(self, name:str, machine:MachineType, num:int, inputs:list[BlockIO], outputs:list[BlockIO]) -> None:
        self.name         = name
        self.machine      = machine
        self.num          = num
        self.inputs       = inputs
        self.blockInputs  = list()
        self.outputs      = outputs
        self.blockOutputs = list()

    def printState(self):
        print('----------------------------------------')
        print('         name: ', self.name)
        print('      machine: ', self.machine)
        print('          num: ', self.num)
        print('   raw inputs: ', [(e.name, e.val) for e in self.inputs])
        print(' block inputs: ', [(e.name, e.num) for e in self.blockInputs])
        print('  raw outputs: ', [(e.name, e.val) for e in self.outputs])
        print('block outputs: ', [(e.name, e.num) for e in self.blockOutputs])
        print('----------------------------------------')
    
    def _bfsInputs(self, action):
        queue = deque([self])
        while len(queue) > 0:
            curr = queue.pop()
            action(curr)
            for e in curr.blockInputs:
                queue.appendleft(e)
    
    def addInputBlock(self, block:BlockNode):
        for e in self.inputs:
            if e.name == block.name:
                # Get LeastMinimumMultiply and adjust blocks
                lcm = utils.lcm(e.val, block.num)
                self.multiplyInputs(lcm // block.num)
                self.inputs.remove(e)
                self.blockInputs.append(block)

    def printRecipe(self):
        self._bfsInputs(lambda b: b.printState())
    
    def _multiplyRaw(self, val):
        for l in [self.inputs, self.outputs]:
            for e in l:
                e.val *= val
    
    def multiplyInputs(self, val):
        self._bfsInputs(lambda b: b._multiplyRaw(val))





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
                    e.val = int(e.val / GCD)
        return num, inputs, outputs
    

    def getBlock(self, name, machine:MachineType) -> BlockNode:
        data = self.DM.getBasicBlock(name)
        n, i, o = self._processData(data, machine)
        return BlockNode(name, machine, n, i, o)

