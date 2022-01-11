#!/usr/bin/env python3
import math
from src.data_manager import DataManager

dm = DataManager()


def printBasicBlocksList():
    for k in dm.getBasicBlocks():
        print(k)


class Block():
    def __init__(self, name, inputs, outputs, subBlocks={}):
        self.name      = name
        self.num       = 1
        self.inputs    = inputs
        self.outputs   = outputs
        self.subBlocks = subBlocks
    
    def print(self):
        space = '  '
        print(f'[{self.num}x] {self.name}')
        if self.subBlocks:
            print('SubBlocks:')
            for k,v in self.subBlocks.items():
                print(f'{space}[{v}x] {k}')
        print('Inputs:')
        for k,v in self.inputs.items():
            print(f'{space}{v: >6} {k}')
        print('Outputs:')
        for k,v in self.outputs.items():
            print(f'{space}{v: >6} {k}')
        print()
    
    def normalize(self, val):
        if val != 1:
            for e in [self.inputs, self.outputs]:
                for k in e:
                    newVal = e[k] // val
                    remainder = e[k] % val
                    e[k] = newVal
                    if remainder != 0:
                        raise RuntimeError('Reminder Found')

    def multiply(self, val):
        if val != 1:
            for e in [self.inputs, self.outputs, self.subBlocks]:
                for k in e:
                    e[k] *= val
            self.num = val


def getBlockFromName(name):
    data = dm.getBasicBlocks()[name]
    subBlock = {name: 1}
    block = Block(name, data['inputs'], data['outputs'], subBlock)
    block.normalize(data['sec'])
    return block


def multiplyBlocks(block, val):
    newBlockInputs  = block.inputs.copy()
    newBlockOutputs = block.outputs.copy()
    newsubBlocks    = block.subBlocks.copy()
    for e in [newBlockInputs, newBlockOutputs, newsubBlocks]:
        for k in e:
            e[k] *= val
    newBlock = Block(block.name, newBlockInputs, newBlockOutputs, newsubBlocks)
    newBlock.num = val
    return newBlock


def _mcm(a, b):
    return (a*b)//math.gcd(a,b)


def _dictMerge(a, b, delete=None):
    c = dict()
    for k,v in a.items():
        if k != delete:
            c[k] = v
    for k,v in b.items():
        if k != delete:
            if k in c:
                c[k] = c[k] + v
            else:
                c[k] = v
    return c


def _getCommonLine(blockIN, blockOUT):
    for e in blockIN.outputs:
        for f in blockOUT.inputs:
            if e == f:
                return e
    return None


def composeBlocks(name, blockIN, blockOUT):
    # Get the line where do the union.
    line = _getCommonLine(blockIN, blockOUT)
    if line:
        # Get MCM and adjust subBlocks
        blocksMCM = _mcm(blockIN.outputs[line], blockOUT.inputs[line])
        a = multiplyBlocks(blockIN, blocksMCM // blockIN.outputs[line])
        b = multiplyBlocks(blockOUT, blocksMCM // blockOUT.inputs[line])
    # Get new Block parts
    newBlockInputs  = _dictMerge(a.inputs, b.inputs, delete=line)
    newBlockOutputs = _dictMerge(a.outputs, b.outputs, delete=line)
    newSubBlocks    = _dictMerge(a.subBlocks, b.subBlocks)
    return Block(name, newBlockInputs, newBlockOutputs, newSubBlocks)
