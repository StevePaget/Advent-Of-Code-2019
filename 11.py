import processor
from collections import defaultdict

def load(fname):
    f = open(fname, "r")
    out = []
    for line in f:
        out.append(line.strip())
    return out[0]



def readWall(pos):
    return wall[(pos[0],pos[1])]

def paintWall(pos, colour):
    wall[(pos[0],pos[1])] = colour

def printWall(wall):
    for row in range(0,10):
        for col in range(-42,42):
            if wall[(col,row)] == 1:
                print("#",end="")
            else:
                print(" ",end="")
        print()

wall = defaultdict(int)
currentPos = [0,0]
directions = ([0,-1], [1,0], [0,1], [-1,0])
direction = 0
topleft=[0,0]
painted=set()
program = [int(s) for s in load("11.txt").split(",")]
proc = processor.Processor(program)
paintWall(currentPos, 1)
while True:
    o = proc.run([readWall(currentPos)])
    paintWall(currentPos, o[0])
    painted.add(str(currentPos[0]) + ":" + str(currentPos[1]))
    if o[1] == 0:
        o[1]= -1
    direction = (direction+o[1])%4
    currentPos[0] += directions[direction][0]
    currentPos[1] += directions[direction][1]
    if proc.runState==0:
        break
print(len(painted))
printWall(wall)