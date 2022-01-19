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


    def getBasicBlocks(self, name):
        """Return the pointer to dict"""
        try:
            return self.basicData[name]
        except KeyError:
            print(f'Error: Not found in basicBlocks.json the object called "{name}"')
            exit(1)


    def getCustomBlocks(self):
        return self.customData
    

    def resetCustomBlocks(self):
        with open(self.path_custom, 'w') as file:
            json.dump(dict(), file, ensure_ascii=True, indent=4, sort_keys=True)


    def saveCustomBlock(self, block):
        self.customData = {**self.customData, **block}
        with open(self.path_custom, 'w') as file:
            json.dump(self.customData, file, ensure_ascii=True, indent=4, sort_keys=True)
