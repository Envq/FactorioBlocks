#!/usr/bin/env python3
import unittest

from src.blocks import BlockGraph, BlockNode, MachineType


ASM1 = MachineType.AssemblingMachine1
ASM2 = MachineType.AssemblingMachine2
ASM3 = MachineType.AssemblingMachine3
OIL = MachineType.OilRefinery


class TestBlockGraph(unittest.TestCase):
    def test_processdata(self):
        g = BlockGraph()
        neutral = MachineType.OilRefinery
        d = {'sec': 0.5, 'inputs': {'i': 2}, 'outputs': {'o': 3}}
        (n, i, o) = g._processData(d, neutral)
        self.assertEqual(n, 1, 'Test1: num')
        self.assertListEqual([(e.name,e.num) for e in i], [('i',4)], 'Test1: inputs')
        self.assertListEqual([(e.name,e.num) for e in o], [('o',6)], 'Test1: outputs')

        d = {'sec': 5.0, 'inputs': {'i': 4}, 'outputs': {'o': 2}}
        (n, i, o) = g._processData(d, neutral)
        self.assertEqual(n, 5, 'Test1: num')
        self.assertListEqual([(e.name,e.num) for e in i], [('i',4)], 'Test2: inputs')
        self.assertListEqual([(e.name,e.num) for e in o], [('o',2)], 'Test2: outputs')

        d = {'sec': 1.5, 'inputs': {'i': 1}, 'outputs': {'o': 1}}
        (n, i, o) = g._processData(d, neutral)
        self.assertEqual(n, 3, 'Test1: num')
        self.assertListEqual([(e.name,e.num) for e in i], [('i',2)], 'Test3: inputs')
        self.assertListEqual([(e.name,e.num) for e in o], [('o',2)], 'Test3: outputs')

        d = {'sec': 2.0, 'inputs': {'i': 4}, 'outputs': {'o': 2}}
        (n, i, o) = g._processData(d, neutral)
        self.assertEqual(n, 1, 'Test1: num')
        self.assertListEqual([(e.name,e.num) for e in i], [('i',2)], 'Test4: inputs')
        self.assertListEqual([(e.name,e.num) for e in o], [('o',1)], 'Test4: outputs')



class TestBlockNode(unittest.TestCase):
    def test(self):
        g = BlockGraph()
        # Create
        cc_data = {'sec': 0.5, 'inputs': {'CopperPlate': 1}, 'outputs': {'CopperCable': 2}}

        (n, i, o) = g._processData(cc_data, ASM1)
        cc_1 = BlockNode('cc', ASM1, n, i, o)
        self.assertEqual(cc_1.num, 1, 'cc: num')
        self.assertListEqual([(e.name,e.num) for e in cc_1.inputs],  [('CopperPlate',1)], 'cc: inputs')
        self.assertListEqual([(e.name,e.num) for e in cc_1.outputs], [('CopperCable',2)], 'cc: outputs')

        (n, i, o) = g._processData(cc_data, ASM2)
        cc_2 = BlockNode('cc', ASM2, n, i, o)
        self.assertEqual(cc_2.num, 2, 'cc: num')
        self.assertListEqual([(e.name,e.num) for e in cc_2.inputs],  [('CopperPlate',3)], 'cc: inputs')
        self.assertListEqual([(e.name,e.num) for e in cc_2.outputs], [('CopperCable',6)], 'cc: outputs')

        (n, i, o) = g._processData(cc_data, ASM3)
        cc_2 = BlockNode('cc', ASM3, n, i, o)
        self.assertEqual(cc_2.num, 2, 'cc: num')
        self.assertListEqual([(e.name,e.num) for e in cc_2.inputs],  [('CopperPlate',5)], 'cc: inputs')
        self.assertListEqual([(e.name,e.num) for e in cc_2.outputs], [('CopperCable',10)], 'cc: outputs')



