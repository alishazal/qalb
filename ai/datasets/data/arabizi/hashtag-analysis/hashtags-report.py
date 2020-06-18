"""
Usage: python3 hashtags-report.py [ml-input] [ml-output] [pred.out]
"""

import sys

mlInput = open(sys.argv[1], "r").readlines()
mlOutput = open(sys.argv[2], "r").readlines()
pred = open(sys.argv[3], "r").readlines()

# First make new gold with #e and #f
newGold = []
for mlIn, mlOut in zip(mlInput, mlOutput):
    currMlIn = mlIn.strip().split()
    currMlOut = mlOut.strip().split()

    currLine = []
    for currMlInWord, currMlOutWord in zip(currMlIn, currMlOut):
        if currMlInWord == "#" and currMlOutWord == "#":
            currLine.append("#e")
        
        elif currMlInWord != "#" and currMlOutWord == "#":
            currLine.append("#f")

        else:
            currLine.append(currMlOutWord)

    newGold.append(" ".join(currLine))

# Analysis starts here
emoHashtagCount = 0
emoHashtagTotal = 0
foreignHashtagCount = 0
foreignHashtagTotal = 0
overGenerationCount = 0
for p, g in zip(pred, newGold):
    p = p.strip().split()
    g = g.strip().split()
    
    for pWord, gWord in zip(p, g):
        if gWord == "#e":
            if pWord == "#":
                emoHashtagCount += 1
            emoHashtagTotal += 1
        
        elif gWord == "#f":
            if pWord == "#":
                foreignHashtagCount += 1
            foreignHashtagTotal += 1

        else:
            if pWord == "#":
                overGenerationCount += 1

print("Emoji & punctuation hashtags score:", emoHashtagCount, "/", emoHashtagTotal)
print("Foreign hashtags score:", foreignHashtagCount, "/", foreignHashtagTotal)
print("Hashtag wrongly generated:", overGenerationCount)