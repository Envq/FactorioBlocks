#!/usr/bin/env python3
from src.blocks_lib import Block, printBasicBlocksList, getBlockFromName, multiplyBlocks, composeBlocks


if __name__ == "__main__":
    a = getBlockFromName('AdvanceOilProcessing')
    b = getBlockFromName('LubricantOilCracking')
    c = getBlockFromName('LightOilCracking')

    res = composeBlocks('Lubriant', composeBlocks('TMP', a, b), c)
    res.print()



# if __name__ == "__main__":
#     print('STEP 1:')
#     print('Given: ')
#     a = getBlockFromName('AdvanceOilProcessing')
#     print(f'- {a.name}')
#     b = getBlockFromName('LubricantOilCracking')
#     print(f'- {b.name}')

#     print('\nYou get:')
#     c = composeBlocks('PartialLubriant', a, b)
#     c.print()
#     print('-----------------------------------\n')


#     print('STEP 2:')
#     print('Given: ')
#     print(f'- {c.name}')
#     d = getBlockFromName('LightOilCracking')
#     print(f'- {d.name}')

#     print('\nYou get:')
#     e = composeBlocks('Lubriant', c, d)
#     e.print()