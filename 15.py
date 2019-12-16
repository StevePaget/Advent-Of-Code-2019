import processor
from collections import defaultdict
from pygame_functions import *
from copy import deepcopy

screenSize(800,800)

outLabel = makeLabel("", 18,10,10,"white")
showLabel(outLabel)
def load(fname):
    f = open(fname, "r")
    out = []
    for line in f:
        out.append(line.strip())
    return out[0]

def getLoc(cX, cY, dir):
    movements = [None, [0,-1], [0,1], [-1,0], [1,0]]
    return cX + movements[dir][0], cY + movements[dir][1]

def reverse(dir):
    opposites = [None, 2,1,4,3]
    return opposites[dir]

def updateMap(x,y,value):
    add = f"{x}:{y}"
    mapp[add] = value

def readMap(x,y):
    add = f"{x}:{y}"
    try:
        return mapp[add]
    except KeyError:
        return False

program = [int(i) for i in load("15.txt").split(",")]
proc = processor.Processor(program)

cX, cY = 0, 0
mapp = {}
updateMap(cX, cY, 1)

stack = []
drawEllipse(400 + cX * 15, 400 + cY * 15, 15, 15, "green")
while True:
    backTrack = True
    for d in range(1,5):
        newx, newy = getLoc(cX, cY, d)
        if readMap(newx, newy) is False:
            result = proc.run([d])[0]
            updateMap(newx, newy, result)
            if result == 0:
                drawEllipse(400 + newx * 15, 400 + newy * 15, 15, 15, "red")
            else:
                if result == 2:
                    drawEllipse(400 + newx * 15, 400 + newy * 15, 15, 15, "blue")
                    o2x, o2y = newx, newy
                    print(len(stack))
                else:
                    drawEllipse(400 + newx * 15, 400 + newy * 15, 15, 15, "white")
                cX, cY = newx, newy
                stack.insert(0,reverse(d))
                backTrack = False
                break
    if backTrack:
        if len(stack) == 0:
            break
        d = stack.pop(0)
        proc.run([d])
        cX, cY = getLoc(cX, cY,d)

# Now produce oxygen map
nextLayer = [[o2x,o2y]]
time = 0
visited = []
while True:
    current = deepcopy(nextLayer)
    added = False
    nextLayer = []
    for pos in current:
        visited.append(pos)
        for d in range(1,5):
            testx, testy = getLoc(pos[0], pos[1], d)
            if [testx, testy] not in visited:
                if readMap(testx, testy) != 0:
                    nextLayer.append([testx, testy])
                    drawEllipse(400 + testx * 15, 400 + testy * 15, 15, 15, "blue")
                    added = True
    if added:
        time+=1
        changeLabel(outLabel, f"time taken: {time}")
    else:
        print(time)
        break
    tick(50)






endWait()