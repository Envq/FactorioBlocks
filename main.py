#!/usr/bin/env python3
from src.blocks_lib import getBasicBlock, getCustomBlock, composeBlocks


if __name__ == "__main__":
    r = getBasicBlock('AdvanceOilProcessing')
    a = getBasicBlock('LubricantOilCracking')
    b = getBasicBlock('HeavyOilCracking')
    c = getBasicBlock('LightOilCracking')
    l = getBasicBlock('CoalLiquefaction')
    pet2 = getCustomBlock('PetroleumGas2')
    pet2.print()

    # pet1 = composeBlocks('PetroleumGas1', [r, b, c])
    # pet1.print()
    # pet1.save()

    # lub1 = composeBlocks('Lubriant1', [r, a, c])
    # lub1.print()
    # lub1.save()

    # lub2 = composeBlocks('Lubriant2', [l, a, c])
    # lub2.print()
    # lub2.save()

