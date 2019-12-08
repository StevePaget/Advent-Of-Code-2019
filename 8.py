def load(fname):
    f = open(fname, "r")
    out = []
    for line in f:
        out.append(line.strip())
    return out[0]


data = load("8.txt")
w = 25
h = 6
layers = [data[start: start+(w*h)] for start in range(0,len(data),(w*h))] #split into layers
layers = [[int(d) for d in l] for l in layers] # turn into integers


def part1():
    zeroes = [l.count(0) for l in layers]
    print(zeroes.index(min(zeroes))) # find out which layer has the least zeroes
    print(layers[8].count(1) * layers[8].count(2)) # do the calculation in the puzzle


def part2(w,h,numLayers):
    finalimage = ["_" for c in range(w*h)]
    for layerIndex in range(numLayers-1,-1, -1):  # go from bottom up
        for c in range(w*h):
            if layers[layerIndex][c] == 0:  # only update the final image if it's not transparent (2)
                finalimage[c] = " "
            elif layers[layerIndex][c] == 1:
                finalimage[c] = "*"
    for r in range(h):
        print("".join(finalimage[r*w:r*w+w])) # print out

part2(w,h, len(layers))