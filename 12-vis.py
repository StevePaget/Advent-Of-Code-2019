from pygame_functions import *
import math


# Instructions:
# To view this visualisation, you need Pygame installed
# and have a copy of my library pygame_functions.
# This is provided in the git repository.

# Press Space to pause the orbits at any time
# then use cursor keys to rotate the universe!
# Press G to Go again

# Note: The rotating does not update the velocities,
# So it will no longer provide valid solutions for the
# Advent of Code puzzle


screenSize(900,900)
setAutoUpdate(False)


class Body():
    def __init__(self,x,y,z, colour):
        self.positions = [x,y,z]
        self.vels = [0,0,0]
        self.colour = colour
    
    def getEnergy(self):
        pot = 0
        for dimension in range(3):
            pot += abs(self.positions[dimension])  # add all the absolute values of the positions
        kin = 0
        for dimension in range(3):
            kin += abs(self.vels[dimension])    # add all the absolute values of the velocities
        return pot*kin  # multiply
                   
    def drawMe(self):
        centre = 450
        factor = 3
        drawEllipse(centre + self.x2D()*factor, centre + self.y2D()*factor, max([20+self.positions[2],5]), max([20+self.positions[2],5]), self.colour)

    def applyGravity(self, bodies):
        # this applies the gravity as described in the challenge. Greater gives +1, Less than gives -1
        # Each dimensions is handled independently
        for body in bodies:
            if body is not self:
                for dimension in range(3):
                    if body.positions[dimension] > self.positions[dimension]:
                        self.vels[dimension] +=1
                    elif body.positions[dimension] < self.positions[dimension]:
                        self.vels[dimension] -=1


    def applyVelocity(self):
        # Just adding the velocities to the positions
        for dimension in range(3):
            self.positions[dimension] += self.vels[dimension]


    def x2D(self):
        x = int(self.positions[0] + (self.positions[0] * self.positions[2]/400))
        return x

    def y2D(self):
        y = int(self.positions[1] + (self.positions[1] * self.positions[2]/400))
        return y

    def RotateX(self, dist):
        rad = dist * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        newy = self.positions[1] * cosa - self.positions[2] * sina
        newz = self.positions[1] * sina + self.positions[2] * cosa
        self.positions[2] = newz
        self.positions[1] = newy

    def RotateY(self, dist):
        rad = dist / 2 * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        newz = self.positions[2] * cosa - self.positions[0] * sina
        newx = self.positions[2] * sina + self.positions[0] * cosa
        self.positions[2] = newz
        self.positions[0] = newx

def drawWorld(bodies):
    clearShapes()
    # sort the bodies into distances
    bodies.sort(key=lambda b: b.positions[2])
    for b in bodies:
        b.drawMe()
    updateShapes()

def hashit(bodies, states, step, done):
    # when trying to identify whether a particular position has ever appeared before, it would be very slow to put them
    # in a list and try to search it.
    # Using a dictionary lets us produce a hash value for a position, which gives us a very quick lookup
    # (it should have a time complexity of O(1)  )

    stateStrings = ["","",""]  # These will be used to hold strings which represent a state.
    #                            One string will be used for each dimension (x, y, z)
    for b in bodies:
        for d in range(3):
            #  We add the position and velocity of this body to the string describing the relevant dimension
            stateStrings[d] += f"{b.positions[d]}:{b.vels[d]} "
    # at this point, a single stateString looks something like: "15:0 -5:0 0:0 5:0"
    # representing   "xpos:xvel xpos:xvel xpos:xvel xpos:xvel"  one pair of values for each body's x state

    # it doesn't really matter what this looks like, so long as each state produces a unique string that can be used
    # as a dictionary index. it will be hashed to produce a unique number

    for d in range(3):
        # here we are looking to see if these state strings have ever appeared before
        # we do it one dimension at a time, as they operate independently
        if done[d] is False:
            # The Done array indicates whether we have yet identified the repeat period of each dimension.
            # We only want to report each dimension's period once. Otherwise we'll be overwhelmed with test output.
            if stateStrings[d] in states[d]: # if this state string has already been used as a hash in the dictionary...
                done[d] = True               # mark this dimension as done
                print(f"repeats in dimension {d} after {step - states[d][stateStrings[d]]}")  # report the period
            states[d][stateStrings[d]] = step  # otherwise, store the last time this state was seen for future reference
    return done  # send back the list that indicated which dimensions have been identified already
    
bodiesList = [Body(15,-2,-6, "red"), Body(-5,-4,-11,"white"),Body(0,-6,0,"blue"),Body(5,9,6,"green")]

states = [{}, {}, {}]
done = [False, False, False]

hashit(bodiesList, states, 0, done)
for step in range(1,100000001):
    for b in bodiesList:
        b.applyGravity(bodiesList)
    for b in bodiesList:
        b.applyVelocity()
    done = hashit(bodiesList, states, step, done)
    drawWorld(bodiesList)
    if keyPressed("space"):
        while not keyPressed("g"):
            if keyPressed("right"):
                for b in bodiesList:
                    b.RotateY(3)
            if keyPressed("up"):
                for b in bodiesList:
                    b.RotateX(3)
            if keyPressed("down"):
                for b in bodiesList:
                    b.RotateX(-3)
            if keyPressed("left"):
                for b in bodiesList:
                    b.RotateY(-3)
            drawWorld(bodiesList)
            tick(50)
    tick(10)


totalEnergy = sum([b.getEnergy() for b in bodiesList])
print(totalEnergy)

# Once run, we have three periods (for dimension 0 , 1 and 2)
# The answer is the least common multiple of these
# I was super lazy, so I didn't program this calculation.
# I used the website https://www.calculatorsoup.com/calculators/math/lcm.php instead!


