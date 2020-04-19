"""
Usage: python3 mlPrepGold.py [raw.gold] [ml-ready.arabizi] [new.gold]
"""

import sys

rawGoldFile = open(sys.argv[1], "r")
arabiziInput = open(sys.argv[2], "r")
newGoldFile = open(sys.argv[3], "w")

rawGoldLines = rawGoldFile.readlines()
lineCounter = 0
for arabiziLine in arabiziInput:
    newGoldLine = []
    currGoldLine = rawGoldLines[lineCounter].strip().split(" ")

    arabiziLine = arabiziLine.strip().split(" ")
    for word in range(len(arabiziLine)):
        if currGoldLine[word] != "#" and arabiziLine[word] == "#":
            newGoldLine.append("#")
        else:
            newGoldLine.append(currGoldLine[word])

    newGoldLine = " ".join(newGoldLine)

    if newGoldLine == " ": print("what")
    newGoldFile.write(newGoldLine + "\n")
    lineCounter += 1

rawGoldFile.close()
arabiziInput.close()
newGoldFile.close()
