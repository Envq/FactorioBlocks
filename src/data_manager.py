#!/usr/bin/env python3
import json


class DataManager:
    def __init__(self):
        self.path_basic  = 'src/data/basicBlocks.json'
        self.path_custom = 'src/data/customBlocks.json'
        with open(self.path_basic) as file:
            self.basicData = json.load(file)
        with open(self.path_custom) as file:
            self.customData = json.load(file)

    def getBasicBlocks(self):
        return self.basicData

    def getCustomBlock(self):
        return self.customData
    
    def saveCustomBlock(self, block):
        self.customData = {**self.customData, **block}
        with open(self.path_custom, 'w') as file:
            json.dump(self.customData, file, ensure_ascii=True, indent=4, sort_keys=True)

    




# TESTS
if __name__ == "__main__":
    dm = DataManager()
    print(dm.getBasicBlock()['AdvanceOilProcessing'])
