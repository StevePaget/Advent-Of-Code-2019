
def loadfile(fname):
    f=open(fname,"r")
    out=[]
    for line in f:
        out.append(line.strip(""))
    return out


def getfuel(mass):
    if mass<9:
        return 0
    thisFuel = mass//3-2
    return thisFuel + getfuel(thisFuel)

masses = loadfile("1.txt")
sum = 0
for mass in masses:
    sum += getfuel(int(mass))

print(sum)
