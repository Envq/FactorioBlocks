#!/usr/bin/env python3
import unittest

from src.blocks import BlockManager, BlockNode, MachineType as MT


BM = BlockManager()


class TestBlockNode(unittest.TestCase):
    def test_init(self):
        ec = BM.getBlock('ElectronicCircuit', MT.assemblingMachine1)
        cc = BM.getBlock('CopperCable', MT.assemblingMachine1)
        ec.printRecipe()
        print('\n\n')
        ec.addInputBlock(cc)
        ec.printRecipe()

    
    

if __name__ == '__main__':
    unittest.main()