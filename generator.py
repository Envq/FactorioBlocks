#!/usr/bin/env python3
from src.blocks_lib import BlockManager


if __name__ == "__main__":
    # Setup
    BM = BlockManager( \
        printing = 1,  \
        saving   = 1   \
    )
    BM.resetCustomBlocks()


    # Liquid Generator
    # aop   = BM.getBasicBlock('AdvanceOilProcessing', BM.LREF)
    # cl    = BM.getBasicBlock('CoalLiquefaction',     BM.LREF)
    # lub   = BM.getBasicBlock('LubricantOilCracking', BM.LREF)
    # heavy = BM.getBasicBlock('HeavyOilCracking',     BM.LREF)
    # light = BM.getBasicBlock('LightOilCracking',     BM.LREF)

    # petroleumGas_AOP = BM.composeBlocks('PetroleumGas_AOP', [aop, heavy, light])
    # BM.printAndSave(petroleumGas_AOP)

    # lubriant_AOP = BM.composeBlocks('Lubriant_AOP', [aop, lub, light])
    # BM.printAndSave(lubriant_AOP)

    # petroleumGas_CL = BM.composeBlocks('petroleumGas_CL', [cl, heavy, light])
    # BM.printAndSave(petroleumGas_CL)

    # lubriant_CL = BM.composeBlocks('lubriant_CL', [cl, lub, light])
    # BM.printAndSave(lubriant_CL)


    # RedScience Generator
    i = 1
    for speed in [BM.ASM1, BM.ASM2, BM.ASM3]:
        ig = BM.getBasicBlock('IronGearWheel', speed)
        rs = BM.getBasicBlock('RedScience', speed)
        res = BM.composeBlocks(f'RedScience_ASM{i}', [ig, rs])
        i += 1
        BM.print(res)

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


