"""
Usage: python no-context.py [xyz.arabizi] [xyz.gold] [newXyz.arabizi] [newXyz.gold]
"""

import sys

arabizi = sys.argv[1]
arabiziFile = open(arabizi, "r")
afLines = arabiziFile.readlines()

gold = sys.argv[2]
goldFile = open(gold, "r")
gfLines = goldFile.readlines()

newArabiziFile = open(sys.argv[3], "w")
newGoldFile = open(sys.argv[4], "w")


# Making single word per line version of arabizi file
for line in afLines:
    line = line.strip()
    line = line.split()
    for word in line:
        newArabiziFile.write(word + " " + "\n")

# Making single word per line version of gold file
for line in gfLines:
    line = line.strip()
    line = line.split()
    for word in line:
        newGoldFile.write(word + "\n")

arabiziFile.close()
goldFile.close()
newArabiziFile.close()
newGoldFile.close()