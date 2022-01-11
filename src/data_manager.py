#!/usr/bin/env python3
import json


class DataManager:
    def __init__(self):
        path_basic  = 'src/data/basicBlocks.json'
        path_custom = 'src/data/customBlocks.json'
        with open(path_basic) as file:
            self.BasicData = json.load(file)
        with open(path_custom) as file:
            self.CustomData = json.load(file)

    def getBasicBlocks(self):
        return self.BasicData
    




# TESTS
if __name__ == "__main__":
    dm = DataManager()
    print(dm.getBasicBlock()['AdvanceOilProcessing'])
