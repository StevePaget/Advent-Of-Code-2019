class Processor():
    def __init__(self, basememory):
        self.memory = basememory[:]
        self.rba = 0
        self.opcode = 0
        self.pos = 0
        self.runState = 0
        
    def parsemodes(self, modes):
        return modes.rjust(3,"0")

    def getData(self, modes, para, modeIndex):
        if modes[modeIndex] =="0":
            return self.memory[para]
        elif modes[modeIndex] == "2":
            return self.memory[self.rba + para]
        else:
            return para

    def add(self, modes, para1, para2, para3):
        data1 = self.getData(modes, para1, -1)
        data2 = self.getData(modes, para2, -2)
        self.memory[para3] = data1 + data2

    def mul(self, modes,  para1, para2, para3):
        data1 = self.getData(modes, para1, -1)
        data2 = self.getData(modes, para2, -2)
        self.memory[para3] = data1 * data2

    def sto(self, modes, target):
        if len(self.inputs) ==0:
            # wait for input
            self.runState = 2
            return False
        thisInput = self.inputs.pop(0)
        self.memory[target] = thisInput
        return True

    def out(self, modes, para1):
        data = self.getData(modes, para1, -1)
        return data

    def processCommand(self, pos):
        #print("position:", pos)
        inst = self.memory[pos]
        opcode = str(inst)[-2:].rjust(2,"0")
        modes = self.parsemodes(str(inst)[:-2])
        #print(inst, modes)
        if opcode == "01":
            self.add(modes, self.memory[pos+1], self.memory[pos+2], self.memory[pos+3])
            return pos + 4, None
        if opcode == "02":
            self.mul(modes, self.memory[pos+1], self.memory[pos+2], self.memory[pos+3])
            return pos + 4, None
        if opcode == "03":
            success = self.sto(modes, self.memory[pos+1])
            if success:
                return pos+2, None
            return pos, None
        if opcode == "04":
            output = self.out(modes, self.memory[pos+1])
            return pos + 2, output
        if opcode == "05":
            newpos = self.jit(modes, pos, self.memory[pos+1], self.memory[pos+2])
            return newpos, None
        if opcode == "06":
            newpos = self.jif(modes, pos, self.memory[pos+1], self.memory[pos+2])
            return newpos, None
        if opcode == "07":
            self.lth(modes, self.memory[pos+1], self.memory[pos+2], self.memory[pos+3])
            return pos + 4, None
        if opcode == "08":
            self.equ(modes, self.memory[pos+1], self.memory[pos+2], self.memory[pos+3])
            return pos + 4, None
        if opcode == "09":
            self.arb(modes, self.memory[pos+1])
            return pos + 2, None

    def run(self, inputs):
        self.inputs = inputs
        self.runState = 1
        output = None
        while self.runState==1 and self.pos < len(self.memory) - 2 and self.memory[self.pos] != 99:
            self.pos, o = self.processCommand(self.pos)
            if o is not None:
                output = o
        if self.memory[self.pos] == 99:
            self.runState=0
        return output

    def jit(self, modes, pos, param, param1):
        data1 = self.getData(modes, param, -1)
        data2 = self.getData(modes, param1, -2)
        if data1 != 0:
            return data2
        return pos+3

    def jif(self, modes, pos, param, param1):
        data1 = self.getData(modes, param, -1)
        data2 = self.getData(modes, param1, -2)
        if data1 == 0:
            return data2
        return pos+3

    def lth(self, modes, param, param1, param2):
        data1 = self.getData(modes, param, -1)
        data2 = self.getData(modes, param1, -2)
        if data1 < data2:
            self.memory[param2] = 1
        else:
            self.memory[param2] = 0

    def equ(self, modes, param, param1, param2):
        data1 = self.getData(modes, param, -1)
        data2 = self.getData(modes, param1, -2)
        if data1 == data2:
            self.memory[param2] = 1
        else:
            self.memory[param2] = 0
