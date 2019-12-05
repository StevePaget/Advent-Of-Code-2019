def load(fname):
    f = open(fname, "r")
    out = []
    for line in f:
        out.append(line.strip())
    return out[0]


class Processor():
    def __init__(self, basememory, inputs):
        self.memory = basememory[:]
        self.reg1 = 0
        self.opcode = 0
        self.inputs = [int(i) for i in inputs.split(",")]
        
    def parsemodes(self, modes):
        return modes.rjust(3,"0")

    def getData(self, modes, para, modeIndex):
        if modes[modeIndex] =="0":
            return self.memory[para]
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
        thisInput = self.inputs[0]
        self.memory[target] = thisInput

    def out(self, modes, para1):
        data = self.getData(modes, para1, -1)
        print(data)

    def processCommand(self, pos):
        #print("position:", pos)
        inst = self.memory[pos]
        opcode = str(inst)[-2:].rjust(2,"0")
        modes = self.parsemodes(str(inst)[:-2])
        #print(inst, modes)
        if opcode == "01":
            self.add(modes, self.memory[pos+1], self.memory[pos+2], self.memory[pos+3])
            return pos + 4
        if opcode == "02":
            self.mul(modes, self.memory[pos+1], self.memory[pos+2], self.memory[pos+3])
            return pos + 4
        if opcode == "03":
            self.sto(modes, self.memory[pos+1])
            return pos + 2
        if opcode == "04":
            self.out(modes, self.memory[pos+1])
            return pos + 2
        if opcode == "05":
            newpos = self.jit(modes, pos, self.memory[pos+1], self.memory[pos+2])
            return newpos
        if opcode == "06":
            newpos = self.jif(modes, pos, self.memory[pos+1], self.memory[pos+2])
            return newpos
        if opcode == "07":
            self.lth(modes, self.memory[pos+1], self.memory[pos+2], self.memory[pos+3])
            return pos + 4
        if opcode == "08":
            self.equ(modes, self.memory[pos+1], self.memory[pos+2], self.memory[pos+3])
            return pos + 4

    def run(self):
        pos = 0
        while pos < len(self.memory) - 2 and self.memory[pos] != 99:
            pos = self.processCommand(pos)

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


basememory = [int(val) for val in load("5.txt").split(",")]
newProc = Processor(basememory, "5")
newProc.run()
