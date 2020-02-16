# Usage python accuracy.py [system-pred.out] [something.gold] [word/sentence]

import sys

systemOutput = sys.argv[1]
systemOutputfile = open(systemOutput, "r")
soLines = systemOutputfile.readlines()

gold = sys.argv[2]
goldFile = open(gold, "r")
gfLines = goldFile.readlines()

correct = 0
total = 0

correctDict = {}
wrongDict = {}

for i in range(len(soLines)):
    if soLines[i] == gfLines[i]:
        correct += 1
        if len(soLines[i]) in correctDict:
            correctDict[len(soLines[i])] += 1
        else:
            correctDict[len(soLines[i])] = 1
    else:
        if len(soLines[i]) in wrongDict:
            wrongDict[len(soLines[i])] += 1
        else:
            wrongDict[len(soLines[i])] = 1
    total += 1

level = sys.argv[3]
if level == "word":
    print("Correct dictionary:", correctDict)
    print("Incorrect dictionary:", wrongDict)
print("Correct lines are", correct)
print("Total lines are", total)
print("Accuracy is:", ((correct/total)*100))

systemOutputfile.close()
goldFile.close()