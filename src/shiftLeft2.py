from cpuElement import CPUElement

class ShiftLeft2(CPUElement):
    def __init__(self):
        pass

    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 1), 'ShiftLeft2 should have one input'
        assert(len(outputValueNames) == 1), 'ShiftLeft2 has only one output'
        assert(len(control) == 0), 'ShiftLeft2 should not have any control signal'
        assert(len(outputSignalNames) == 0), 'ShiftLeft2 should not have any control output'

        self.inputName = inputSources[0][1]
        self.outputName = outputValueNames[0]

    def writeOutput(self):
        # uncertain if it returns a 32 bit or 34 bit number
        if type(self.inputValues[self.inputName]) is str:
            self.input = self.inputValues[self.inputName] + '00'
            self.outputValues[self.outputName] = self.input[2:]
