#!/usr/bin/env python3
import unittest

from src.blocks import BlocksManager, BlockMachine, BlocksChain, MachineType as MT


BM = BlocksManager()


class TestBlocksManager(unittest.TestCase):
    def test_processdata(self):
        neutral = MT.oilRefinery
        d = {'sec': 0.5, 'inputs': {'i': 2}, 'outputs': {'o': 3}}
        (n, i, o) = BM._processData(d, neutral)
        self.assertEqual(n, 1, 'Test1: num')
        self.assertListEqual([e.getData() for e in i], [('i',4)], 'Test1: inputs')
        self.assertListEqual([e.getData() for e in o], [('o',6)], 'Test1: outputs')

        d = {'sec': 5.0, 'inputs': {'i': 4}, 'outputs': {'o': 2}}
        (n, i, o) = BM._processData(d, neutral)
        self.assertEqual(n, 5, 'Test1: num')
        self.assertListEqual([e.getData() for e in i], [('i',4)], 'Test2: inputs')
        self.assertListEqual([e.getData() for e in o], [('o',2)], 'Test2: outputs')

        d = {'sec': 1.5, 'inputs': {'i': 1}, 'outputs': {'o': 1}}
        (n, i, o) = BM._processData(d, neutral)
        self.assertEqual(n, 3, 'Test1: num')
        self.assertListEqual([e.getData() for e in i], [('i',2)], 'Test3: inputs')
        self.assertListEqual([e.getData() for e in o], [('o',2)], 'Test3: outputs')

        d = {'sec': 2.0, 'inputs': {'i': 4}, 'outputs': {'o': 2}}
        (n, i, o) = BM._processData(d, neutral)
        self.assertEqual(n, 1, 'Test1: num')
        self.assertListEqual([e.getData() for e in i], [('i',2)], 'Test4: inputs')
        self.assertListEqual([e.getData() for e in o], [('o',1)], 'Test4: outputs')
    


class TestBlockMachine(unittest.TestCase):
    def test(self):
        # Create
        cc_data = {'sec': 0.5, 'inputs': {'CopperPlate': 1}, 'outputs': {'CopperCable': 2}}

        ASM = MT.assemblingMachine1
        (n, i, o) = BM._processData(cc_data, ASM)
        cc_1 = BlockMachine('cc', ASM, n, i, o)
        self.assertEqual(cc_1.num, 1, 'cc: num')
        self.assertListEqual([e.getData() for e in cc_1.inputs],  [('CopperPlate',1)], 'cc: inputs')
        self.assertListEqual([e.getData() for e in cc_1.outputs], [('CopperCable',2)], 'cc: outputs')

        ASM = MT.assemblingMachine2
        (n, i, o) = BM._processData(cc_data, ASM)
        cc_2 = BlockMachine('cc', ASM, n, i, o)
        self.assertEqual(cc_2.num, 2, 'cc: num')
        self.assertListEqual([e.getData() for e in cc_2.inputs],  [('CopperPlate',3)], 'cc: inputs')
        self.assertListEqual([e.getData() for e in cc_2.outputs], [('CopperCable',6)], 'cc: outputs')

        ASM = MT.assemblingMachine3
        (n, i, o) = BM._processData(cc_data, ASM)
        cc_2 = BlockMachine('cc', ASM, n, i, o)
        self.assertEqual(cc_2.num, 2, 'cc: num')
        self.assertListEqual([e.getData() for e in cc_2.inputs],  [('CopperPlate',5)], 'cc: inputs')
        self.assertListEqual([e.getData() for e in cc_2.outputs], [('CopperCable',10)], 'cc: outputs')





class TestGeneral(unittest.TestCase):
    def test_init(self):
        print('### DEBUG ############################')
        cc = BM.getBlock('CopperCable', MT.assemblingMachine1)
        ec = BM.getBlock('ElectronicCircuit', MT.assemblingMachine1)
        ptr = BM.createBlocksChainFrom(ec)
        cc.printState()
        ec.printState()
        print('######################################')
        ptr.addToTail(cc)
        cc.printState()
        ec.printState()
        print('######################################')

    
    

if __name__ == '__main__':
    unittest.main()