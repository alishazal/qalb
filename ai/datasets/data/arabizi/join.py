"""
Usage: python join.py [sysPred.out] [xyz.lines] [finalPred.out]
"""

import sys

pred = sys.argv[1]
predFile = open(pred, "r")
pfLines = predFile.readlines()

linesFile = open(sys.argv[2], "r")
lLines = linesFile.readlines()

newPredFile = open(sys.argv[3], "w")

predFileLinesTracker = 0

for num in lLines:
    num = int(num.strip())
    
    finalLine = ""
    for i in range(predFileLinesTracker, predFileLinesTracker + num):
        finalLine += pfLines[i].strip() + " "

    predFileLinesTracker += num
    newPredFile.write(finalLine.strip() + "\n")


predFile.close()
linesFile.close()
newPredFile.close()