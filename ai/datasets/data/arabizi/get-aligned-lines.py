"""
Usage: python3 get-aligned-lines.py [file.arabizi] [file.gold] [new-file.arabizi] [new-file.gold]
"""

import sys

arabizi = open(sys.argv[1], "r")
arabiziLines = arabizi.readlines()
gold = open(sys.argv[2], "r")
goldLines = gold.readlines()

newArabizi = open(sys.argv[3], "w")
newGold = open(sys.argv[4], "w")

for i in range(len(arabiziLines)):
    currArabiziLine = arabiziLines[i].split(" ")
    currGoldLine = goldLines[i].split(" ")

    if len(currArabiziLine) == len(currGoldLine):
        newArabizi.write(" ".join(currArabiziLine))
        newGold.write(" ".join(currGoldLine))

arabizi.close()
gold.close()
newArabizi.close()
newGold.close()