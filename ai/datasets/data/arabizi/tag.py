"""
Usage: python tag.py [xyz.arabizi] [xyz.gold] [newXyz.arabizi] [newXyz.gold] [xyz.lines] [context_number]
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

        wordCtr = 0
        for word in line:
            newLine = []

            for i in list(range(-context, context+1)):
                if wordCtr + i >= 0 and wordCtr + i < len(line):
                    if wordCtr + i  == 0 and wordCtr == 0:
                        newLine.append("<bos>")
                
                    if i == 0:
                        newLine.extend(["<bow>", word, "<eow>"])
                    elif len(newLine) != 0 and newLine[-1] not in ["<bow>", "<eow>", "<bos>", "<eos>"]:
                        newLine.extend([" ", line[wordCtr + i]])
                    else:
                        newLine.append(line[wordCtr + i])

                    if wordCtr + i == len(line) - 1 and wordCtr == len(line) - 1:
                        newLine.append("<eos>")

            strLine = " ".join(newLine) + "\n"
            newArabiziFile.write(strLine)
            wordCtr += 1
    

afLines = open(sys.argv[1], "r").readlines()
gfLines = open(sys.argv[2], "r").readlines()
newArabiziFile = open(sys.argv[3], "w")
newGoldFile = open(sys.argv[4], "w")
linesFile = open(sys.argv[5], "w")
context = int(sys.argv[6])

if context == 0:
    zeroContext(afLines, newArabiziFile, linesFile)
else:
    nonZeroContext(afLines, newArabiziFile, linesFile, context)

# Making single word per line version of gold file
for line in gfLines:
    line = line.strip()
    line = line.split()
    for word in line:
        newGoldFile.write(word + "\n")

newArabiziFile.close()
newGoldFile.close()
linesFile.close()