from processor import Processor
from itertools import permutations


def load(fname):
    f = open(fname, "r")
    out = []
    for line in f:
        out.append(line.strip())
    return out


def part1():
    progstring = load("7.txt")[0]
    program = [int(inst) for inst in progstring.split(",")]
    settings = list(permutations([0,1,2,3,4],5))
    max = 0
    for setting in settings:
        out = 0
        for i in range(5):
            newProc = Processor(program)
            out = newProc.run([setting[i], out])
        if out is not None and out > max:
            max = out
    print(max)

def part2():
    progstring = load("7.txt")[0]
    program = [int(inst) for inst in progstring.split(",")]
    settings = list(permutations([9,8,7,6,5],5)) # all possible permutations of the phase settings

    max = 0
    for setting in settings:
        processors = [ Processor(program) for n in range(5)]

        # send phase settings to each
        for i in range(5):
            out = processors[i].run([setting[i]])
        # now start them all running

        lastE = None
        output = 0
        while sum([p.runState for p in processors]) > 0:  # The runState is zero when the processor is ended
            for i in range(5):
                output = processors[i].run([output]) # pass the output of this processor as the input of the next
                # The processors now pause when they run out of input, remembering their current line position
            if output is not None:
                lastE = output
        if lastE > max:
            max = lastE
    print(max)

part1()
part2()