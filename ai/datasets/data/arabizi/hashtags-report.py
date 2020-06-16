"""
Usage: python3 hashtags-report.py [sys.out] [gold]
"""

import sys

arabizi = open(sys.argv[1], "r").readlines()
gold = open(sys.argv[2], "r").readlines()


truePositive = 0
falsePositive = 0
falseNegative = 0
trueNegative = 0
for i in range(len(arabizi)):
    currArabiziLine = arabizi[i].strip().split()
    currGoldLine = gold[i].strip().split()

    for j in range(len(currArabiziLine)):
        if j >= len(currGoldLine):
            break
        
        currArabiziWord = currArabiziLine[j]
        currGoldWord = currGoldLine[j]
        if currArabiziWord == "#" and currGoldWord == "#":
            truePositive += 1
        
        elif currArabiziWord == "#" and currGoldWord != "#":
            falsePositive += 1

        elif currArabiziWord != "#" and currGoldWord == "#":
            falseNegative += 1

        else:
            trueNegative += 1

print("Hashtag in pred and gold - true positive:", truePositive)
print("Hashtag in pred and not in gold - false positive:", falsePositive)
print("Hashtag not in pred but in gold - false negative:", falseNegative)
print("Hashtag not in pred and not in gold - true negative:", trueNegative)