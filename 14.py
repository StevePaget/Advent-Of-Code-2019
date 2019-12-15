import math
from collections import defaultdict
from copy import deepcopy


# I started off creating objects for the different products, because I was intending to do a node-based tree traversal.
# In the end this became more trouble that it was worth, as I ended up using dicts and lists for all the useful data
class Product:
    def __init__(self, name):
        self.name = name
        self.needs = []
        self.quantityProduced = 0  # this is how many are made in one batch

    def addNeed(self, item, q):
        self.needs.append([item, q])

    def __str__(self):
        return self.name


def load(fname):
    f = open(fname, "r")
    out = []
    for line in f:
        out.append(line.strip())
    return out


def parse():
    fileList = load("14.txt")
#     fileList = """171 ORE => 8 CNZTR
# 7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
# 114 ORE => 4 BHXH
# 14 VRPVC => 6 BMBT
# 6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
# 6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
# 15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
# 13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
# 5 BMBT => 4 WPTQ
# 189 ORE => 9 KTJDG
# 1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
# 12 VRPVC, 27 CNZTR => 2 XDBXC
# 15 KTJDG, 12 BHXH => 5 XCVML
# 3 BHXH, 2 VRPVC => 7 MZWV
# 121 ORE => 7 VRPVC
# 7 XCVML => 6 RJRHP
# 5 BHXH, 4 VRPVC => 5 LTCX""".split("\n")

    productList = []
    for line in fileList:
        elements = line.split()
        for ei in range(len(elements)):
            if elements[ei][-1] == ",":
                elements[ei] = elements[ei][:-1]
        target = elements[-1]
        targetQuantity = int(elements[-2])
        ingredientsList = []
        for ingredientNo in range(0,len(elements)-3,2):
            ingredientsList.append((elements[ingredientNo+1],int(elements[ingredientNo])))
        #print(target, targetQuantity, ingredientsList)
        productList.append([target, targetQuantity, ingredientsList])
    return productList


def makeObjects():
    # this makes all the objects, producing a dict called products[itemName] pointing to the object
    productstext = parse()
    productsDict = {'ORE':Product("ORE")}
    for p in productstext:
        productsDict[p[0]] = Product(p[0])
    for p in productstext:
        productsDict[p[0]].quantityProduced=p[1]
        for ingredient in p[2]:
            productsDict[p[0]].addNeed(ingredient[0],ingredient[1])
    return productsDict


def part1(FuelNeeded):
    products = makeObjects()

    # Manufacturing items sometimes results in more being created than necessary. I used a "dump" to store the excess,
    # so I was not making more than needed.
    dump = defaultdict(int)

    oreneeded = 0
    # I used a simple queue based system in the end.
    # To start with, I added the required fuel to the list
    reqs= [["FUEL", FuelNeeded]]  # queue for the required items

    while len(reqs)>0:
        # We run the process in reverse-> from Fuel to starting ingredients:
        # While there are still items that need to be broken down...
        # take an item out of the reqs queue
        item, noNeeded = reqs.pop(0)
        # Take as many as possible out of the dump and work out what's left
        dumpMove = min(noNeeded, dump[item])
        noNeeded -= dumpMove
        dump[item] -= dumpMove
        # work out how many batches are needed
        batchesNeeded = math.ceil(noNeeded/products[item].quantityProduced)
        # work out the raw ingredients for the batches
        # Note this use of deepcopy. I'll explain later
        ingredients = deepcopy(products[item].needs)
        for i in ingredients:
            i[1] *= batchesNeeded  # Because we need multiple batches, we multiply the required ingredients
            # The problem was that this was permanently multiplying the required ingredients for this chemical
            # in the original object. I used deepcopy to make a copy of these ingredients, so I could multiply them
            # on a temporary basis. This is horrible, but it worked. If it hadn't worked, i would have looked at
            # ditching the objects altogether
        # add the ingredients to the queue
        for i in ingredients:
            if i[0] == "ORE":      # (unless it's ORE, in which case increment the counter and just delete it)
                oreneeded += i[1]
            elif i[1] > 0:  # It's possible that the requirements are zero, if we took them all from the dump
                reqs.append(i)
        # see how many spares are also made, and add them to the dump
        spares = (batchesNeeded * products[item].quantityProduced) - noNeeded
        dump[item] += spares

    return oreneeded

def part2():
    #  binary search for the lowest fuel that takes more than 1000000000000 fuel
    trillion = 1000000000000
    low = 10000000
    high =100000000
    mid = (low+high)//2
    while low <= high:
        fuelneeded = part1(mid)
        if fuelneeded > trillion:
            high = mid - 1
        else:
            if part1(mid+1) < trillion:
                low = mid + 1
            else:
                print(mid, "is the breakpoint")
                break
        mid = (low+high)//2

print(part1(1))
part2()