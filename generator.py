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
    aop   = BM.getBasicBlock('AdvanceOilProcessing', BM.LREF)
    cl    = BM.getBasicBlock('CoalLiquefaction',     BM.LREF)
    lub   = BM.getBasicBlock('LubricantOilCracking', BM.LREF)
    heavy = BM.getBasicBlock('HeavyOilCracking',     BM.LREF)
    light = BM.getBasicBlock('LightOilCracking',     BM.LREF)

    petroleumGas_AOP = BM.composeBlocks('PetroleumGas_AOP', [aop, heavy, light])
    BM.printAndSave(petroleumGas_AOP)

    lubriant_AOP = BM.composeBlocks('Lubriant_AOP', [aop, lub, light])
    BM.printAndSave(lubriant_AOP)

    petroleumGas_CL = BM.composeBlocks('petroleumGas_CL', [cl, heavy, light])
    BM.printAndSave(petroleumGas_CL)

    lubriant_CL = BM.composeBlocks('lubriant_CL', [cl, lub, light])
    BM.printAndSave(lubriant_CL)


    # RedScience Generator
    # ig = BM.getBasicBlock('IronGearWheel', BM.ASM1)
    # BM.print(ig)
    # rs = BM.getBasicBlock('RedScience', BM.ASM1)
    # BM.print(rs)


    # cc = BM.getBasicBlock('CopperCable', BM.ASM1)
    # ec = BM.getBasicBlock('ElectronicCircuit', BM.ASM1)
    # res = BM.composeBlocks('EletronicCircuit', [cc, ec])
    # ec.save()




