from cpuElement import CPUElement


class AluControl(CPUElement):
    def __init__(self):
        self.instFunc = 0
        self.aluOp = 'xx'  # 00 = add, 01 = sub, 10 = and, 11 = or

    def connect(self, input, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, input, outputValueNames, control, outputSignalNames)

        assert(len(input) == 1), 'AluControl should have one input (instruction)'
        assert(len(outputValueNames) == 0), 'AluControl has no output'
        assert(len(control) == 2), 'AluControl should have two control signal (aluOp and overflow)'
        assert(len(outputSignalNames) == 2), 'AluControl should have (add, sub, and, or) and overflow'

        # function field
        self.inputName = input[0][1]
        self.controlName1 = control[0][1]
        self.controlName2 = control[1][1]
        self.outputName1 = outputSignalNames[0]
        self.outputName2 = outputSignalNames[1]

    def writeOutput(self):
        pass  # AluControl does not have any output

    def setControlSignals(self):

        instFunc = self.inputValues[self.inputName][26:32]  # get function field from instruction
        aluOp = self.controlSignals[self.controlName1]  # get aluOp value from Controls
        overflow = self.controlSignals[self.controlName2] # get overflow value from Controls

        # for R-types:
        if aluOp == '10':
            # add:
            if instFunc == '100000':
                self.outputControlSignals[self.outputName1] = '0010'
                self.outputControlSignals[self.outputName2] = 1
            # addu:
            elif instFunc == '100001':
                self.outputControlSignals[self.outputName1] = '0010'
                self.outputControlSignals[self.outputName2] = 0
            # sub:
            elif instFunc == '100010':
                self.outputControlSignals[self.outputName1] = '0110'
                self.outputControlSignals[self.outputName2] = 1
            # subu:
            elif instFunc == '100011':
                self.outputControlSignals[self.outputName1] = '0110'
                self.outputControlSignals[self.outputName2] = 0
            # AND:
            elif instFunc == '100100':
                self.outputControlSignals[self.outputName1] = '0000'
            # OR:
            elif instFunc == '100101':
                self.outputControlSignals[self.outputName1] = '0001'
                self.outputControlSignals[self.outputName2] = 0
            # NOR:
            elif instFunc == '100111':
                self.outputControlSignals[self.outputName1] = '1000'  # made own control signal for NOR
                self.outputControlSignals[self.outputName2] = 0
            # slt:
            elif instFunc == '101010':
                self.outputControlSignals[self.outputName1] = '0111'
                self.outputControlSignals[self.outputName2] = 1

        # for LW, SW, addiu:
        elif aluOp == '00':
            # should always send add:
            self.outputControlSignals[self.outputName1] = '0010'
            self.outputControlSignals[self.outputName2] = overflow

        # for BEQ and BNE:
        elif aluOp == '01':
            # should always send sub:
            self.outputControlSignals[self.outputName1] = '0110'
            self.outputControlSignals[self.outputName2] = overflow

        # for slt:
        elif aluOp == '11':
            # should always send slt:
            self.outputControlSignals[self.outputName1] = '0111'
            self.outputControlSignals[self.outputName2] = overflow
