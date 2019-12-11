import processor
from collections import defaultdict

def load(fname):
    f = open(fname, "r")
    out = []
    for line in f:
        out.append(line.strip())
    return out[0]


def readWall(wall, pos):
    return wall[(pos[0],pos[1])]

def paintWall(wall, pos, colour):
    wall[(pos[0],pos[1])] = colour

def printWall(wall):
    # this is cheaty. Rather than calculate the top, bottom, left and right limits of the painting, I just examined the
    # wall data and chose appropriate values to capture the relevant area
    for row in range(0,10):
        for col in range(0,42):
            if wall[(col,row)] == 1:
                print("#",end="")
            else:
                print(" ",end="")
        print()

program = [int(s) for s in load("11.txt").split(",")]


def part1():
    proc = processor.Processor(program)
    wall = defaultdict(int)
    # we use a defaultdict rather than a list because we don't know which direction the painting robot is going to move.
    # If it moves left (or up) from the starting position, the coordinates will be negative.
    # If we tried to use these as an index of a list (or array) it would fail
    # The benefit of a defaultdict is that if we try to access a coordinate that has not been set up previously, the
    # program won't crash. It will just create the new item with a default value of 0

    painted = set()  # This will be a list of (unique) panels that have been painted
    currentPos = [0, 0] # we could start anywhere. 0,0 is arbitrary
    directions = ([0, -1], [1, 0], [0, 1], [-1, 0]) # These represent x,y coordinate changes for Up, Right, Down, Left
    direction = 0  # we start facing up (the first of the directions in the list on the previous line)

    paintWall(wall, currentPos, 0)  # paint the current panel black
    while True:  # keep going as long as the processor has not finished its program
        o = proc.run([readWall(wall, currentPos)])  # run the processor with the input of the current panel

        paintWall(wall, currentPos, o[0])
        # o is the output, which will contain two values: The colour to paint and the direction to turn

        painted.add(str(currentPos[0]) + ":" + str(currentPos[1]))
        # add this panel coordinate to a set, so we can count the painted panels

        if o[1] == 0:  # 0 means turn left, which means shifting one direction down in the directions list
            o[1]= -1   # But since adding zero to our direction would not do anything, we really want -1

        direction = (direction+o[1]) % 4  # move either up or down the directions list
        currentPos[0] += directions[direction][0]  # use the coordinate changes to affect the current position
        currentPos[1] += directions[direction][1]
        if proc.runState == 0:  # the runstate of the processor is zero when it halts
            break
    print(len(painted))

def part2():
    proc = processor.Processor(program)
    wall = defaultdict(int)
    currentPos = [0, 0]
    directions = ([0, -1], [1, 0], [0, 1], [-1, 0])
    direction = 0
    paintWall(wall, currentPos, 1)  # the only real difference is that we paint the starting panel white
    while True:
        o = proc.run([readWall(wall, currentPos)])
        paintWall(wall, currentPos, o[0])
        if o[1] == 0:
            o[1]= -1
        direction = (direction+o[1])%4
        currentPos[0] += directions[direction][0]
        currentPos[1] += directions[direction][1]
        if proc.runState==0:
            break
    printWall(wall) # and we paint the wall at the end


part1()
part2()