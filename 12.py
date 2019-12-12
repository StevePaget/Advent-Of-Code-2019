class Body():
    def __init__(self,x,y,z):
        self.positions = [x,y,z]
        self.vels = [0,0,0]
    
    def getEnergy(self):
        pot = 0
        for dimension in range(3):
            pot += abs(self.positions[dimension])  # add all the absolute values of the positions
        kin = 0
        for dimension in range(3):
            kin += abs(self.vels[dimension])    # add all the absolute values of the velocities
        return pot*kin  # multiply
                   

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


def hashit(bodies, states, step, done):
    # when trying to identify whether a particular position has ever appeared before, it would be very slow to put them
    # in a list and try to search it.
    # Using a dictionary lets us produce a hash value for a position, which gives us a very quick lookup
    # (it should have a time complexity of O(1)   )

    stateStrings = ["","",""]  # These will be used to hold strings which represent a state.
    #                            One string will be used for each dimension (x, y, z)
    for b in bodies:
        for d in range(3):
            #  We add the position and velocity of this body to the string describing the relevant dimension
            stateStrings[d] += f"{b.positions[d]}:{b.vels[d]} "
    print(stateStrings[0])
    # at this point, a single stateString looks something like: "15:0 -5:0 0:0 5:0"
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
    
bodiesList = [Body(15,-2,-6), Body(-5,-4,-11),Body(0,-6,0),Body(5,9,6)]

states = [{}, {}, {}]
done = [False, False, False]

hashit(bodiesList, states, 0, done)
for step in range(1,100000001):
    for b in bodiesList:
        b.applyGravity(bodiesList)
    for b in bodiesList:
        b.applyVelocity()
    done = hashit(bodiesList, states, step, done)

totalEnergy = sum([b.getEnergy() for b in bodiesList])
print(totalEnergy)

# Once run, we have three periods (for dimension 0 , 1 and 2)
# The answer is the least common multiple of these
# I was super lazy, so I didn't program this calculation.
# I used the website https://www.calculatorsoup.com/calculators/math/lcm.php instead!
