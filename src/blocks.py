#!/usr/bin/env python3
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
    def __init__(self, name:str, val:int) -> None:
        self.name = name
        self.val  = val
        self.head = None
        self.tail = None
    
    def getData(self):
        return (self.name, self.val)



class BlockMachine():
    def __init__(self, name:str, machine:MachineType, num:int, inputs:list[BlockIO], outputs:list[BlockIO]) -> None:
        self.name    = name
        self.machine = machine
        self.num     = num
        self.inputs  = inputs
        self.outputs = outputs
        # Adjust BlockIO
        for e in self.inputs:
            e.head = self
        for e in self.outputs:
            e.tail = self

    def printState(self):
        print('----------------------------------------')
        print('name:    ', self.name)
        print('machine: ', self.machine)
        print('num:     ', self.num)
        print('inputs:  ', [e.getData() for e in self.inputs])
        print('outputs: ', [e.getData() for e in self.outputs])
        print('----------------------------------------')

    def changeMachine(self, machine:MachineType):
        pass
    


class BlocksChain():
    def __init__(self, head:BlockMachine):
        self.head = head
    
    def getInputs(self):
        return self.head.inputs
    
    def getOutputs(self):
        return self.head.output
    
    def getNumBlocks(self):
        return 'TODO'

    def _bfs(self, action, direction):
        if direction == 'tail':
            queue = deque([self.head])
            while len(queue) > 0:
                curr = queue.pop()
                action(curr)
                for i in curr.inputs:
                    if i.tail:
                        queue.appendleft(i.tail)
        elif direction == 'head':
            queue = deque([self.head])
            while len(queue) > 0:
                curr = queue.pop()
                action(curr)
                for o in curr.outputs:
                    if o.head:
                        queue.appendleft(o.head)
    
    def _print(self, block:BlockMachine):
        block.printState()

    def print(self, direction='tail'):
        self._bfs(lambda x: self._print(x), direction)
    
    def _addToTail(self, b:BlockMachine, a:BlockMachine):
        """Add a Block to b tail"""
        for i in range(len(b.inputs)):
            for o in range(len(a.outputs)):
                # Get common line
                if a.outputs[o].name == b.inputs[i].name:
                    # Get LeastMinimumMultiply and adjust blocks
                    lcm = utils.lcm(b.inputs[i].val, a.outputs[o].val)
                    BlocksChain(a).adjust(lcm // a.outputs[i].val, 'tail')
                    BlocksChain(b).adjust(lcm // b.inputs[o].val, 'head')
                    # Adjust pointers
                    b.inputs[i].tail = a
                    a.outputs[o] = b.inputs[i]

    def addToTail(self, block:BlockMachine):
        self._bfs(lambda x: self._addToTail(x, block), 'tail')
    
    def addToHead(self):
        pass
    
    def minimize(self):
        pass

    def _multiply(self, x:BlockMachine, val):
        x.num *= val
        for i in x.inputs:
            i.val *= val
        for o in x.outputs:
            o.val *= val
    
    def adjust(self, val, direction):
        self._bfs(lambda x: self._multiply(x, val), direction)




class BlocksManager():
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
    

    def getBlock(self, name, machine:MachineType):
        data = self.DM.getBasicBlock(name)
        n, i, o = self._processData(data, machine)
        return BlockMachine(name, machine, n, i, o)
    
    
    def createBlocksChainFrom(self, block:BlockMachine):
        return BlocksChain(block)

