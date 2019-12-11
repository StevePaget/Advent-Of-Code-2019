import math
from collections import defaultdict

class Asteroid():
    def __init__(self, x,y, ID):
        self.x = x
        self.y = y
        self.ID = ID
        self.targetlists = defaultdict(list)

    def getAngle(self, x,y):
        angle = ((math.atan2((y-self.y), (x-self.x)) *180 / math.pi)+90)
        # this is a bit messy. I'm sure there's a better way to do it!
        # using atan2 ensures that we can distinguish between all the different directions
        # I'm using degrees instead of radians for no good reason

        if angle < 0:
            angle += 360  # ugh. This is such a kludge. I was in a hurry.
            # Any negative angles represent the final quadrant of the circle, so they belong in the 270-360 region
        return angle

    def countAngles(self, alist):
        angles = set()
        for a in alist: # for each asteroid in the list
            if a is not self:
                angles.add(self.getAngle(a.x, a.y))
                # calculate the angle pointing to this asteroid and put it in a set
                # sets can only store each unique value once, so any duplicates are ignores
        return len(angles)

    def getTargets(self, alist):
        for a in alist:
            if a is not self:
                self.targetlists[self.getAngle(a.x, a.y)].append(a)
        # now sort them according to their distance, so we can eliminate the nearest ones first
        for angle in self.targetlists:
            self.targetlists[angle].sort(key=lambda x: x.getDist(self))

    def getDist(self, otherA):
        return abs(self.x-otherA.x) + abs(self.y - otherA.y)  # Manhattan Distance is fine
    
    def blast(self):
        num = 0
        keys = self.targetlists.keys()
        for key in sorted(keys):
            # We start pointing upwards (angle = 0)
            # We then move through each of the angles for which we have identified one or more asteroids along the line
            # the targetlists are all sorted into distance order
            if len(self.targetlists[key]) >0:  # if there's at least one asteroid left in this direction...
                a = self.targetlists[key].pop(0)  # we will remove it from the list
                num += 1                            # count it
                # print(key, num)                   # print it for diagnostic reasons
                if num == 200:                      # and if this is the 200th one, highlight that fact
                    print("Two Hundredth asteroid destroyed: ", a.x, a.y)
        # I was expecting to have to make more than one 360-degree sweep before I had cleared 200 asteroids
        # In fact, I was done part-way through my first sweep so I didn't have to repeat the process
        # I don't know if this is the same for all inputs, however. YMMV


def load(fname):
    f = open(fname, "r")
    out = []
    for line in f:
        out.append(line.strip())
    return out


astring = load("10.txt")

asteroids = []
ID = 0
for row in range(len(astring)):
    for col in range(len(astring[row])):
        if astring[row][col] == "#":
            asteroids.append(Asteroid(col, row, ID))
            ID +=1


def part1():
    maxDestroyed = 0
    best = None
    for a in asteroids:
        c = a.countAngles(asteroids)
        if c > maxDestroyed:
            maxDestroyed = c
            best = [a.ID, a.x, a.y]
    print(f"Most asteroids is {maxDestroyed}, as seen from asteroid {best}")
    return best


def part2(best):
    asteroids[best].getTargets(asteroids)
    asteroids[best].blast()


best = part1()  # We need to know which Asteroid is the best one, so that part2 can focus getting that one to run the
#                 blast function
part2(best[0])
