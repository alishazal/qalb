"""
Usage: python3 getArabiziAndGold.py [folder] [folder/output.arabizi] [folder/output.gold]
"""

import xml.etree.ElementTree as ET
import os
import sys
from camel_tools.utils.charmap import CharMapper
ar2bw = CharMapper.builtin_mapper('ar2bw')

def fixPunctuation(line):

    punctuationDict = {"؛": ";", "؟": "?", "،": ","}
    newLine = []
    for word in range(len(line)):
        newWord = ""
        for char in range(len(line[word])):
            currCharacter = line[word][char]
            if currCharacter in punctuationDict:
                newWord += punctuationDict[currCharacter]
            else:
                newWord += currCharacter
        newLine.append(newWord)
    return newLine

def removeNones(arr):
    return list(filter(lambda x: x.text != None, arr))


dirs = os.listdir(sys.argv[1])
dirs.sort()

arabiziOutput = open(sys.argv[2], "w")
goldOutput = open(sys.argv[3], "w")

for i in dirs:
    if i[-3:] != "xml":
        continue

    tree = ET.parse(sys.argv[1] + i)
    root = tree.getroot()

    tracker = 0
    allWords = root.findall("./su/annotated_arabizi/token")
    allRawGold = removeNones(root.findall("./su/corrected_transliteration"))
    totalLinesInFile = len(allRawGold)
    lineCounter = 0
    for source in root.findall("./su/source"):
        if lineCounter >= totalLinesInFile:
            continue
            
        numLines = 0
        if source.text == None:
            continue

        arabiziOutput.write(source.text.strip() + "\n")

        currGoldLine = ar2bw(allRawGold[lineCounter].text.strip()).split()
        currGoldLine = fixPunctuation(currGoldLine)

        numLines = len(source.text.split())

        if tracker >= len(allWords):
            continue

        wordsOfThisLineCounter = 0
        for j in range(tracker, tracker + numLines):
            if "tag" in allWords[j].attrib and allWords[j].attrib["tag"] in ["punctuation", "foreign"]:
                currGoldLine[wordsOfThisLineCounter] = "#"
            wordsOfThisLineCounter += 1
        
        goldOutput.write(" ".join(currGoldLine) + "\n")
        tracker += numLines
        lineCounter += 1
        
arabiziOutput.close()
