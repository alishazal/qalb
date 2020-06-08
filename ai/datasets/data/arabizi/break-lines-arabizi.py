"""
UsageL python3 break-lines-arabizi.py [original.arabizi] [new.arabizi] [new.lines] [chunk-length]
"""

import sys

orig = open(sys.argv[1], "r")
new = open(sys.argv[2], "w")
linesFile = open(sys.argv[3], "w")
length = int(sys.argv[4])

for line in orig:
    line = line.strip().split()

    if len(line) <= length:
        new.write(" ".join(line) + "\n")
        linesFile.write("1\n")
    
    else:
        count = 0
        for i in range(0, len(line), length):
            new.write(" ".join(line[i:i+length]) + "\n")
            count += 1
        
        linesFile.write(str(count) + "\n")

orig.close()
new.close()
linesFile.close()