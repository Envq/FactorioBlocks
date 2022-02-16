#!/usr/bin/env python3
from src.blocks import BlockGraph, BlockNode, MachineType


ASM1 = MachineType.AssemblingMachine1
ASM2 = MachineType.AssemblingMachine2
ASM3 = MachineType.AssemblingMachine3
OIL = MachineType.OilRefinery
CHM = MachineType.ChemicalPlant



if __name__ == '__main__':
    VIEW_SCIENCE = True
    VIEW_OIL1    = True
    VIEW_OIL2    = True




    # --- OILs PRODUCT 1 ---------------------------------------
    oil = BlockGraph()
    refinery = oil.create('AdvancedOilProcessing', OIL)
    light = oil.create('LightOilCracking', CHM)
    lubricant = oil.create('LubricantOilCracking', CHM)
    oil.connect(refinery, light)
    oil.connect(refinery, lubricant)
    oil.generateGraphRecipe(view=VIEW_OIL1, name='AdvancedOilProcessing_Lubricant')

    oil = BlockGraph()
    refinery = oil.create('AdvancedOilProcessing', OIL)
    light = oil.create('LightOilCracking', CHM)
    heavy = oil.create('HeavyOilCracking', CHM)
    oil.connect(refinery, heavy)
    oil.connect(heavy, light)
    oil.generateGraphRecipe(view=VIEW_OIL1, name='AdvancedOilProcessing_petroleum')


    oil = BlockGraph()
    liquefaction = oil.create('CoalLiquefaction', OIL)
    light = oil.create('LightOilCracking', CHM)
    lubricant = oil.create('LubricantOilCracking', CHM)
    oil.connect(liquefaction, lubricant)
    oil.connect(liquefaction, light)
    oil.generateGraphRecipe(view=VIEW_OIL1, name='CoalLiquefaction_Lubricant')


    oil = BlockGraph()
    liquefaction = oil.create('CoalLiquefaction', OIL)
    heavy = oil.create('HeavyOilCracking', CHM)
    light = oil.create('LightOilCracking', CHM)
    oil.connect(liquefaction, heavy)
    oil.connect(heavy, light)
    oil.generateGraphRecipe(view=VIEW_OIL1, name='CoalLiquefaction_petroleum')






    # --- OILs PRODUCT 2 ---------------------------------------
    chm = BlockGraph()
    plastic = chm.create('PlasticBar', OIL)
    chm.generateGraphRecipe(view=VIEW_OIL2, name='Plastic')


    chm = BlockGraph()
    sulfur = chm.create('Sulfur', CHM)
    acid = chm.create('SulfuricAcid', CHM)
    chm.connect(sulfur, acid)
    chm.generateGraphRecipe(view=VIEW_OIL2, name='SulfuricAcid')






    # --- AUTOMATION SCIENCE -----------------------------------
    science = BlockGraph()
    ASM = MachineType.AssemblingMachine1
    target = science.create('AutomationSciencePack', ASM)
    gear_1 = science.create('IronGearWheel', ASM)
    science.connect(gear_1, target)
    science.generateGraphRecipe(view=VIEW_SCIENCE, name='AutomationSciencePack')


    # --- LOGISTIC SCIENCE -------------------------------------
    science = BlockGraph()
    ASM = MachineType.AssemblingMachine1
    target = science.create('LogisticSciencePack', ASM)
    inserter = science.create('Inserter', ASM)
    circuit = science.create('ElectronicCircuit', ASM1)
    cable = science.create('CopperCable', ASM1)
    gear_1 = science.create('IronGearWheel', ASM1)
    belt = science.create('TransportBelt', ASM)
    gear_2 = science.create('IronGearWheel', ASM1)
    science.connect(cable, circuit)
    science.connect(circuit, inserter)
    science.connect(gear_1, inserter)
    science.connect(inserter, target)
    science.connect(gear_2, belt)
    science.connect(belt, target)
    science.generateGraphRecipe(view=VIEW_SCIENCE, name='LogisticSciencePack')


    # --- MILITARY SCIENCE -------------------------------------
    science = BlockGraph()
    ASM = MachineType.AssemblingMachine1
    target = science.create('MilitarySciencePack', ASM)
    magazineL2 = science.create('PiercingRoundsMagazine', ASM)
    magazineL1 = science.create('FirearmMagazine', ASM1)
    grenade = science.create('Grenade', ASM)
    wall = science.create('Wall', ASM1)
    science.connect(magazineL1, magazineL2)
    science.connect(magazineL2, target)
    science.connect(grenade, target)
    science.connect(wall, target)
    science.generateGraphRecipe(view=VIEW_SCIENCE, name='MilitarySciencePack')


    # --- CHEMICAL SCIENCE -------------------------------------
    science = BlockGraph()
    ASM = MachineType.AssemblingMachine1
    target = science.create('ChemicalSciencePack', ASM)
    circuitL2 = science.create('AdvancedCircuit', ASM)
    cable_1 = science.create('CopperCable', ASM1)
    circuitL1 = science.create('ElectronicCircuit', ASM1)
    cable_2 = science.create('CopperCable', ASM1)
    # plastic = science.create('PlasticBar', ASM1)
    engine = science.create('EngineUnit', ASM1)
    gear = science.create('IronGearWheel', ASM1)
    pipe = science.create('Pipe', ASM1)
    # sulfur = science.create('Sulfur', ASM)
    science.connect(cable_2, circuitL1)
    science.connect(cable_1, circuitL2)
    science.connect(circuitL1, circuitL2)
    # science.connect(plastic, circuitL2)
    science.connect(gear, engine)
    science.connect(pipe, engine)
    science.connect(circuitL2, target)
    science.connect(engine, target)
    # science.connect(sulfur, target)
    science.generateGraphRecipe(view=VIEW_SCIENCE, name='ChemicalSciencePack')