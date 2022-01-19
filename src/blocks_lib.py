#!/usr/bin/env python3
from src.data_manager import DataManager
import src.utils as utils
# from data_manager import DataManager
# import utils as utils



class Block():
    def __init__(self, name, speed, inputs, outputs, subBlocks):
        self.name      = name
        self.speed     = speed
        self.inputs    = inputs
        self.outputs   = outputs
        self.subBlocks = subBlocks


    def printState(self):
        print('inputs:    ', self.inputs)
        print('subBlocks: ', self.subBlocks)
        print('outputs:   ', self.outputs)
        print()
    

    def getCopy(self):
        return Block(self.name, self.speed, self.inputs, self.outputs, self.subBlocks)
    

    def multiply(self, num):
        for d in [self.subBlocks, self.inputs, self.outputs]:
            for k in d:
                d[k] *= num

    

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
    

    def _normalizeSec(self, sec):
        # Phase0: adjust with speed
        time = sec / self.speed
        # Phase1: transform sec in integer
        val = utils.getSmallestFactor(time)
        num = int(time * val)
        for d in [self.inputs, self.outputs]:
            for k in d:
                d[k] *= val
        # Phase2: normalize to 1 sec
        if num != 1:
            self.subBlocks[self.name] = num
        # Phase3: check if it can be simplified
        self.normalize()
    

    def normalize(self):
        # Reduce inputs-outputs-num to minimum terms
        s = set()
        for d in [self.subBlocks, self.inputs, self.outputs]:
            for k in d:
                s.add(d[k])
        GCD = utils.gcd(*s)
        if GCD != 1:
            for d in [self.subBlocks, self.inputs, self.outputs]:
                for k in d:
                    d[k] = int(d[k] / GCD)




class BlockManager():
    ASM1 = 0.50  #ASsemblingMachine1
    ASM2 = 0.75  #ASsemblingMachine2
    ASM3 = 1.25  #ASsemblingMachine3
    LREF = 1     #LiquidREFinery = OilRefinery + ChemicalPlant

    def __init__(self, printing = False, saving = False):
        self.DM = DataManager()
        self.printing = printing
        self.saving   = saving
    

    ##### PRINT AND SAVE ####################################################
    def print(self, block):
        if self.printing:
            print(f'<{block.name}>')
            print('SubBlocks:')
            for k,v in block.subBlocks.items():
                print(f'   {v: >6}x {k}')
            print('Inputs:')
            for k,v in block.inputs.items():
                print(f'   {v: >6}  {k}')
            print('Outputs:')
            for k,v in block.outputs.items():
                print(f'   {v: >6}  {k}')
            print()

    def save(self, block):
        if self.saving:
            block = {block.name: {"subBlocks": block.subBlocks, \
                                  "inputs"   : block.inputs,    \
                                  "outputs"  : block.outputs}   }
            self.DM.saveCustomBlock(block)
    
    def resetCustomBlocks(self):
        if self.saving:
            self.DM.resetCustomBlocks()

    def printAndSave(self, block):
        self.print(block)
        self.save(block)


    ##### GETTING ###########################################################
    def getBasicBlock(self, name, speed):
        data = self.DM.getBasicBlocks(name)
        block = Block(name, speed,            \
                      data['inputs'].copy(),  \
                      data['outputs'].copy(), \
                      {name: 1}               )
        block._normalizeIO()
        block._normalizeSec(data['sec'])
        return block


    ##### BLOCK OPERATIONS ##################################################
    def _compose2Blocks(self, name, blockIN:Block, blockOUT:Block):
        # Get the line where do the union.
        line = utils.getCommonLine(blockIN, blockOUT)
        if line:
            # Get MCM and adjust subBlocks
            blocksMCM = utils.lcm(blockIN.outputs[line], blockOUT.inputs[line])
            a = blockIN.getCopy()
            a.multiply(blocksMCM // blockIN.outputs[line])
            b = blockOUT.getCopy()
            b.multiply(blocksMCM // blockOUT.inputs[line])
        # Get new Block parts
        newBlockInputs  = utils.dictMerge(a.inputs, b.inputs, ignoreKey=line)
        newBlockOutputs = utils.dictMerge(a.outputs, b.outputs, ignoreKey=line)
        newSubBlocks    = utils.dictMerge(a.subBlocks, b.subBlocks)
        return Block(name, 1, newBlockInputs, newBlockOutputs, newSubBlocks)

    def composeBlocks(self, name, blocksArray):
        res = blocksArray[0]
        for i in range(1, len(blocksArray)):
            res = self._compose2Blocks(name, res, blocksArray[i])
        res.normalize()
        return res




# TEST
if __name__ == "__main__":
    print('\nTESTS: normalize')
    print('Test1...')
    t = Block('s', 1, {'i': 2}, {'o': 3}, {'s': 1})
    t._normalizeIO()
    t._normalizeSec(0.5)
    assert t.inputs    == {'i':4}
    assert t.subBlocks == {'s':1}
    assert t.outputs   == {'o':6}

    print('Test2...')
    t = Block('s', 1, {'i': 4}, {'o': 2}, {'s': 1})
    t._normalizeIO()
    t._normalizeSec(5)
    assert t.inputs    == {'i':4}
    assert t.subBlocks == {'s':5}
    assert t.outputs   == {'o':2}

    print('Test3...')
    t = Block('s', 1, {'i': 1}, {'o': 1}, {'s': 1})
    t._normalizeIO()
    t._normalizeSec(1.5)
    assert t.inputs    == {'i':2}
    assert t.subBlocks == {'s':3}
    assert t.outputs   == {'o':2}

    print('Test4...')
    t = Block('s', 1, {'i': 4}, {'o': 2}, {'s': 1})
    t._normalizeIO()
    t._normalizeSec(2)
    assert t.inputs    == {'i':2}
    assert t.subBlocks == {'s':1}
    assert t.outputs   == {'o':1}

    print('Test5...')
    t = Block('s', 1, {'i': 4, 'o':2}, {'o': 4}, {'s': 1})
    t._normalizeIO()
    t._normalizeSec(5)
    assert t.inputs    == {'i':4}
    assert t.subBlocks == {'s':5}
    assert t.outputs   == {'o':2}

    print('Test6...')
    t = Block('s', 1, {'i': 4, 'o':2}, {'o': 4}, {'s': 1})
    t._normalizeSec(5)
    t._normalizeIO()
    assert t.inputs    == {'i':4}
    assert t.subBlocks == {'s':5}
    assert t.outputs   == {'o':2}


    print('\nTESTS: copy + multiply + normalize')
    t1x = Block('s', 1, {'i': 2}, {'o': 1}, {'s': 1})
    print('Test Copy...')
    t3x = t1x.getCopy()
    assert t1x.inputs    == t3x.inputs
    assert t1x.subBlocks == t3x.subBlocks
    assert t1x.outputs   == t3x.outputs
    print('Test Multiply...')
    t3x.multiply(3)
    assert t3x.inputs    == {'i':6}
    assert t3x.subBlocks == {'s':3}
    assert t3x.outputs   == {'o':3}
    print('Test Normalize...')
    t3x.normalize()
    assert t1x.inputs    == t3x.inputs
    assert t1x.subBlocks == t3x.subBlocks
    assert t1x.outputs   == t3x.outputs


    print('\n\nSuccessful Tests!')