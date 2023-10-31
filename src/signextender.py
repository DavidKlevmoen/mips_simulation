import unittest
from cpuElement import CPUElement
from testElement import TestElement


class signExtender(CPUElement):

    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 1)  # One input, 16-bit number
        assert(len(outputValueNames) == 1)  # One output, the extended number
        assert(len(control) == 0)  # No control signals
        assert(len(outputSignalNames)) == 0  # No output signals

        self.inputName = inputSources[0][1]

        self.outputName = outputValueNames[0]


    def writeOutput(self):
        self.input = self.inputValues[self.inputName][16:]
        print(self.input)
        if self.input[0] == '1':
            self.input = '1111111111111111' + self.input
        else:
            self.input = '0000000000000000' + self.input

        self.outputValues[self.outputName] = self.input

        #TODO check if works on negative numbers



class testsignExtender(unittest.TestCase):
    def setUp(self):
        self.signExtender = signExtender()
        self.testInput = TestElement()
        self.testOutput = TestElement()

        self.testInput.connect(
            [],
            ["16bitInput"],
            [],
            []
        )
        self.signExtender.connect(
            [(self.testInput, "16bitInput")],
            ["32bitOutput"],
            [],
            []
        )
        self.testOutput.connect(
            [(self.signExtender, "32bitOutput")],
            [],
            [],
            []
        )
    def test_correct_behaviour(self):
        self.testInput.setOutputValue("16bitInput", '00000000001')
        self.signExtender.readInput()
        self.signExtender.writeOutput()
        self.testOutput.readInput()

        print(self.testOutput.inputValues["32bitOutput"])

