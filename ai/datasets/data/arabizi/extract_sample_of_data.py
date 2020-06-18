# -*- coding: utf-8 -*-

"""
Usage: python3 extract_sample_of_data.py [orig-file.arabizi] [orig-file.gold] [new-file.arabizi] [new-file.gold] [sample_size]
"""

import os
import sys
import random
random.seed(1)

def getNoOfWordsInList(l):
    count = 0
    for line in l:
        count += len(line[0].strip().split())

    return count

origArabizi = open(sys.argv[1], "r").readlines()
origGold = open(sys.argv[2], "r").readlines()
origCombined = [list(l) for l in zip(origArabizi, origGold)]

newArabizi = open(sys.argv[3], "w")
newGold = open(sys.argv[4], "w")
sampleSize = int(sys.argv[5])

#Taking out a sample of data
print("Now sampling data")
sampledLines = origCombined
noOfSampledLines = len(origCombined)
noOfSampledWords = getNoOfWordsInList(sampledLines)
while noOfSampledWords > sampleSize:
    currSample = random.sample(sampledLines, noOfSampledLines)
    noOfSampledWords = getNoOfWordsInList(currSample)
    if noOfSampledLines > 500:
        noOfSampledLines -= 500
    else:
        noOfSampledLines -= 50

print("Sampling completed. Writing to file")
for line in currSample:
    newArabizi.write(line[0].strip() + "\n")
    newGold.write(line[1].strip() + "\n")
        
newArabizi.close()
newGold.close()