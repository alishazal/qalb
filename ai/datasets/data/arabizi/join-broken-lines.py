"""
Usage: python join-broken-lines-version-2-beginning-chunk.py [broken.arabizi] [xyz.lines] [final.out]
"""

import sys

broken = open(sys.argv[1], "r").readlines()
lines = open(sys.argv[2], "r").readlines()
final = open(sys.argv[3], "w")

newCompleteLine = []
for l in range(len(broken)):
    currBrokenLine = broken[l].strip().split()
    currLinesLine = lines[l].strip().split()
    
    newCompleteLine.extend(currBrokenLine[:int(currLinesLine[0])])
    if currLinesLine[1] == "no":
        final.write(" ".join(newCompleteLine) + "\n")
        newCompleteLine = []

final.close()
