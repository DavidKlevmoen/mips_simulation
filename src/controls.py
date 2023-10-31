
from cpuElement import CPUElement


class Controls(CPUElement):
    def __init__(self):
        self.regDst = 0
        self.jump = 0
        self.beq = 0
        self.bne = 0
        self.memRead = 0
        self.memToReg = 0
        self.aluOp = 'xx'  # 00 = LW/SW, 01 = beq/bnq, 10 = R-type, 11 = slt
        self.memWrite = 0
        self.aluSrc = 'xx'  # 00 = register, 01 = sign-extend
        self.regWrite = 0
        self.overflow = 0
        self.lui = 0

        # dict for output signals
        self.signals = {'regDst': 0, 'jump': 0, 'beq': 0, 'bne': 0, 'memRead': 0, 'memToReg': 0, 'aluOp': 'xx', 'memWrite': 0, 'aluSrc': 'xx', 'regWrite': 0, 'overflow': 0, 'lui': 0}
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert (len(inputSources) == 1), 'Controls has one input'
        assert (len(outputValueNames) == 0), 'Random control does not have output'
        assert (len(control) == 0), 'Random control does not have any control signals'
        assert (len(outputSignalNames) == 12), 'Controls has nine control outputs'

        self.inputName = inputSources[0][1]

    def writeOutput(self):
        pass

    def setControlSignals(self):
        self.instruction = self.inputValues[self.inputName]
        # R-type:
        if self.instruction[0:6] == '000000':
            self.regDst = 1
            self.jump = 0
            self.beq = 0
            self.bne = 0
            self.memRead = 0
            self.memToReg = 0
            self.aluOp = '10'
            self.memWrite = 0
            self.aluSrc = 0
            self.regWrite = 1
            self.overflow = 0  # Changes to 1 for the appropriate funct in ALUControl
            self.lui = 0

        # j:
        if self.instruction[0:6] == '000010':
            self.regDst = 0
            self.jump = 1
            self.beq = 0
            self.bne = 0
            self.memRead = 0
            self.memToReg = 0
            self.aluOp = '11'
            self.memWrite = 0
            self.aluSrc = 0
            self.regWrite = 0
            self.overflow = 0
            self.lui = 0

        # beq:
        elif self.instruction[0:6] == '000100':
            self.regDst = 0
            self.jump = 0
            self.beq = 1
            self.bne = 0
            self.memRead = 0
            self.memToReg = 0
            self.aluOp = '01'
            self.memWrite = 0
            self.aluSrc = 0
            self.regWrite = 0
            self.overflow = 0
            self.lui = 0

        # bne:
        elif self.instruction[0:6] == '000101':
            self.regDst = 0
            self.jump = 0
            self.beq = 0
            self.bne = 1
            self.memRead = 0
            self.memToReg = 0
            self.aluOp = '01'
            self.memWrite = 0
            self.aluSrc = 0
            self.regWrite = 0
            self.overflow = 0
            self.lui = 0

        # lui:
        elif self.instruction[0:6] == '001111':
            self.regDst = 0
            self.jump = 0
            self.beq = 0
            self.bne = 0
            self.memRead = 0
            self.memToReg = 0
            self.aluOp = '00'
            self.memWrite = 0
            self.aluSrc = 1
            self.regWrite = 1
            self.overflow = 0
            self.lui = 1

        # slt:
        elif self.instruction[0:6] == '101010':
            self.regDst = 1
            self.jump = 0
            self.beq = 0
            self.bne = 0
            self.memRead = 0
            self.memToReg = 0
            self.aluOp = '11'
            self.memWrite = 0
            self.aluSrc = 0
            self.regWrite = 1
            self.overflow = 0
            self.lui = 0

        # lw:
        elif self.instruction[0:6] == '100011':
            self.regDst = 0
            self.jump = 0
            self.beq = 0
            self.bne = 0
            self.memRead = 1
            self.memToReg = 1
            self.aluOp = '00'
            self.memWrite = 0
            self.aluSrc = 1
            self.regWrite = 1
            self.overflow = 0
            self.lui = 0

        # sw:
        elif self.instruction[0:6] == '101011':
            self.regDst = 0
            self.jump = 0
            self.beq = 0
            self.bne = 0
            self.memRead = 0
            self.memToReg = 0
            self.aluOp = '00'
            self.memWrite = 1
            self.aluSrc = 1
            self.regWrite = 0
            self.overflow = 0
            self.lui = 0

        # addi:
        elif self.instruction[0:6] == '001000':
            self.regDst = 0
            self.jump = 0
            self.beq = 0
            self.bne = 0
            self.memRead = 0
            self.memToReg = 0
            self.aluOp = '00'  # TODO: find out what to do
            self.memWrite = 0
            self.aluSrc = 1
            self.regWrite = 1
            self.overflow = 1
            self.lui = 0

        # addiu:
        elif self.instruction[0:6] == '001001':
            self.regDst = 0
            self.jump = 0
            self.beq = 0
            self.bne = 0
            self.memRead = 0
            self.memToReg = 0
            self.aluOp = '00'  # TODO: find out what to do
            self.memWrite = 0
            self.aluSrc = 1
            self.regWrite = 1
            self.overflow = 0
            self.lui = 0

        # TODO: Missing add

        # break:
        elif self.instruction[0:6] == '001101':
            self.regDst = 0
            self.jump = 0
            self.beq = 0
            self.bne = 0
            self.memRead = 0
            self.memToReg = 0
            self.aluOp = 0
            self.memWrite = 0
            self.aluSrc = 0
            self.regWrite = 0
            self.overflow = 0
            self.lui = 0


        for signalnames in self.outputControlSignals:
            if signalnames == 'regDst':
                self.outputControlSignals[signalnames] = self.regDst
            elif signalnames == 'jump':
                self.outputControlSignals[signalnames] = self.jump
            elif signalnames == 'beq':
                self.outputControlSignals[signalnames] = self.beq
            elif signalnames == 'bne':
                self.outputControlSignals[signalnames] = self.bne
            elif signalnames == 'memRead':
                self.outputControlSignals[signalnames] = self.memRead
            elif signalnames == 'memToReg':
                self.outputControlSignals[signalnames] = self.memToReg
            elif signalnames == 'aluOp':
                self.outputControlSignals[signalnames] = self.aluOp
            elif signalnames == 'memWrite':
                self.outputControlSignals[signalnames] = self.memWrite
            elif signalnames == 'aluSrc':
                self.outputControlSignals[signalnames] = self.aluSrc
            elif signalnames == 'regWrite':
                self.outputControlSignals[signalnames] = self.regWrite
            elif signalnames == 'overflow':
                self.outputControlSignals[signalnames] = self.overflow
            elif signalnames == 'lui':
                self.outputControlSignals[signalnames] = self.lui

