from processor import Processor

def load(fname):
    f = open(fname, "r")
    out = []
    for line in f:
        out.append(line.strip())
    return out[0]

program = [int(c) for c in load("17.txt").split(",")]

def part1():
    proc = Processor(program)
    out = proc.run([])
    mapp = [[]]
    row = 0
    i = 0
    while i < len(out):
        if out[i] == 10:
            row+=1
            mapp.append([])
        else:
            mapp[row].append(chr(out[i]))
        i+=1
    total =0


    for row in range(len(mapp)):
        for col in range(len(mapp[row])):
            if row > 0 and row < 58 and col > 0 and col < 40:
                if mapp[row][col] == mapp[row-1][col] and mapp[row][col] == mapp[row+1][col] and mapp[row][col] == mapp[row][col-1] and mapp[row][col] == mapp[row][col+1] and mapp[row][col]=="#":
                    total += row * col
                    print("O", end="")
                    continue
            print(mapp[row][col], end="")
        print()
    print(total)

def part2():
    proc = Processor(program)
    proc.memory[0] = 2
    A = "L,12,L,8,R,10\n"
    B = "R,4,R,12,R,10,L,12\n"
    C = "L,12,R,4,R,12\n"
    MP = "B,C,C,A,A,B,C,C,A,B\n"
    out = proc.run([ord(c) for c in MP])
    out = proc.run([ord(c) for c in A])
    out = proc.run([ord(c) for c in B])
    out = proc.run([ord(c) for c in C])
    out = proc.run([ord(c) for c in "n\n"])
    print(out)

part1()
part2()

