from collections import defaultdict

class Processor():
    def __init__(self, basememory):
        self.memory = defaultdict(int)
        for pos in range(len(basememory)):
            self.memory[pos] = basememory[pos]
        self.rba = 0
        self.opcode = 0
        self.pos = 0
        self.runState = 0

    def parsemodes(self, modes):
        return modes.rjust(3, "0")

    def getPara(self, modes, shift, modeIndex):
        if modes[modeIndex] == "0":
            return self.memory[self.pos+shift]
        elif modes[modeIndex] == "2":
            return self.rba + self.memory[self.pos+shift]
        else:
            return self.pos+shift

    def add(self, modes):
        p1 = self.getPara(modes, 1, -1)
        p2 = self.getPara(modes, 2, -2)
        p3 = self.getPara(modes, 3, -3)
        self.memory[p3] = self.memory[p1] + self.memory[p2]

    def mul(self, modes):
        p1 = self.getPara(modes, 1, -1)
        p2 = self.getPara(modes, 2, -2)
        p3 = self.getPara(modes, 3, -3)
        self.memory[p3] = self.memory[p1] * self.memory[p2]

    def sto(self, modes):
        if len(self.inputs) == 0:
            # wait for input
            self.runState = 2
            return False
        p1 = self.getPara(modes, 1, -1)
        thisInput = self.inputs.pop(0)
        self.memory[p1] = thisInput
        return True

    def out(self, modes):
        data = self.getPara(modes, 1, -1)
        print(self.memory[data])
        return self.memory[data]

    def processCommand(self):
        inst = self.memory[self.pos]
        opcode = str(inst)[-2:].rjust(2, "0")
        modes = self.parsemodes(str(inst)[:-2])
        # print(inst, modes)
        if opcode == "01":
            self.add(modes)
            self.pos +=4
            return None
        if opcode == "02":
            self.mul(modes)
            self.pos += 4
            return None
        if opcode == "03":
            success = self.sto(modes)
            if success:
                self.pos += 2
            return None
        if opcode == "04":
            output = self.out(modes)
            self.pos += 2
            return output
        if opcode == "05":
            self.pos = self.jit(modes)
            return None
        if opcode == "06":
            self.pos = self.jif(modes)
            return None
        if opcode == "07":
            self.lth(modes)
            self.pos +=4
            return None
        if opcode == "08":
            self.equ(modes)
            self.pos +=4
            return None
        if opcode == "09":
            self.arb(modes)
            self.pos +=2
            return None

    def run(self, inputs):
        self.inputs = inputs
        self.runState = 1
        output = None
        while self.runState == 1 and self.pos < len(self.memory) - 2 and self.memory[self.pos] != 99:
            o = self.processCommand()
            if o is not None:
                output = o
        if self.memory[self.pos] == 99:
            self.runState = 0
        return output

    def jit(self, modes):
        p1 = self.getPara(modes, 1, -1)
        p2 = self.getPara(modes, 2, -2)
        if self.memory[p1] != 0:
            return self.memory[p2]
        return self.pos + 3

    def jif(self, modes):
        p1 = self.getPara(modes, 1, -1)
        p2 = self.getPara(modes, 2, -2)
        if self.memory[p1] == 0:
            return self.memory[p2]
        return self.pos + 3

    def lth(self, modes):
        p1 = self.getPara(modes, 1, -1)
        p2 = self.getPara(modes, 2, -2)
        p3 = self.getPara(modes, 3, -3)
        if self.memory[p1] < self.memory[p2]:
            self.memory[p3] = 1
        else:
            self.memory[p3] = 0

    def equ(self, modes):
        p1 = self.getPara(modes, 1, -1)
        p2 = self.getPara(modes, 2, -2)
        p3 = self.getPara(modes, 3, -3)
        if self.memory[p1] == self.memory[p2]:
            self.memory[p3] = 1
        else:
            self.memory[p3] = 0

    def arb(self, modes):
        p1 = self.getPara(modes, 1,-1)
        self.rba += self.memory[p1]
