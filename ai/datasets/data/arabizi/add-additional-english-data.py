"""
Usage: python3 add-additional-english-data.py [train.arabizi] [train.gold] [new-data.english] [new-train.arabizi] [new-train.gold]
"""

import sys
import random
random.seed(1)

origTrainArabizi = open(sys.argv[1], "r").readlines()
origTrainGold = open(sys.argv[2], "r").readlines()
origTrainCombined = [list(l) for l in zip(origTrainArabizi, origTrainGold)]

englishData = open(sys.argv[3], "r").readlines()
newTrainArabizi = open(sys.argv[4], "w")
newTrainGold = open(sys.argv[5], "w")

englishDataLabels = []
for line in englishData:
    noOfWords = len(line.strip().split())
    currLabel = ["#"] * noOfWords
    englishDataLabels.append(" ".join(currLabel))

combinedEnglishData = [list(l) for l in zip(englishData, englishDataLabels)]

newData = origTrainCombined + combinedEnglishData
random.shuffle(newData)

for i in range(len(newData)):
    newTrainArabizi.write(newData[i][0].strip() + "\n")
    newTrainGold.write(newData[i][1].strip() + "\n")

newTrainArabizi.close()
newTrainGold.close()