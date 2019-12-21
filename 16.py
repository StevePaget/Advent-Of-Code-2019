
def load(fname):
    f = open(fname, "r")
    out = []
    for line in f:
        out.append(line.strip())
    return out[0]

inp = "03036732577212944063491565474664"
inp = inp*10000
#inp = load("16.txt")
inplist = [int(c) for c in inp]
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

thisString = inplist[:]
for phases in range(100):
    newstring = []
    for i in range(1,len(thisString)+1):
        newstring.append(phase(thisString,i))
        if i%10000 ==0:
            print(i)
    print(newstring[:])
    thisString = newstring[:]

