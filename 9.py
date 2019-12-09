from processor import Processor


def load(fname):
    f = open(fname, "r")
    out = []
    for line in f:
        out.append(line.strip())
    return out


progstring = load("9.txt")[0]
#progstring= "1102,34915192,34915192,7,4,7,99,0"
program = [int(inst) for inst in progstring.split(",")]

myProc = Processor(program)

myProc.run([2])
