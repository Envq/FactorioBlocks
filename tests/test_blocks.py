#!/usr/bin/env python3
import unittest

from src.blocks import BlockManager


BM = BlockManager()


class TestBlockManager(unittest.TestCase):
    def test_normalize(self):
        d = {'sec': 0.5, 'inputs': {'i': 2}, 'outputs': {'o': 3}}
        self.assertTupleEqual(BM._normalizeData(d), (1,{'i':4},{'o':6}), 'Test1')

        d = {'sec': 5.0, 'inputs': {'i': 4}, 'outputs': {'o': 2}}
        self.assertTupleEqual(BM._normalizeData(d), (5,{'i':4},{'o':2}), 'Test2')
        
        d = {'sec': 1.5, 'inputs': {'i': 1}, 'outputs': {'o': 1}}
        self.assertTupleEqual(BM._normalizeData(d), (3,{'i':2},{'o':2}), 'Test3')

        d = {'sec': 2.0, 'inputs': {'i': 4}, 'outputs': {'o': 2}}
        self.assertTupleEqual(BM._normalizeData(d), (1,{'i':2},{'o':1}), 'Test4')



if __name__ == '__main__':
    unittest.main()