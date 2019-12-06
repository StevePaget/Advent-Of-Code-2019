class Thing():
    def __init__(self, name):
        self.name = name
        self.satellites = []
        self.parent = None

    def __str__(self):
        return self.name

    def makeOrbit(self, sat):
        self.satellites.append(sat)

    def countSats(self, level):
        return len(self.satellites)* level + sum([sat.countSats(level+1) for sat in self.satellites])

    def containsSan(self):
        if self.name == "SAN":
            return -1
        else:
            for sat in self.satellites:
                found = sat.containsSan()
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

things = {}
for line in orbits:
    names = line.split(")")
    body = names[0]
    sat = names[1]
    try:
        print("orbiting ", things[body], "...")
    except KeyError:
        things[body] = Thing(body)
        print("made", things[body])
    try:
        print("            ... is ", things[sat])
    except KeyError:
        things[sat] = Thing(sat)
        print("made", things[sat])
    things[body].makeOrbit(things[sat])
    things[sat].parent = things[body]

# part 1
print(things["COM"].countSats(1))

# part 2
current = things["YOU"].parent
steps = 0
while current.containsSan() is False:
    current = current.parent
    steps +=1
steps += current.containsSan()
print(steps)