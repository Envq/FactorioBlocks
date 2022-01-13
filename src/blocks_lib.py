#!/usr/bin/env python3
from src.data_manager import DataManager
import src.utils as utils

dm = DataManager()


def printCustomBlocksList():
    for k in dm.getCustomBlocks():
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
    
    def _normalizeIO(self):
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
    
    def _normalizeNum(self, val):
        # adjust sec
        if val != 1:
            for e in [self.inputs, self.outputs]:
                for k in e:
                    newVal = e[k] / val
                    e[k] = int(newVal)
                    if not (newVal).is_integer():
                        raise RuntimeError('Reminder Found')
    
    def normalize(self, val):
        self._normalizeNum(val)
        self._normalizeIO()
        
    
    def saveAs(self, name):
        if self.num != 1:
            raise RuntimeError('Can\'t save block with size != 1')
        block = {name: {"subBlocks": self.subBlocks, \
                        "inputs": self.inputs, \
                        "outputs": self.outputs}}
        dm.saveCustomBlock(block)
    
    def save(self):
        self.saveAs(self.name)


def getBasicBlock(name):
    data = dm.getBasicBlocks()[name]
    subBlock = {name: 1}
    block = Block(name, data['inputs'], data['outputs'], subBlock)
    block.normalize(data['sec'])
    return block


def getCustomBlock(name):
    data = dm.getCustomBlocks()[name]
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


def compose2Blocks(name, blockIN, blockOUT):
    # Get the line where do the union.
    line = utils.getCommonLine(blockIN, blockOUT)
    if line:
        # Get MCM and adjust subBlocks
        blocksMCM = utils.mcm(blockIN.outputs[line], blockOUT.inputs[line])
        a = multiplyBlocks(blockIN, blocksMCM // blockIN.outputs[line])
        b = multiplyBlocks(blockOUT, blocksMCM // blockOUT.inputs[line])
    # Get new Block parts
    newBlockInputs  = utils.dictMerge(a.inputs, b.inputs, delete=line)
    newBlockOutputs = utils.dictMerge(a.outputs, b.outputs, delete=line)
    newSubBlocks    = utils.dictMerge(a.subBlocks, b.subBlocks)
    return Block(name, newBlockInputs, newBlockOutputs, newSubBlocks)


def composeBlocks(name, blockArray):
    res = blockArray[0]
    for i in range(1, len(blockArray)):
        res = compose2Blocks(name, res, blockArray[i])
    return res

