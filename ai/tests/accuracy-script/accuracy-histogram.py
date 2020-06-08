# Usage python accuracy-histogram.py [system-pred.out] [something.gold]

import sys

def accuracy(system, gold):
    system = system.strip().split(" ")
    gold = gold.strip().split(" ")

    correct = 0
    total = 0
    if len(system) == len(gold):
        for i in range(len(system)):
            if system[i] == gold[i]:
                correct += 1
            total += 1
    
    elif len(system) > len(gold):
        for i in range(len(system)):
            if i < len(gold) and system[i] == gold[i]:
                correct += 1
            total += 1
    else:
        for i in range(len(gold)):
            if i < len(system) and system[i] == gold[i]:
                correct += 1
            total += 1
    
    return (correct/total) * 100


systemOutputfile = open(sys.argv[1], "r")
soLines = systemOutputfile.readlines()

goldFile = open(sys.argv[2], "r")
gfLines = goldFile.readlines()

hist = {}

for line in range(len(soLines)):
    noOfWords = len(gfLines[line].strip().split(" "))
    currAccuracy = accuracy(soLines[line], gfLines[line])
    weightedCurrAccuracy = currAccuracy * noOfWords
    if noOfWords in hist:
        hist[noOfWords][0] += weightedCurrAccuracy
        hist[noOfWords][1] += noOfWords
    
    else:
        hist[noOfWords] = [weightedCurrAccuracy, noOfWords]

histList = []
for i in hist:
    histList.append([i, round(hist[i][0]/hist[i][1], 1)])

histList.sort(key = lambda ele: ele[0])

for i in histList:
    print(i[1])


systemOutputfile.close()
goldFile.close()