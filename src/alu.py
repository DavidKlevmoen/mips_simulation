from cpuElement import CPUElement
from common import Overflow
from convert import *

class Alu(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 2), 'Alu should have two inputs'
        assert(len(outputValueNames) == 1), 'Alu has only one output'
        assert(len(control) == 4), 'Alu should have four control signal: aluControl, beq, bne and overflow'
        assert(len(outputSignalNames) == 1), 'Alu should have one control output (zero)'

        self.inputName1 = inputSources[0][1]
        self.inputName2 = inputSources[1][1]

        self.outputName = outputValueNames[0]
        self.outputControlSignalName = outputSignalNames[0]

        self.controlName1 = control[0][1]  # aluControl
        self.controlName2 = control[1][1]  # beq
        self.controlName3 = control[2][1]  # bne
        self.controlName4 = control[3][1]  # overflow

        self.result = 0
        self.zero = 0



    def writeOutput(self):

        self.aluc = self.controlSignals[self.controlName1]
        self.beq = self.controlSignals[self.controlName2]
        self.bne = self.controlSignals[self.controlName3]
        self.overflow = self.controlSignals[self.controlName4]

        self.input1 = self.inputValues[self.inputName1]
        self.input2 = self.inputValues[self.inputName2]

        self.outputControlSignals[self.outputControlSignalName] = 0

        # makes input to integers
        if type(self.input1) is not int:
            self.input1 = bin_to_int(self.input1)
        if type(self.input2) is not int:
            self.input2 = bin_to_int(self.input2)
        # TODO: write output
        if self.aluc == "0010":  # Add
            self.result = self.input1 + self.input2
        elif self.aluc == "0110":  # Sub
            self.result = self.input1 - self.input2
        elif self.aluc == "0000":  # AND
            self.result = self.input1 & self.input2
        elif self.aluc == "0001":  # OR
            self.result = self.input1 | self.input2
        elif self.aluc == "1000":  # NOR
            self.result = ~(self.input1 | self.input2)
        elif self.aluc == "0111":  # Set less than
            if self.input1 < self.input2:
                self.result = 1
            else:
                self.result = 0

        # branch if equal (beq)
        if self.result == 0 and self.beq == 1:
            self.outputControlSignals[self.outputControlSignalName] = 1

        # branch if not equal (bne)
        if self.result != 0 and self.bne == 1:
            self.outputControlSignals[self.outputControlSignalName] = 1


        else:
            self.result = int_to_32bin(self.result)
            print("------------------")
            print(self.result)
            print("------------------")

            if self.overflow:
                print("Is self.overflow.")
                # checks if the result is too big for 32 bits=
                if self.result[0] == '1' or self.result[0] == '-':
                    # if both inputs are positive
                    if int_to_32bin(self.input1)[0] == '0' and int_to_32bin(self.input2)[0] == '0':
                        Overflow("Overflow error")
                        self.result = '0' + '1'*31  # overflow has occurred and the result is max size

                elif self.result[0] == '0':
                    if int_to_32bin(self.input1) == '1' and int_to_32bin(self.input2)[0] == '1':
                        Overflow("Overflow error")
                        self.result = '1' + '0'*31
                else:
                    self.result = bin_to_int(self.result)
                    if self.result < int_to_32bin(LOWER_LIMIT):
                        self.result = '0' + '1'*31
                    elif self.result > UPPER_LIMIT:
                        self.result = '0' + '1'*31

            self.outputValues[self.outputName] = self.result
