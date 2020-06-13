# -*- coding: utf-8 -*-

"""
Usage: python3 extract_sample_of_data.py [sample_size]
"""

import xml.etree.ElementTree as ET
import os
import sys
import random
random.seed(1)

def getNoOfWordsInList(l):
    count = 0
    for line in l:
        count += len(line.strip().split())

    return count

sampleSize = int(sys.argv[1])
english = open("sms_chat_data.english", "w")

files = os.listdir("data")
files.sort()

fileCount = 1
lineCount = 0
englishLines = []
for file in files:

    if fileCount % 200 == 0:
        print(str(fileCount) + " files read. " + str(lineCount) + " lines processed.")

    if file[-3:] != "xml":
        continue

    tree = ET.parse("data/" + file)
    root = tree.getroot()
    allLines = root.findall("./messages/message/body")
    for line in allLines:
        if line.text == None:
            continue
        englishLines.append(line.text.strip())
        lineCount += 1

    fileCount += 1

#Taking out a sample of data
print("Now sampling data")
sampledEnglishLines = englishLines
noOfSampledLines = len(englishLines)
noOfSampledWords = getNoOfWordsInList(sampledEnglishLines)
while noOfSampledWords > sampleSize:
    currSample = random.sample(sampledEnglishLines, noOfSampledLines)
    noOfSampledWords = getNoOfWordsInList(currSample)
    if noOfSampledLines > 5000:
        noOfSampledLines -= 5000
    else:
        noOfSampledLines -= 100

print("Sampling completed. Writing to file")
for line in currSample:
    english.write(line + "\n")
        
english.close()