class Thing():
    def __init__(self, name):
        self.name = name
        self.satellites = []
        self.parent = None

    def __str__(self):
        # A print-friendly version of this object
        return self.name

    def makeOrbit(self, sat):
        self.satellites.append(sat)

    def countSats(self, level):
        # A recursive counter. Count this body's satellites, plus all the satellites of its children
        return len(self.satellites)* level + sum([sat.countSats(level+1) for sat in self.satellites])

    def containsSan(self):
        # if SAN is a child of this body, it returns the distance to its main body
        # if not, it returns False
        if self.name == "SAN":
            return -1
        else:
            for sat in self.satellites:
                found = sat.containsSan()  # Recursion FTW
                if found is not False:
                    return found+1
            return False


def load(fname):
    f = open(fname, "r")
    out = []
    for line in f:
        out.append(line.strip())
    return out


orbits = load("6.txt")

things = {}  # A dictionary is a nice fast way of accessing objects by name
for line in orbits:
    names = line.split(")")
    body = names[0]
    sat = names[1]
    if body not in things:
        things[body] = Thing(body) # if it doesn't already exist, let's make it
    if sat not in things:
        things[sat] = Thing(sat) # if it doesn't already exist, let's make it
    things[body].makeOrbit(things[sat])  # add the sat to the main body's child nodes
    things[sat].parent = things[body]  # give the child a reference to its parent, so we can traverse the tree upwards

# part 1
print(things["COM"].countSats(1))

# part 2
current = things["YOU"].parent
steps = 0
while current.containsSan() is False: # it's not on this branch, so let's move up the tree
    current = current.parent
    steps +=1
# At this point, we know that SAN is somewhere on this branch
steps += current.containsSan()
print(steps)