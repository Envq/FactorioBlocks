#!/usr/bin/env python3
from src.blocks_lib import getBasicBlock, getCustomBlock, composeBlocks


if __name__ == "__main__":
    # EXAMPLE WITH LIQUIDS
    # r = getBasicBlock('AdvanceOilProcessing')
    # a = getBasicBlock('LubricantOilCracking')
    # b = getBasicBlock('HeavyOilCracking')
    # c = getBasicBlock('LightOilCracking')
    # l = getBasicBlock('CoalLiquefaction')
    # pet1 = composeBlocks('PetroleumGas1', [r, b, c])
    # pet1.print()
    # pet1.save()

    # EXAMPLE WITH SOLIDS
    # cc = getBasicBlock('CopperCable_ASM1')
    # cc.print()
    # ec = getBasicBlock('ElectronicCircuit_ASM1')
    # ec.print()

    # res = composeBlocks('EletronicCircuit', [cc, ec])
    # res.print()
    # res.save()

    igw = getBasicBlock('IronGearWheel_ASM1')
    igw.print()
    ars = getBasicBlock('AutomationRedScience_ASM1')
    ars.print()
