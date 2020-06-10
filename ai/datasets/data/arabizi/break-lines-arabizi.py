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
    currLineNoOfWords = len(line)

    if currLineNoOfWords <= length:
        new.write(" ".join(line) + "\n")
        linesFile.write(str(currLineNoOfWords) + " no " + "\n")
    
    else:
        count = 0
        for i in range(0, currLineNoOfWords, length):
            if currLineNoOfWords - i >= length:
                new.write(" ".join(line[i:i+length]) + "\n")
                if i+length >= currLineNoOfWords:
                    linesFile.write(str(length) + " no " + "\n")
                else:
                    linesFile.write(str(length) + " yes " + "\n")
            else:
                remainder = currLineNoOfWords % length
                new.write(" ".join(line[i-(length-remainder):i+remainder]) + "\n")
                linesFile.write(str(remainder) + " no " + "\n")
            
            count += 1

orig.close()
new.close()
linesFile.close()