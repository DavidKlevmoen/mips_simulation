from cpuElement import CPUElement

class ShiftLeft16(CPUElement):
    def __init__(self):
        pass

    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 1), 'ShiftLeft16 should have one input'
        assert(len(outputValueNames) == 1), 'ShiftLeft16 has only one output'
        assert(len(control) == 1), 'ShiftLeft16 should only have one control signal: lui'
        assert(len(outputSignalNames) == 0), 'ShiftLeft16 should not have any control output'

        self.inputName = inputSources[0][1]
        self.controlName = control[0][1]
        self.outputName = outputValueNames[0]

    def writeOutput(self):
        if self.controlSignals[self.controlName] == 1:  # if lui == 1, load upper immediate
            self.input = self.inputValues[self.inputName] + '0' * 16
            self.outputValues[self.outputName] = self.input[16:]
        else:
            self.outputValues[self.outputName] = self.inputValues[self.inputName]
