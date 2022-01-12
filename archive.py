#!/usr/bin/env python3
from src.blocks_lib import printCustomBlocksList, getCustomBlock


def help():
    print('Commands availables:')
    print('- help: print this.')
    print('- list: return the blocks list.')
    print('- get NAME: return the block selected by NAME.')
    print('- quit: to exit')


if __name__ == "__main__":
    print('Welcome...')
    help()

    while True:
        cmd = input('Select command: ')
        if cmd == 'quit' or cmd == 'q':
            break
        elif cmd == 'help':
            help()
        elif cmd == 'list':
            printCustomBlocksList()
        elif cmd[:3] == 'get':
            cmds = cmd.split()
            block = getCustomBlock(cmds[1])
            block.print()
        print()
