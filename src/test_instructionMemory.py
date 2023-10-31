'''
Implements CPU element for Instruction Memory in MEM stage.

Code written for inf-2200, University of Tromso
'''
import unittest
from cpuElement import CPUElement
from memory import Memory
from testElement import TestElement

class InstructionMemory(Memory):
    def __init__(self, filename):
        Memory.__init__(self, filename)
        
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)
        
        # TODO: check if self declarations are correct!
        assert(len(inputSources) == 1), 'InstructionMemory should have one input'
        assert(len(outputValueNames) == 1), 'InstructionMemory has only one output (instruction, that can be parsed)'
        assert(len(control) == 0), 'InstructionMemory has no control input'
        assert(len(outputSignalNames) == 0), 'InstructionMemory should not have any control output'
        self.inputField_address = inputSources[0][1]
        self.outputName = outputValueNames[0]

    def writeOutput(self):
        #TODO: check if self declarations are correct!
        instruction = self.memory[self.inputValues[self.inputField_address]]  # instruction fetched from memory
        self.outputValues[self.outputName] = instruction


class TestInstructionMemory(unittest.TestCase):
    def setUp(self):
        self.InstructionMemory = InstructionMemory('fibonacci.mem')
        self.testInput = TestElement()
        self.testOutput = TestElement()


        self.testInput.connect(
            [],
            ['address'],
            [],
            []
        )

        self.InstructionMemory.connect(
            [(self.testInput, 'address')],
            ['instruction'],
            [],
            []
        )

        self.testOutput.connect(
            [(self.InstructionMemory, 'instruction')],
            [],
            [],
            []
        )

    def test_correct_behavior(self):
        self.testInput.setOutputValue('address', 0xbfc00000)

        #print(self.InstructionMemory.memory)
        self.InstructionMemory.readInput()
        self.InstructionMemory.writeOutput()

        self.testOutput.readInput()
        output = self.testOutput.inputValues["instruction"]

        print(output)
        self.assertEqual(output, 0x0bf00080) #Henter fra output (Testoutput)

        #self.assertEqual(self.InstructionMemory.memory[4], 0x214A7FFF) #Henter rett fra instructionmemory

    
if __name__ == '__main__':
    unittest.main()