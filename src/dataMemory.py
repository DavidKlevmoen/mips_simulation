'''
Implements CPU element for Data Memory in MEM stage.

Code written for inf-2200, University of Tromso
'''

from cpuElement import CPUElement
from memory import Memory
import unittest
from testElement import TestElement
from convert import *

import common

class DataMemory(Memory):
    def __init__(self, filename):
        Memory.__init__(self, filename)
        
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)
        
        assert(len(inputSources) == 2), 'DataMemory should have two inputs'  # address and writeData
        assert(len(outputValueNames) == 1), 'DataMemory has only one output'  # readData
        assert(len(control) == 2), 'DataMemory should have at least one control signal'  # memRead and memWrite
        assert(len(outputSignalNames) == 0), 'DataMemory should not have any control output'

        self.outputName = outputValueNames[0]
        self.inputAddress = inputSources[0][1]
        self.inputWriteData = inputSources[1][1]
        self.memRead = control[0][1]
        self.memWrite = control[1][1]

    def writeOutput(self):
        address = bin_to_int(self.inputValues[self.inputAddress])
        write_data = self.inputValues[self.inputWriteData]
        memRead = self.controlSignals[self.memRead]
        memWrite = self.controlSignals[self.memWrite]

        if memRead and memWrite:
            raise AssertionError("DataMemory cannot perform both read and write operations simultaneously!")

        elif memRead:
            # Perform memory read operation
            read_data = self.memory[address]
            self.outputValues[self.outputName] = int_to_32bin(read_data)

        elif memWrite:
            # Perform memory write operation
            self.memory[address] = write_data


class testDataMemory(unittest.TestCase):

    def setUp(self):
        self.dataMemory = DataMemory('fibonacci.mem')
        self.testInput = TestElement()
        self.testOutput = TestElement()

        self.testInput.connect(
            [],
            ['address', 'writeData'],
            [],
            ['memRead', 'memWrite']
        )

        self.dataMemory.connect(
            [(self.testInput, 'address'), (self.testInput, 'writeData')],
            ['readData'],
            [(self.testInput, 'memRead'), (self.testInput, 'memWrite')],
            []
        )

        self.testOutput.connect(
            [(self.dataMemory, 'readData')],
            [],
            [],
            []
        )

    def test_correct_behaviour(self):
        pass