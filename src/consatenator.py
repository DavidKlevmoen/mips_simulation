from cpuElement import CPUElement
import unittest
from testElement import TestElement
from convert import bin_to_int, int_to_32bin, twos_comp
from add import Add
from constant import Constant


class Consatenator(CPUElement):
    def __init(self):
        pass

    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert (len(inputSources) == 2), 'Consatenator should have two inputs'
        assert (len(outputValueNames) == 1), 'Consatenator has only one output'
        assert (len(control) == 0), 'Consatenator should not have any control signal'
        assert (len(outputSignalNames) == 0), 'Consatenator should not have any control output'

        self.inputName1 = inputSources[0][1]  # From Adder, Should be int
        self.inputName2 = inputSources[1][1]  # From ShiftLeft2
        self.outputName = outputValueNames[0]

    def writeOutput(self):
        self.input1 = self.inputValues[self.inputName1]
        self.input2 = self.inputValues[self.inputName2]

        self.input1 = int_to_32bin(self.input1)
        if isinstance(self.input2, int):
            self.input2 = int_to_32bin(self.input2)

        self.input2 = self.input2[4:]

        # print(f"input1: {self.input1}, input2: {self.input2}")
        # print(len(self.input1), len(self.input2))
        self.outputtest = self.input1[0:4] + self.input2
        self.outputtest = bin_to_int(self.outputtest)
        self.outputValues[self.outputName] = self.outputtest


class TestConsatenator(unittest.TestCase):
    def setUp(self):
        self.Consatenator = Consatenator()
        self.testInput = TestElement()  # From Adder

        self.adder = Add()

        self.testInput2 = TestElement()  # From ShiftLeft2

        self.constant = Constant(4)

        self.testOutput = TestElement()

        self.constant.connect(
            [],
            ['constant'],
            [],
            []
        )

        self.testInput.connect(
            [],
            ['orginaladdress'],
            [],
            []
        )

        self.adder.connect(
            [(self.testInput, 'orginaladdress'), (self.constant, 'constant')],
            ['upper4'],
            [],
            []
        )

        self.testInput2.connect(
            [],
            ['Shiftedleft'],
            [],
            []
        )

        self.Consatenator.connect(
            [(self.adder, 'upper4'), (self.testInput2, 'Shiftedleft')],
            ['output'],
            [],
            []
        )

        self.testOutput.connect(
            [(self.Consatenator, 'output')],
            [],
            [],
            []
        )

    def test_correct_behaviour(self):
        self.testInput.setOutputValue('originaladdress', 0x00000158)
        self.testInput2.setOutputValue('Shiftedleft', 0b000000000000000000101000)
        self.testInput.readInput()
        self.testInput2.readInput()
        self.testInput.writeOutput()
        self.testInput2.writeOutput()

        self.Consatenator.readInput()
        self.Consatenator.writeOutput()

        self.testOutput.readInput()
        output = self.testOutput.inputValues["output"]
        print("output: ", output)


if __name__ == '__main__':
    unittest.main()