class TestGeneral(unittest.TestCase):
    def test_connect(self):
        g = BlockGraph()
        ec = g.create('ElectronicCircuit', ASM1)
        cc = g.create('CopperCable', ASM1)
        gw = g.create('IronGearWheel', ASM1)
        i = g.create('Inserter', ASM1)
        g.connect(gw, i)
        g.connect(ec, i)
        g.connect(cc, ec)
        res = g.getRecipes()
        test = [{ \
            'inputs': {'CopperPlate': 3, 'IronPlate': 8}, \
            'outputs': {'Inserter': 2}, \
            'machines': {'Inserter': {'AssemblingMachine1': 2}, \
                        'CopperCable': {'AssemblingMachine1': 3}, \
                        'IronGearWheel': {'AssemblingMachine1': 2}, \
                        'ElectronicCircuit': {'AssemblingMachine1': 2}} \
        }]
        self.assertListEqual(test, res)
    
    def test_more_equal_machine1(self):
        g = BlockGraph()
        cc1 = g.create('CopperCable', ASM1)
        cc2 = g.create('CopperCable', ASM1)
        ec = g.create('ElectronicCircuit', ASM1)
        ac = g.create('AdvancedCircuit', ASM1)
        g.connect(cc2, ac)
        g.connect(cc1, ec)
        g.connect(ec, ac)
        res = g.getRecipes()
        test = [{ \
            'inputs': {'CopperPlate': 5, 'PlasticBar': 2,  'IronPlate': 2}, \
            'outputs': {'AdvancedCircuit': 1}, \
            'machines': {'AdvancedCircuit': {'AssemblingMachine1': 12}, \
                        'CopperCable': {'AssemblingMachine1': 5}, \
                        'ElectronicCircuit': {'AssemblingMachine1': 2}} \
        }]
        self.assertListEqual(test, res)
    
    def test_more_equal_machine2(self):
        g = BlockGraph()
        cc1 = g.create('CopperCable', ASM1)
        cc2 = g.create('CopperCable', ASM2)
        ec = g.create('ElectronicCircuit', ASM1)
        ac = g.create('AdvancedCircuit', ASM1)
        g.connect(cc2, ac)
        g.connect(cc1, ec)
        g.connect(ec, ac)
        res = g.getRecipes()
        test = [{ \
            'inputs': {'CopperPlate': 15, 'PlasticBar': 6,  'IronPlate': 6}, \
            'outputs': {'AdvancedCircuit': 3}, \
            'machines': {'AdvancedCircuit': {'AssemblingMachine1': 36}, \
                        'CopperCable': {'AssemblingMachine1': 9, 'AssemblingMachine2': 4}, \
                        'ElectronicCircuit': {'AssemblingMachine1': 6}} \
        }]
        self.assertListEqual(test, res)

    def test_aoc_lubriant(self):
        g = BlockGraph()
        aop = g.create('AdvancedOilProcessing', OIL)
        lig = g.create('LightOilCracking', OIL)
        lub = g.create('LubricantOilCracking', OIL)
        g.connect(aop, lig)
        g.connect(aop, lub)
        res = g.getRecipes()
        test = [{ \
            'inputs': {'Water': 190, 'CrudeOil': 200}, \
            'outputs': {'PetroleumGas': 170,'Lubricant': 50}, \
            'machines': {'AdvancedOilProcessing': {'OilRefinery': 10}, \
                        'LightOilCracking': {'OilRefinery': 6}, \
                        'LubricantOilCracking': {'OilRefinery': 5}} \
        }]
        self.assertListEqual(test, res)

    def test_aoc_petroleum1(self):
        g = BlockGraph()
        aop = g.create('AdvancedOilProcessing', OIL)
        lig = g.create('LightOilCracking', OIL)
        hea = g.create('HeavyOilCracking', OIL)
        g.connect(aop, hea)
        g.connect(hea, lig)
        res = g.getRecipes()
        test = [{ \
            'inputs': {'Water': 530, 'CrudeOil': 400}, \
            'outputs': {'PetroleumGas': 390}, \
            'machines': {'AdvancedOilProcessing': {'OilRefinery': 20}, \
                        'LightOilCracking': {'OilRefinery': 17}, \
                        'HeavyOilCracking': {'OilRefinery': 5}} \
        }]
        self.assertListEqual(test, res)

    def test_aoc_petroleum2(self):
        g = BlockGraph()
        aop = g.create('AdvancedOilProcessing', OIL)
        lig = g.create('LightOilCracking', OIL)
        hea = g.create('HeavyOilCracking', OIL)
        g.connect(aop, hea)
        g.connect(aop, lig)
        res = g.getRecipes()
        test = [{ \
            'inputs': {'Water': 530, 'CrudeOil': 400}, \
            'outputs': {'PetroleumGas': 390}, \
            'machines': {'AdvancedOilProcessing': {'OilRefinery': 20}, \
                        'LightOilCracking': {'OilRefinery': 17}, \
                        'HeavyOilCracking': {'OilRefinery': 5}} \
        }]
        self.assertListEqual(test, res)

    def test_clf_lubriant(self):
        g = BlockGraph()
        clf = g.create('CoalLiquefaction', OIL)
        lig = g.create('LightOilCracking', OIL)
        lub = g.create('LubricantOilCracking', OIL)
        g.connect(clf, lub)
        g.connect(clf, lig)
        res = g.getRecipes()
        test = [{ \
            'inputs': {'Water': 120, 'Steam': 300, 'Coal':60}, \
            'outputs': {'Lubricant': 390, 'PetroleumGas':140}, \
            'machines': {'CoalLiquefaction': {'OilRefinery': 30}, \
                        'LightOilCracking': {'OilRefinery': 8}, \
                        'LubricantOilCracking': {'OilRefinery': 39}} \
        }]
        self.assertListEqual(test, res)

    def test_clf_petroleum(self):
        g = BlockGraph()
        clf = g.create('CoalLiquefaction', OIL)
        hea = g.create('HeavyOilCracking', OIL)
        lig = g.create('LightOilCracking', OIL)
        g.connect(clf, hea)
        g.connect(hea, lig)
        res = g.getRecipes()
        test = [{ \
            'inputs': {'Water': 1410, 'Steam': 600, 'Coal':120}, \
            'outputs': {'PetroleumGas':670}, \
            'machines': {'CoalLiquefaction': {'OilRefinery': 60}, \
                        'LightOilCracking': {'OilRefinery': 55}, \
                        'HeavyOilCracking': {'OilRefinery': 39}} \
        }]
        self.assertListEqual(test, res)





if __name__ == '__main__':
    unittest.main()

    g = BlockGraph()
    aop = g.create('AdvancedOilProcessing', OIL)
    # clf = g.create('CoalLiquefaction', OIL)
    hea = g.create('HeavyOilCracking', OIL)
    lig = g.create('LightOilCracking', OIL)
    # lub = g.create('LubricantOilCracking', OIL)
    
    g.connect(hea, lig)
    g.connect(aop, lig)

    g.view(mergeResources=True)
    g.printRecipes()