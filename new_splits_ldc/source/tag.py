"""
Usage: python tag.py [xyz.arabizi] [newXyz.arabizi] [context_number]
"""

import sys

arabiziFile = open(sys.argv[1], "r")
afLines = arabiziFile.readlines()

newArabiziFile = open(sys.argv[2], "w")

context = int(sys.argv[3])

# Making tagged version of arabizi file
for line in afLines:
    line = line.strip()
    line = line.split()

    wordCtr = 0
    for word in line:
        newLine = []

        for i in list(range(-context, context+1)):
            if wordCtr + i >= 0 and wordCtr + i < len(line):
                if wordCtr + i  == 0:
                    newLine.append("<bos>")
            
                if i == 0:
                    newLine.extend(["<bow>", word, "<eow>"])
                elif len(newLine) != 0 and newLine[-1] not in ["<bow>", "<eow>", "<bos>", "<eos>"]:
                    newLine.extend([" ", line[wordCtr + i]])
                else:
                    newLine.append(line[wordCtr + i])

                if wordCtr + i == len(line) - 1:
                    newLine.append("<eos>")

        if context == 1:
            strLine = " ".join(newLine) + "\n"
        else:
            strLine = " ".join(newLine) + "\n"
        newArabiziFile.write(strLine)
        wordCtr += 1

arabiziFile.close()
newArabiziFile.close()