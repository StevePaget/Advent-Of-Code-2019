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

cX, cY = 0, 0  # start in the middle
mapp = {} # a dict will provide our lookup structure to see if we have visited a square already
updateMap(cX, cY, 1)  # the two functions, updateMap and readMap provide our abstraction, to save time converting the
# x and y coordinates into strings so they can be used as keys for the dict

stack = []  # we are using a stack to provide our "breadcrumbs", so we can backtrack when we reach a dead end.
# The stack will contain the direction number needed (1-4) to get back to the previous position

drawEllipse(400 + cX * 15, 400 + cY * 15, 15, 15, "green")  # draw our starting position

while True:
    backTrack = True        # We will keep ploughing on in a depth-first search unless we meet a dead end
    #                         and have to backtrack. For now, let's assume we're all OK

    for d in range(1,5):    # take each direction from our current position
        newx, newy = getLoc(cX, cY, d)  # work out where this direction takes us
        if readMap(newx, newy) is False:  # if we have never been there before
            result = proc.run([d])[0]  # call the Intcode program to get the contents of this square
            updateMap(newx, newy, result)  # store the value in our local copy of the map
            if result == 0:  # if it a wall
                drawEllipse(400 + newx * 15, 400 + newy * 15, 15, 15, "red")  # draw a red circle and ignore
                #                                                               The program will have automatically
                #                                                               stepped back, so we just try another
                #                                                               direction
            else:
                if result == 2:  # if we have found the target square
                    drawEllipse(400 + newx * 15, 400 + newy * 15, 15, 15, "blue")  # draw it blue
                    o2x, o2y = newx, newy  # store the location for the next part
                    print(len(stack))  # print out the length of the stack. This is the length of the journey here and
                    #                    is the answer to part 1
                else:
                    drawEllipse(400 + newx * 15, 400 + newy * 15, 15, 15, "white") # it's a corridor
                cX, cY = newx, newy # we have found a corridor, so we will move there straight away.
                # cX, cY is our current position
                stack.insert(0,reverse(d))  # Put the reverse direction into our stack, so we can backtrack later
                backTrack = False  # but not right now. We're moving on!
                break  # We're not even going to look in the other directions yet. We'll do that when we backtrack
    if backTrack:  # If we never found an unvisited corridor, we're at a dead end so...
        if len(stack) == 0:  # If there's nothing left in the stack, it means we have already backtracked through
            #                  The entire map to the beginning again
            break            # So quit here
        d = stack.pop(0)     # otherwise, we need to backtrack, so pop off the most recent "breadcrumb"
        proc.run([d])        # feed it into the robot, so it moves
        cX, cY = getLoc(cX, cY,d)  # and this is our new location

# Now produce oxygen map
# This time, we're doing a breadth first search. We will use this list as a queue, but we'll clear it after each layer
# So we can count the layers that were added
nextLayer = [[o2x,o2y]]  # we start wherever the oxygen unit was found before
time = 0
visited = []  # This helps us keep track of places we have been
while True:
    current = deepcopy(nextLayer)  # a deepcopy will copy the 2-dimensional array. Shallow copies won't do this
    #                                The current layer contains all the places we need to go in this iteration
    added = False   # Have we added anything in this layer? We'll check this at the end
    nextLayer = []  # This will hold the next iteration's list of loactions
    for pos in current:
        visited.append(pos)  # Add it to the list, so we don't go there twice
        for d in range(1,5):  # for each direction
            testx, testy = getLoc(pos[0], pos[1], d)  # work out the location in this direction
            if [testx, testy] not in visited:  # if we haven't been there before
                if readMap(testx, testy) != 0:  # and it's not a wall
                    nextLayer.append([testx, testy])  # add it to the queue to be visited in the next iteration
                    drawEllipse(400 + testx * 15, 400 + testy * 15, 15, 15, "blue")
                    added = True  # We've added a layer, so don't quit yet
    if added:
        time+=1  # Tick!
        changeLabel(outLabel, f"time taken: {time}")
    else:
        print(time)  # If we haven't added anything, we're done!
        break






endWait()