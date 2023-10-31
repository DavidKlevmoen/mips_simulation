'''
Code written for inf-2200, University of Tromso
'''

from pc import PC
from add import Add
from alu import Alu
from aluControl import AluControl
from mux import Mux, MuxInstr_Reg
from registerFile import RegisterFile
from instructionMemory import InstructionMemory
from dataMemory import DataMemory
from constant import Constant
from convert import *
from common import Break, Overflow
from randomControl import RandomControl
from controls import Controls
from signextender import signExtender
from shiftLeft2 import ShiftLeft2
from shiftLeft16 import ShiftLeft16
from consatenator import Consatenator


class MIPSSimulator():
    '''Main class for MIPS pipeline simulator.

    Provides the main method tick(), which runs pipeline
    for one clock cycle.

    '''

    def __init__(self, memoryFile):
        self.nCycles = 0  # Used to hold number of clock cycles spent executing instructions

        # TODO: finish dataMemory and registerFile
        self.dataMemory = DataMemory(memoryFile)
        self.instructionMemory = InstructionMemory(memoryFile)
        self.registerFile = RegisterFile()

        self.constant3 = Constant(3)
        self.constant4 = Constant(4)
        self.randomControl = RandomControl()

        # TODO: finish controls
        self.controls = Controls()  # our implementation

        # TODO: check if muxes work properly
        self.muxInstr_Reg = MuxInstr_Reg()
        self.muxReg_ALU = Mux()
        self.muxData_Reg = Mux()
        self.muxAdder_PC = Mux()

        self.muxToPc = Mux()

        # TODO: check if signExtend and shiftLeft2 works properly
        self.signExtend = signExtender()
        self.aluControl = AluControl()
        self.alu = Alu()
        self.shiftLeft2 = ShiftLeft2()
        self.shiftLeft2Jump = ShiftLeft2()
        self.shiftLeft16 = ShiftLeft16()
        self.addAdder_Shift = Add()

        self.consatenator = Consatenator()


        self.mux = Mux()
        self.adder = Add()
        self.pc = PC(self.startAddress())

        self.elements = [self.constant4, self.adder, self.instructionMemory, self.controls,
                         self.registerFile, self.signExtend, self.shiftLeft16, self.muxReg_ALU, self.aluControl, self.alu, self.dataMemory,
                         self.muxData_Reg, self.muxInstr_Reg, self.registerFile, self.shiftLeft2, self.shiftLeft2Jump, self.addAdder_Shift, self.muxAdder_PC, self.consatenator, self.muxToPc]

        self._connectCPUElements()

    def _connectCPUElements(self):
        self.constant3.connect(
            [],
            ['constant'],
            [],
            []
        )

        self.constant4.connect(
            [],
            ['constant'],
            [],
            []
        )

        self.adder.connect(
            [(self.pc, 'pcAddress'), (self.constant4, 'constant')],
            ['sum'],
            [],
            []
        )

        '''
        Mux connections
        '''
        self.muxInstr_Reg.connect([(self.instructionMemory, 'instructionOut')],
                                    ['muxInstr_RegOut'],
                                    [(self.controls, 'regDst')],
                                    [])

        self.muxReg_ALU.connect([(self.registerFile, 'readData2'), (self.shiftLeft16, 'shiftLeft16Out')],
                                ['muxReg_ALUOut'],
                                [(self.controls, 'aluSrc')],
                                [])

        self.muxData_Reg.connect([(self.alu, 'aluResult'), (self.dataMemory, 'dataMemoryOut')],
                                    ['muxData_RegOut'],
                                    [(self.controls, 'memToReg')],
                                    [])

        self.muxAdder_PC.connect([(self.adder, 'sum'), (self.addAdder_Shift, 'addAdder_ShiftOut')],
                                    ['muxAdder_PCOut'],
                                    [(self.alu, 'aluZero')],
                                    [])

        self.muxToPc.connect([(self.muxAdder_PC, "muxAdder_PCOut"), (self.consatenator, "newPc")],
                             ["muxToPcOut"],
                             [(self.controls, "jump")],
                             [])

        '''

        self.mux.connect(
            [(self.adder, 'sum'), (self.constant3, 'constant')],
            ['muxOut'],
            [(self.randomControl, 'randomSignal')],
            []
        )
        '''


        self.pc.connect(
            [(self.muxToPc, 'muxToPcOut')],
            ['pcAddress'],
            [],
            []
        )

        '''
            Our implementation
        '''
        self.addAdder_Shift.connect([(self.adder, 'sum'), (self.shiftLeft2, 'shiftLeft2Out')],
                                    ['addAdder_ShiftOut'],
                                    [],
                                    [])

        self.alu.connect([(self.registerFile, 'readData1'), (self.muxReg_ALU, 'muxReg_ALUOut')],
                         ['aluResult'],
                         [(self.aluControl, 'aluControl'), (self.controls, 'beq'), (self.controls, 'bne'), (self.aluControl, 'overflow')],
                         ['aluZero'])

        self.aluControl.connect([(self.instructionMemory, 'instructionOut')],
                                [],
                                [(self.controls, 'aluOp'), (self.controls, 'overflow')],
                                ['aluControl', 'overflow'])

        self.controls.connect([(self.instructionMemory, 'instructionOut')],
                              [],
                              [],
                              ['regDst', 'jump', 'beq', 'bne', 'memRead', 'memToReg', 'aluOp', 'memWrite', 'aluSrc',
                               'regWrite', 'overflow', 'lui'])

        self.dataMemory.connect([(self.alu, 'aluResult'), (self.registerFile, 'readData2')],
                                ['dataMemoryOut'],
                                [(self.controls, 'memRead'), (self.controls, 'memWrite')],
                                [])

        self.instructionMemory.connect([(self.pc, 'pcAddress')],
                                       ['instructionOut'],
                                       [],
                                       [])

        self.registerFile.connect([(self.instructionMemory, 'instructionOut'), (self.muxInstr_Reg, 'muxInstr_RegOut'), (self.muxData_Reg, 'muxData_RegOut')],
                                  ['readData1', 'readData2'],
                                  [(self.controls, 'regWrite')],
                                  [])

        self.shiftLeft2.connect([(self.signExtend, 'signExtended')],
                                ['shiftLeft2Out'],
                                [],
                                [])

        self.shiftLeft16.connect([(self.signExtend, 'signExtended')],
                                ['shiftLeft16Out'],
                                [(self.controls, 'lui')],
                                [])

        self.signExtend.connect([(self.instructionMemory, 'instructionOut')],
                                ['signExtended'],
                                [],
                                [])

        self.shiftLeft2Jump.connect([(self.instructionMemory, "instructionOut")],
                                    ["shiftLeft2JumpOut"],
                                    [],
                                    [])

        self.consatenator.connect([(self.addAdder_Shift, "addAdder_ShiftOut"), (self.shiftLeft2Jump, "shiftLeft2JumpOut")],
                                  ["newPc"],
                                  [],
                                  [])






    def startAddress(self):
        '''
        Returns first instruction from instruction memory
        '''
        return next(iter(sorted(self.instructionMemory.memory.keys())))

    def clockCycles(self):
        '''Returns the number of clock cycles spent executing instructions.'''

        return self.nCycles

    def dataMemory(self):
        '''Returns dictionary, mapping memory addresses to data, holding
        data memory after instructions have finished executing.'''

        return self.dataMemory.memory

    def registerFile(self):
        '''Returns dictionary, mapping register numbers to data, holding
        register file after instructions have finished executing.'''

        return self.registerFile.register

    def printDataMemory(self):
        self.dataMemory.printAll()

    def printRegisterFile(self):
        self.registerFile.printAll()
    def tick(self):
        '''Execute one clock cycle of pipeline.'''
        self.nCycles += 1

        # The following is just a small sample implementation

        self.pc.writeOutput()

        self.pc.debug_print()

        for elem in self.elements:
            elem.readControlSignals()
            elem.readInput()
            elem.writeOutput()
            elem.setControlSignals()

            elem.debug_print()
        self.printRegisterFile()
        self.printDataMemory()
        self.pc.readInput()
        if self.instructionMemory.memory[self.pc.outputValues['pcAddress']] == 13:
            self.nCycles += 1
            Break("Break instruction found")
            # flush memory
            self.pc.memory = {}
            self.instructionMemory.memory = {}
