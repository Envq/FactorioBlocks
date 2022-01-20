#!/usr/bin/env python3
from src.blocks_lib import test as blocks_lib_test
from src.utils import test as utils_test


print('##########################')
print('START TEST OF: utils')
utils_test()


print('\n\n\n##########################')
print('START TEST OF: blocks_lib')
blocks_lib_test()