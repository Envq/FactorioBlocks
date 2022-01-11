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
        # adjust sec
        if val != 1:
            for e in [self.inputs, self.outputs]:
                for k in e:
                    newVal = e[k] // val
                    remainder = e[k] % val
                    e[k] = newVal
                    if remainder != 0:
                        raise RuntimeError('Reminder Found')
        # adjust equal in-out
        to_delete = list()
        for e in self.inputs:
            for f in self.outputs:
                if e == f:
                    self.outputs[f] -= self.inputs[e]
                    if self.outputs[f] <= 0:
                        raise RuntimeError('Negative Output Found', self.outputs[f])
                    to_delete.append(e)
        for e in to_delete:
            self.inputs.pop(e)
    
    def save(self):
        if self.num != 1:
            raise RuntimeError('Can\'t save block with size != 1')
        block = {self.name: {"subBlocks": self.subBlocks, \
                             "inputs": self.inputs, \
                             "outputs": self.outputs}}
        dm.saveCustomBlock(block)


def getBasicBlock(name):
    data = dm.getBasicBlocks()[name]
    subBlock = {name: 1}
    block = Block(name, data['inputs'], data['outputs'], subBlock)
    block.normalize(data['sec'])
    return block


def getCustomBlock(name):
    data = dm.getCustomBlock()[name]
    block = Block(name, data['inputs'], data['outputs'], data['subBlocks'])
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


def compose2Blocks(name, blockIN, blockOUT):
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


def composeBlocks(name, blockArray):
    res = blockArray[0]
    for i in range(1, len(blockArray)):
        res = compose2Blocks(name, res, blockArray[i])
    return res

