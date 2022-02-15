#!/usr/bin/env python3
import json


class DataManager:
    def __init__(self):
        self.path_basic  = 'data/basicBlocks.json'
        with open(self.path_basic) as file:
            self.basicData = json.load(file)


    def getBasicBlock(self, name):
        """Return the pointer to dict"""
        try:
            return self.basicData[name]
        except KeyError:
            print(f'Error: Not found in basicBlocks.json the object called "{name}"')
            exit(1)
