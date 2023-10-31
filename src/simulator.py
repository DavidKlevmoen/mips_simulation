'''
Code written for inf-2200, University of Tromso
'''

import sys
from mipsSimulator2 import MIPSSimulator
from memory import Memory

def runSimulator(sim):
    # TODO: Replace this with your own main loop!
    while (1):
        print(f"CURRENT ADDRESS: {sim.pc.currentAddress()}")
        if Memory(memoryFile).memory[sim.pc.currentAddress()] == 13:  # if instruction is break, then break
            break
        sim.tick()


if __name__ == '__main__':
    # assert(len(sys.argv) == 2), 'Usage: python %s memoryFile' % (sys.argv[0],)
    memoryFile = 'src/testing.mem'#sys.argv[1]
    
    simulator = MIPSSimulator(memoryFile)
    runSimulator(simulator)
