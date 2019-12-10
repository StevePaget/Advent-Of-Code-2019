import math
from collections import defaultdict

class Asteroid():
    def __init__(self, x,y, ID):
        self.x = x
        self.y = y
        self.ID = ID
        self.targetlists = defaultdict(list)

    def getSlope(self, x,y):
        return math.atan2((self.y-y), (self.x-x)) *180 / math.pi

    def countSlopes(self, alist):
        slopes = set()
        for a in alist:
            if a is not self:
                slopes.add(self.getSlope(a.x, a.y))
        return len(slopes)

    def getTargets(self, alist):
        for a in alist:
            if a is not self:
                self.targetlists[self.getSlope(a.x, a.y)].append(a)
        # now sort them
        for angle in self.targetlists:
            self.targetlists[angle].sort(key=lambda x: x.getDist(self))
        print()



    def getDist(self, otherA):
        return abs(self.x-otherA.x) + abs(self.y - otherA.y)

def load(fname):
    f = open(fname, "r")
    out = []
    for line in f:
        out.append(line.strip())
    return out

file=""".#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##"""

astring = load("10.txt")

asteroids = []
ID = 0
for row in range(len(astring)):
    for col in range(len(astring[row])):
        if astring[row][col] == "#":
            asteroids.append(Asteroid(col, row, ID))
            ID +=1


def part1():
    max = 0
    best = None
    for a in asteroids:
        c = a.countSlopes(asteroids)
        if c > max:
            max = c
            best = [a.ID, a.x, a.y]
    print(max, best)

def part2():
    asteroids[210].getTargets(asteroids)

part1()

print(math.atan2(0,5)*180/math.pi)

