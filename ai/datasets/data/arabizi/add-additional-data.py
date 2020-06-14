"""
Usage: python3 add-additional-data.py [train.arabizi] [train.gold] [additional-train.arabizi] [additional-train.gold] [new-train.arabzi] [new-train.gold]
"""

import sys
import random
random.seed(1)

origTrainArabizi = open(sys.argv[1], "r").readlines()
origTrainGold = open(sys.argv[2], "r").readlines()
origTrainCombined = [list(l) for l in zip(origTrainArabizi, origTrainGold)]

addTrainArabizi = open(sys.argv[3], "r").readlines()
addTrainGold = open(sys.argv[4], "r").readlines()
addTrainCombined = [list(l) for l in zip(addTrainArabizi, addTrainGold)]

finalTrainArabizi = open(sys.argv[5], "w")
finalTrainGold = open(sys.argv[6], "w")

newData = origTrainCombined + addTrainCombined
random.shuffle(newData)

for i in range(len(newData)):
    finalTrainArabizi.write(newData[i][0].strip() + "\n")
    finalTrainGold.write(newData[i][1].strip() + "\n")

finalTrainArabizi.close()
finalTrainGold.close()