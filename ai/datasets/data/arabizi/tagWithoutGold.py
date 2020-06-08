"""
Usage: python tagWithoutGold.py [xyz.arabizi] [newXyz.arabizi] [xyz.lines] [context_number]
"""

import sys

def zeroContext(afLines, newArabiziFile, linesFile):
    for line in afLines:
        line = line.strip()
        line = line.split()

        linesFile.write(str(len(line)) + "\n")

        for word in line:
            newArabiziFile.write("<bow> " + word + " <eow>" + "\n")

def nonZeroContext(afLines, newArabiziFile, linesFile, context):
    # Making tagged version of arabizi file
    for line in afLines:
        line = line.strip()
        line = line.split()

        linesFile.write(str(len(line)) + "\n")

        line = (["<bos>"] * context) + line  + (["<eos>"] * context)
        for word in range(context, len(line) - context):
            newLine = line[word - context: word] + ["<bow>", line[word], "<eow>"] + line[word + 1: word + context + 1]
            strLine = " ".join(newLine) + "\n"
            newArabiziFile.write(strLine)

afLines = open(sys.argv[1], "r").readlines()
newArabiziFile = open(sys.argv[2], "w")
linesFile = open(sys.argv[3], "w")
context = int(sys.argv[4])

if context == 0:
    zeroContext(afLines, newArabiziFile, linesFile)
else:
    nonZeroContext(afLines, newArabiziFile, linesFile, context)

newArabiziFile.close()
linesFile.close()