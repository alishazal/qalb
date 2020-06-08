"""
UsageL python3 break-lines-all.py [original.arabizi] [original.gold] [newArabizi.arabizi] [new.gold] [new.lines] [chunk-length]
"""

import sys

origArabizi = open(sys.argv[1], "r").readlines()
origGold = open(sys.argv[2], "r").readlines()
newArabizi = open(sys.argv[3], "w")
newGold = open(sys.argv[4], "w")
linesFile = open(sys.argv[5], "w")
length = int(sys.argv[6])

for line in range(len(origArabizi)):
    currArabiziLine = origArabizi[line].strip().split()
    currGoldLine = origGold[line].strip().split()

    if len(currArabiziLine) <= length:
        newArabizi.write(" ".join(currArabiziLine) + "\n")
        newGold.write(" ".join(currGoldLine) + "\n")
        linesFile.write("1\n")
    
    else:
        count = 0
        for i in range(0, len(currArabiziLine), length):
            newArabizi.write(" ".join(currArabiziLine[i:i+length]) + "\n")
            newGold.write(" ".join(currGoldLine[i:i+length]) + "\n")
            count += 1
        
        linesFile.write(str(count) + "\n")

newArabizi.close()
newGold.close()
linesFile.close()