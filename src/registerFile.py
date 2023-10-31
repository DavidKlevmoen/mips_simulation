'''
Code written for inf-2200, University of Tromso
'''

import unittest
from testElement import TestElement
from cpuElement import CPUElement
from add import Add
import common
from convert import *


class RegisterFile(CPUElement):
    def __init__(self):
        # Dictionary mapping register number to register value
        self.register = {}
        # Note that we won't actually use all the registers listed here...
        self.registerNames = ['$zero', '$at', '$v0', '$v1', '$a0', '$a1', '$a2', '$a3',
                              '$t0', '$t1', '$t2', '$t3', '$t4', '$t5', '$t6', '$t7',
                              '$s0', '$s1', '$s2', '$s3', '$s4', '$s5', '$s6', '$s7',
                              '$t8', '$t9', '$k0', '$k1', '$gp', '$sp', '$fp', '$ra']
        # All registers default to 0
        for i in range(0, 32):
            self.register[i] = 0


    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources,
                           outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 3)  # instruciton, muxInstr_Reg, muxData_Reg
        assert(len(outputValueNames) == 2)  # readdata1, readdata2
        assert(len(control) == 1)  # regWrite

        self.inputName1 = inputSources[0][1]  # instruction
        self.inputName2 = inputSources[1][1]  # muxInstr_Reg
        self.inputName3 = inputSources[2][1]  # muxData_Reg

        self.controlName = control[0][1]

        self.outputvaluename1 = outputValueNames[0]
        self.outputvaluename2 = outputValueNames[1]



    def writeOutput(self):
        self.instruction = self.inputValues[self.inputName1][6:]
        self.control = self.controlSignals[self.controlName]

        self.readaddress1 = self.instruction[0:5]
        self.readaddress2 = self.instruction[5:10]
        self.write_register = self.inputValues[self.inputName2]
        self.write_data = self.inputValues[self.inputName3]
        # print(f"Instruction: {self.instruction}, readaddress1: {self.readaddress1}, readaddress2: {self.readaddress2},\
        # write_register: {self.write_register}, write_data: {self.write_data}, control: {self.control}")
        # TODO: Fix this

        if self.control == 1:  # regWrite
            if self.write_register != 0:
                if len(self.write_data) == 32:
                    self.register[bin_to_int(self.write_register)] = twos_comp(self.write_data)
                else:
                    self.register[bin_to_int(self.write_register)] = bin_to_int(self.write_data)
            else:
                self.register[0] = self.write_data

        self.outputValues[self.outputvaluename1] = self.register[bin_to_int(self.readaddress1)]
        self.outputValues[self.outputvaluename2] = self.register[bin_to_int(self.readaddress2)]

    def updateRegister(self, value):
        """
        Update the value of a register.
        value comes in as binary
        """

        self.register[bin_to_int(self.write_register)] = value

    def printAll(self):
        '''
        Print the name and value in each register.
        '''

        print()
        print("Register file")
        print("================")
        for i in range(0, 32):
            print("%s \t=> %s (%s)" % (self.registerNames[i], common.fromUnsignedWordToSignedWord(
                self.register[i]), hex(int(self.register[i]))[:-1]))
        print("================")
        print()
        print()


class TestRegisterFile(unittest.TestCase):
    def setUp(self):
        self.registerFile = RegisterFile()
        #print(self.registerFile.printAll())


        self.testInput = TestElement()
        self.testOutput = TestElement()
        self.adder = Add()

        self.testInput.connect(
            [],
            ['inputName'],
            [],
            []
        )

        self.registerFile.connect(
            [(self.testInput, 'inputName'), (self.adder, 'sum')],
            ['readdata1', 'readdata2'],
            [],
            []
        )

        self.testOutput.connect(
            [(self.registerFile, 'readdata1'), (self.registerFile, "readdata2")],
            [],
            [],
            []
        )
        self.adder.connect(
            [(self.registerFile, 'readdata1'), (self.registerFile, 'readdata2')],
            ['sum'],
            [],
            []
        )
    def test_correct_behavior(self):
        self.testInput.setOutputValue('inputName', bin(0x012A4820))

        self.registerFile.readInput()
        self.registerFile.writeOutput()
        #self.testOutput.readInput()
        #output = self.testOutput.inputValues['readdata1']
        #output2 = self.testOutput.inputValues['readdata2']

        self.adder.readInput()
        self.adder.writeOutput()
        self.registerFile.updateRegister(self.adder.outputValues['sum'])
        print("-------------------")
        print(self.adder.outputValues['sum'])
        print("-------------------")
        self.registerFile.printAll()


if __name__ == '__main__':
    unittest.main()
