#!/usr/bin/env python3
from fractions import Fraction
from blocks_old import BlockManager


if __name__ == "__main__":
    # Setup
    BM = BlockManager( \
        printing = 1,  \
        saving   = 0   \
    )
    BM.resetCustomBlocks()


    # Liquid Generator
    # aop   = BM.getBasicBlock('AdvanceOilProcessing', BM.LREF)
    # cl    = BM.getBasicBlock('CoalLiquefaction',     BM.LREF)
    # lub   = BM.getBasicBlock('LubricantOilCracking', BM.LREF)
    # heavy = BM.getBasicBlock('HeavyOilCracking',     BM.LREF)
    # light = BM.getBasicBlock('LightOilCracking',     BM.LREF)

    # petroleumGas_AOP = BM.composeBlocksArray('PetroleumGas_AOP', [aop, heavy, light])
    # BM.printAndSave(petroleumGas_AOP)

    # lubriant_AOP = BM.composeBlocksArray('Lubriant_AOP', [aop, lub, light])
    # BM.printAndSave(lubriant_AOP)

    # petroleumGas_CL = BM.composeBlocksArray('petroleumGas_CL', [cl, heavy, light])
    # BM.printAndSave(petroleumGas_CL)

    # lubriant_CL = BM.composeBlocksArray('lubriant_CL', [cl, lub, light])
    # BM.printAndSave(lubriant_CL)


    # RedScience Generator
    # i = 1
    # for speed in [BM.ASM1, BM.ASM2, BM.ASM3]:
    #     ig = BM.getBasicBlock('IronGearWheel', speed)
    #     rs = BM.getBasicBlock('AutomationSciencePack', speed)
    #     res = BM.composeBlocks(f'RedScience_ASM{i}', [ig, rs])
    #     i += 1
    #     BM.print(res)

    # cc = BM.getBasicBlock('CopperCable', BM.ASM1)
    # ec = BM.getBasicBlock('ElectronicCircuit', BM.ASM1)
    # res = BM.composeBlocks('EletronicCircuit', [cc, ec])
    # ec.save()

    # eb = BM.getBasicBlock('EmptyBarrel', BM.ASM1)
    # BM.print(eb)

    # eb1 = BM.getBasicBlock('EmptyBarrel', BM.ASM1)
    # BM.print(eb1)

    # eb2 = BM.getBasicBlock('EmptyBarrel', BM.ASM2)
    # BM.print(eb2)

    # eb3 = BM.getBasicBlock('EmptyBarrel', BM.ASM3)
    # BM.print(eb3)




    # speed = BM.ASM1
    # cc = BM.getBasicBlock('CopperCable', speed)
    # ec = BM.getBasicBlock('ElectronicCircuit', speed)
    # ac = BM.getBasicBlock('AdvancedCircuit', speed)

    # r1 = BM.compose2Blocks('ElectronicCircuit', cc, ec)
    # r2 = BM.compose2Blocks('TMP', r1, ac)
    # r3 = BM.compose2Blocks('AdvancedCircuit', cc, r2)
    # BM.print(r3)

    # r = BM.composeBlocks('AdvancedCircuit', ac, [cc, ec])
    # BM.print(r)



    # Red Science
    # speed = BM.ASM1
    # ig = BM.getBasicBlock('IronGearWheel', speed)
    # BM.print(ig)
    # rs = BM.getBasicBlock('AutomationSciencePack', speed)
    # BM.print(rs)
    # print('------------------------------------')
    # res = BM.composeBlocks(f'RedScience', rs, [ig])
    # BM.print(res)


    # Purple Science
    # i = 1
    # for speed in [BM.ASM1, BM.ASM2, BM.ASM3]:
    #     a = BM.getBasicBlock('EletricFurnace', speed)
    #     b = BM.getBasicBlock('AdvancedCircuit', speed)
    #     c = BM.getBasicBlock('CopperCable', speed)
    #     d = BM.getBasicBlock('ElectronicCircuit', speed)
    #     f = BM.getBasicBlock('ProductivityModule', speed)
    #     g = BM.getBasicBlock('Rail', speed)
    #     h = BM.getBasicBlock('IronStick', speed)
    #     i = BM.getBasicBlock('ProductionSciencePack', speed)

    #     # r1 = BM.composeBlocks('EletricFurnace', a, [b, c, d])
    #     # BM.print(r1)
    #     # r2 = BM.composeBlocks('ProductivityModule', f, [b, c, d])
    #     # BM.print(r2)
    #     # r3 = BM.composeBlocks('Rail', g, [h])
    #     # BM.print(r3)
    #     # print('------------------------------------')

    #     res = BM.composeBlocks('PurpleScience', i, [a, b, c, d, f, g, h])
    #     BM.print(res)
    #     print('#Assembler = ', res.getNumOfMachines())


    speed = BM.ASM1
    cc = BM.getBasicBlock('CopperCable', speed)
    ec = BM.getBasicBlock('ElectronicCircuit', speed)
    res = BM.compose2Blocks('ElectronicCircuit', cc, ec)
    BM.print(res)


    # speed = BM.ASM1
    # a = BM.getBasicBlock('EletricFurnace', speed)
    # b = BM.getBasicBlock('AdvancedCircuit', speed)
    # c = BM.getBasicBlock('CopperCable', speed)
    # d = BM.getBasicBlock('ElectronicCircuit', speed)
    # f = BM.getBasicBlock('ProductivityModule', speed)
    # g = BM.getBasicBlock('Rail', speed)
    # h = BM.getBasicBlock('IronStick', speed)
    # i = BM.getBasicBlock('ProductionSciencePack', speed)
    # BM.print(i)

    # res = BM.composeBlocks('PurpleScience', i, [a, b, c, d, f, g, h])
    # BM.print(res)

    # print('with Rail')
    # res = BM.composeBlocks('PurpleScience', i, [a, b, c, d, f, h])
    # BM.print(res)

    # print('with ProductivityModule')
    # res = BM.composeBlocks('PurpleScience', i, [a, b, c, d, g, h])
    # BM.print(res)

    # print('with EletricFurnace')
    # res = BM.composeBlocks('PurpleScience', i, [b, c, d, g, h])
    # BM.print(res)