"""
UsageL python3 break-lines-arabizi.py [original.arabizi] [new.arabizi] [new.lines] [chunk-length]
"""
import sys
import math

origArabizi = open(sys.argv[1], "r").readlines()
newArabizi = open(sys.argv[2], "w")
linesFile = open(sys.argv[3], "w")
length = int(sys.argv[4])

for line in range(len(origArabizi)):
    currArabiziLine = origArabizi[line].strip().split()

    currLineNoOfWords = len(currArabiziLine)

    if currLineNoOfWords <= length:
        newArabizi.write(" ".join(currArabiziLine) + "\n")
        linesFile.write(str(currLineNoOfWords) + " no " + "\n")
    
    else:
        remainder = currLineNoOfWords % length
        totalIterations = math.ceil(currLineNoOfWords / length)
        count = 0
        for i in range(0, currLineNoOfWords, length):
            if currLineNoOfWords - i >= length:
                newArabizi.write(" ".join(currArabiziLine[i:i+length]) + "\n")
                if i+length >= currLineNoOfWords:
                    linesFile.write(str(length) + " no " + "\n")
                else:
                    if count == totalIterations - 2 and remainder != 0:
                        linesFile.write(str(remainder) + " yes " + "\n")
                    else:
                        linesFile.write(str(length) + " yes " + "\n")
            else:
                newArabizi.write(" ".join(currArabiziLine[i-(length-remainder):i+remainder]) + "\n")
                linesFile.write(str(length) + " no " + "\n")

            count += 1

newArabizi.close()
linesFile.close()