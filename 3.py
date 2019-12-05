import math

def loadfile(fname):
    f=open(fname,"r")
    out=[]
    for line in f:
        out.append(line.strip(""))
    return out


#wires = ["R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51","U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"]
#wires = ["R8,U5,L5,D3","U7,R6,D4,L4"]
wires = loadfile("3.txt")
wires = [wire.split(",") for wire in wires]

shortest = math.inf

wire1 = {"0:0":True}
currentpos = [0,0]
steps = 0
for inst in wires[0]:
    dir = inst[0]
    mag = int(inst[1:])
    if dir == "R":
        y = 0
        x = 1
    if dir == "L":
        y = 0
        x = -1
    if dir == "U":
        y = 1
        x = 0
    if dir == "D":
        y = -1
        x = 0
    for n in range(mag):
        currentpos[0] += x
        currentpos[1] += y
        #print(currentpos)
        steps += 1
        cp = str(currentpos[0]) + ":" + str(currentpos[1])
        try:
            print("crossed again", wire1[cp])
        except:
            wire1[cp] = steps

#print(wire1)

currentpos = [0,0]
steps = 0
for inst in wires[1]:
    dir = inst[0]
    mag = int(inst[1:])
    if dir == "R":
        y = 0
        x = 1
    if dir == "L":
        y = 0
        x = -1
    if dir == "U":
        y = 1
        x = 0
    if dir == "D":
        y = -1
        x = 0
    for n in range(mag):
        currentpos[0] += x
        currentpos[1] += y
        #print(currentpos)
        steps+=1

        try:
            cp = str(currentpos[0]) + ":" + str(currentpos[1])
            total = steps + wire1[cp]
            if total < shortest:
                shortest = total
        except:
            pass

print(f"Shortest {shortest}")

