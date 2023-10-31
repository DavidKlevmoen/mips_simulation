'''
Code written for inf-2200, University of Tromso
'''

from cpuElement import CPUElement
import random

class RandomControl(CPUElement):
    '''
    Random control unit. It randomly sets it's output signal
    '''
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)
        
        assert(len(inputSources) == 0), 'Random control does not have any inputs'
        assert(len(outputValueNames) == 0), 'Random control does not have output'        
        assert(len(control) == 0), 'Random control does not have any control signals'
        assert(len(outputSignalNames) == 1), 'Random control has one control output'
        
        self.inputSource = inputSources[0][1]
        self.signalName = outputSignalNames[0]
    
    def writeOutput(self):
        pass # randomControl has no data output
    
    def setControlSignals(self):
        self.outputControlSignals[self.signalName] = random.randint(0, 1)


'''
Control signals:
'''
# opcode:
r_type = '000000'  # r-type
j = '000010'  # jump
beq = '000100'  # branch if equal
bne = '000101'  # branch if not equal
lui = '001111'  # load upper immediate
slt = '101010'  # set less than
lw = '100011'  # load word
sw = '101011'  # store word
addi = '001000'  # add immediate
addiu = '001001'  # add immediate unsigned

# control
regDst = '000'  # register destination
jump = '001'  # jump
branch = '010'  # branch
memRead = '011'  # memory read
memToReg = '100'  # memory to register
aluOp = '101'  # alu operation
memWrite = '110'  # memory write
aluSrc = '111'  # alu source

# R-type:
'''
    add = '000000'  # add
    addu = '000000'  # add unsigned
    sub = '000000'  # subtract
    subu = '000000'  # subtract unsigned
    and_ = '000000'  # and
    or_ = '000000'  # or
    nor = '000000'  # nor
    break_ = '000000'  # break
'''


funct = {'100000': 'add', '100001': 'addu', '100010': 'sub', '100011': 'subu', '100100': 'and', '100101': 'or', '100111': 'nor', '101010': 'slt'}
# add = '100000'
# sub = '100010'
# and_ = '100100'
# or_ = '100101'
# slt = '101010'
