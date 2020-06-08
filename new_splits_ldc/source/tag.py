"""
Usage: python tag.py [xyz.arabizi] [newXyz.arabizi] [context_number]
"""

import sys

def zeroContext(afLines, newArabiziFile):
    for line in afLines:
        line = line.strip()
        line = line.split()

        for word in line:
            newArabiziFile.write("<bow> " + word + " <eow>" + "\n")

def nonZeroContext(afLines, newArabiziFile, context):
    # Making tagged version of arabizi file
    for line in afLines:
        line = line.strip()
        line = line.split()

        line = (["<bos>"] * context) + line  + (["<eos>"] * context)
        for word in range(context, len(line) - context):
            newLine = line[word - context: word] + ["<bow>", line[word], "<eow>"] + line[word + 1: word + context + 1]
            strLine = " ".join(newLine) + "\n"
            newArabiziFile.write(strLine)

afLines = open(sys.argv[1], "r").readlines()
newArabiziFile = open(sys.argv[2], "w")
context = int(sys.argv[3])

if context == 0:
    zeroContext(afLines, newArabiziFile)
else:
    nonZeroContext(afLines, newArabiziFile, context)

newArabiziFile.close()