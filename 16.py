import math

def load(fname):
    f = open(fname, "r")
    out = []
    for line in f:
        out.append(line.strip())
    return out[0]

inp = load("16.txt") * 10000
inplist = [int(c) for c in inp[5970837:]]
base = [0,1,0,-1]


def phase(inplist, repeats):
    out = inplist[:]
    pattern = []
    while len(pattern)<len(inplist)+1:
        for basedigit in base:
            for i in range(repeats):
                pattern.append(basedigit)
    pattern = pattern[1:]
    for index in range(len(inplist)):
        out[index] *= pattern[index]
    return abs(sum(out))%10


def part1():
    thisString = inplist[:]
    for phases in range(100):
        newstring = []
        for i in range(1,len(thisString)+1):
            newstring.append(phase(thisString,i))
        print(newstring[:])
        thisString = newstring[:]


for phaseno in range(100):
    print(phaseno)
    for pos in range(len(inplist)-2, -1, -1):
        inplist[pos] = (inplist[pos]+inplist[pos+1])%10
print(inplist[:8])