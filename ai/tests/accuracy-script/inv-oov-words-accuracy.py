# Usage python inv-oov-words-accuracy.py [pred.out] [unknown.out] [some.gold] [inv or oov]

import sys

systemOutputfile = open(sys.argv[1], "r")
soLines = systemOutputfile.readlines()

unknown = open(sys.argv[2], "r").readlines()

goldFile = open(sys.argv[3], "r")
gfLines = goldFile.readlines()

vocab = "0"
if sys.argv[4] == "oov":
    vocab = "1"

correct = 0
total = 0


for i in range(len(soLines)):
    
    currPredLine = soLines[i].split(" ")
    currGoldLine = gfLines[i].split(" ")
    currUnknownLine = unknown[i].strip().split(" ")

    if len(currPredLine) == len(currGoldLine):
        for j in range(len(currPredLine)):
            if currUnknownLine[j] == vocab:
                if currPredLine[j] == currGoldLine[j]:
                    correct += 1
                total += 1
    
    elif len(currPredLine) > len(currGoldLine):
        for j in range(len(currPredLine)):
            if j < len(currGoldLine) and currUnknownLine[j] == vocab:
                if currPredLine[j] == currGoldLine[j]:
                    correct += 1
                total += 1
    else:
        for j in range(len(currGoldLine)):
            if j < len(currPredLine) and currUnknownLine[j] == vocab:
                if currPredLine[j] == currGoldLine[j]:
                    correct += 1
                total += 1

print("Correct words are", correct)
print("Total words are", total)
print("Accuracy is:", ((correct/total)*100))

systemOutputfile.close()
goldFile.close()