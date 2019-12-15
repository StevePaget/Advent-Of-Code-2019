import processor
from pygame_functions import *


def load(fname):
    f = open(fname, "r")
    out = []
    for line in f:
        out.append(line.strip())
    return out[0]


def drawOutput(op,screen):
    #print("\n"*50)
    blocks = 0
    ballpos, batpos =0,0
    graphics = [" ", "#", "H","-", "*"]
    for pos in range(0,len(op),3):
        screen[op[pos+1]][op[pos]] = op[pos+2]
    for r in range(25):
        for c in range(50):
            if screen[r][c] == 2:
                blocks += 1
            elif screen[r][c] == 4:
                ballpos = c
            elif screen[r][c] == 3:
                batpos = c
            #print(graphics[screen[r][c]], end = "")
        #print()
    try:
        print(screen[0][-1])
    finally:
        return ballpos, batpos


screen = {}
for r in range(25):
    screen[r] = {}
    for c in range(50):
        screen[r][c] = 0

program = [int(s) for s in load("13.txt").split(",")]
program[0] = 2
newproc = processor.Processor(program)
inp = 0
while True:
    op = newproc.run([inp])
    ballpos, batpos = drawOutput(op,screen)
    if ballpos>batpos:
        inp=1
    elif ballpos < batpos:
        inp=-1
    else:
        inp=0
    if newproc.runState==0:
        break
