#!/usr/bin/env python3
from src.data_manager import DataManager
import src.utils as utils


class BlockNode():
    def __init__(self, speed, num, inputs, outputs):
        self.num     = num
        self.speed   = speed
        self.inputs  = inputs
        self.outputs = outputs
    
    def printState(self):
        print('num:     ', self.num)
        print('speed:   ', self.speed)
        print('inputs:  ', self.inputs)
        print('outputs: ', self.outputs)
        print()
    

    def minimize(self):
        pass
    
    def multiply(self, val):
        pass


class BlockManager():
    ASM1 = 0.50  # ASsemblingMachine1
    ASM2 = 0.75  # ASsemblingMachine2
    ASM3 = 1.25  # ASsemblingMachine3

    def __init__(self):
        self.DM = DataManager()
    

    def _normalizeData(self, data):
        # Normalize phase: normalize to 1 sec
        norm = utils.getSmallestFactor(data['sec'])
        num = int(data['sec'] * norm)
        inputs  = dict()
        for k,v in data['inputs'].items():
            inputs[k] = v * norm
        outputs  = dict()
        for k,v in data['outputs'].items():
            outputs[k] = v * norm
        # Minimize phase: reduce to minimum terms
        s = {num}
        for d in [inputs, outputs]:
            for k in d:
                s.add(d[k])
        GCD = utils.gcd(*s)
        if GCD != 1:
            num = int(num / GCD)
            for d in [inputs, outputs]:
                for k in d:
                    d[k] = int(d[k] / GCD)
        return num, inputs, outputs
    

    def getBlock(self, name, speed):
        data = self.DM.getBasicBlock(name)
        n, i, o = self._normalizeData(data)
        block = BlockNode(speed, n, i, o)
        return block

