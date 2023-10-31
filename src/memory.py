'''
Implements base class for memory elements.

Note that since both DataMemory and InstructionMemory are subclasses of the Memory
class, they will read the same memory file containing both instructions and data
memory initially, but the two memory elements are treated separately, each with its
own, isolated copy of the data from the memory file.

Code written for inf-2200, University of Tromso
'''

from cpuElement import CPUElement
import common


class Memory(CPUElement):
    def __init__(self, filename):
        # Dictionary mapping memory addresses to data
        # Both key and value must be of type 'long'
        self.memory = {}
        
        self.initializeMemory(filename)
    
    def initializeMemory(self, filename):
        '''
        Helper function that reads initializes the data memory by reading input
        data from a file.
        '''
        
        # TODO: Remove this and replace with your implementation!
        try:
            with open(filename, 'r') as f:
                for line in f:
                    if line.startswith('#') or len(line.strip().split('\t')) != 3:  # Skip comments and empty lines
                        continue
                    # else:
                    address, data, comment = line.strip().split('\t')  # Split the line into address and data
                    address = int(address, 16)  # Convert to int
                    data = int(data, 16)  # Convert to int
                    self.memory[address] = data
                    # binary_data = format(int(data, 16), '032b')
                    # print(f"Address: {address}, data: {data}, binary: {binary_data}")

        except FileNotFoundError:
            print(f"File {filename} not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
        
    def printAll(self):
        for key in sorted(self.memory.keys()):
            print("%s\t=> %s\t(%s)" % (hex(int(key)), common.fromUnsignedWordToSignedWord(self.memory[key]), hex(int(self.memory[key]))))
