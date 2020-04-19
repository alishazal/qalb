"""
Usage: python3 getArabiziAndGold.py [folder] [folder/raw-output.arabizi] [folder/raw-output.gold]
"""

import xml.etree.ElementTree as ET
import os
import sys
import re
import unicodedata as ud
from camel_tools.utils.charmap import CharMapper
ar2bw = CharMapper.builtin_mapper('ar2bw')


def isPunctuation(char, position):

    if position == "opening":
        if char in "\"([{-":
            return True
        else:    
            return False
    else:
        if char in ".,?!\":;-()[]}{=_":
            return True
        else:    
            return False

def isEmoji(char):
    if (ud.category(char) == "So") or (ud.category(char) == "Co") or (ord(char) in range(0x1F3Fb, 0x1F400)):
        return True

    return False

def separateGraphicEmoji(word):

    newWord = ""

    for i in range(len(word)):
        char = word[i]
        if isEmoji(char):
            # If its the first char of word and word has more than 1 char
            if i == 0 and len(word) > 1:
                if not isEmoji(word[i+1]):
                    newWord += char + "[+] "
                else:
                    newWord += char
            
            # If its the first char of word and word has just 1 char
            elif i == 0 and len(word) == 1:
                newWord += char
            
            # If its in the middle of the word
            elif i > 0 and i < (len(word) - 1):
                if isEmoji(word[i-1]) and isEmoji(word[i+1]):\
                    newWord += char
                elif isEmoji(word[i-1]) and not isEmoji(word[i+1]):
                    newWord += char + "[+] "
                elif not isEmoji(word[i-1]) and isEmoji(word[i+1]):
                    newWord += " [+]" + char
                else:
                    newWord += " [+]" + char + "[+] "

            #If its the last char of the word
            elif i == len(word) - 1:
                if not isEmoji(word[i-1]):
                    newWord += " [+]" + char
                else:
                    newWord += char

        else:
            newWord += char

    return newWord


def separatePunctuationAndTextEmoji(word):

    firstChar = word[0]
    lastChar = word[-1]

    if isPunctuation(firstChar, "opening"): #If the first char of word is a punctiation 
        for i in range(len(word)): #Go over the word
            if not isPunctuation(word[i], "closing"): #As soon as the first non-punctuation char is encountered, put the separation mark [+]
                word = word[:i] + "[+] " + word[i:] 
                break

    if isPunctuation(lastChar, "closing"): #If the last char of word is a punctiation 
        if "')" in word or "'(" in word:
            for i in range(len(word)-1, -1, -1): #Go over the word backwards
                if not isPunctuation(word[i], "closing") and not word[i] == "'": #As soon as the first non-punctuation char is encountered, put the separation mark [+]
                    word = word[:i+1] + " [+]" + word[i+1:]    
                    break
        else:
            for i in range(len(word)-1, -1, -1): #Go over the word backwards
                if not isPunctuation(word[i], "closing"): #As soon as the first non-punctuation char is encountered, put the separation mark [+]
                    word = word[:i+1] + " [+]" + word[i+1:]    
                    break
    
    else: # If last char is not punc (for example it is :D, :P, etc)
        #match for text emoticons like :D :-) ;) etc
        word = word.replace("3-|", " [+]3-|")
        word = word.replace("8-|", " [+]8-|")
        word = word.strip(" [+]")
        match = re.search(r'[\\]*[=:;][-\'"_.]*[OoPpsSDVv@*|/\\]+', word, re.IGNORECASE) 
        if match:
            emoticon = match.group(0) # matched emoticon
            emoticonIndex = word.find(emoticon) # index of matched emoticon
            if (emoticonIndex  + len(emoticon) - 1 == len(word) - 1) and (emoticonIndex - 1 >= 0): #if there is a char attached to emoticon
                if isPunctuation(word[emoticonIndex - 1], "closing"): #check if attached char is a punctuation mark
                    for i in range(emoticonIndex - 1, -1, -1): #Go behind the emoticon
                        if not isPunctuation(word[i], "closing"): #As soon as the first non-punctuation char is encountered, put the separation mark [+]
                            word = word[:i+1] + " [+]" + word[i+1:]    
                            break
                #if the attached char is a regular letter
                else:
                    word = word[:emoticonIndex] + " [+]" + word[emoticonIndex:]
    
    return word

def preprocessor(line):

    line = line.strip()
    line = line.split()

    # First check for graphic emojis and separate those
    newLine = ""
    for i in range(len(line)):
        newLine += separateGraphicEmoji(line[i]) + " "

    line = newLine.strip().split()
    # Then check punctuations and text emoticons
    for i in range(len(line)): # go over every word of line
        if "[+]" in line[i]: 
            continue
        for char in line[i]: # go over every character of word
            if isPunctuation(char, "closing"): # if char is punctuation
                line[i] = separatePunctuationAndTextEmoji(line[i]) #separate punctuation from word and replace in line
                break

    return " ".join(line)

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

def changeForeignsToHash(line):
    return ("# " * len(line.strip().split(" "))).strip()

def handleContinuousPluses(line):
    line = line.strip().split(" ")
    newLine = []

    counter = 0
    for _ in line:
        if counter >= len(line):
            break

        if "[+]" in line[counter]:
            newWord = line[counter]
            if counter == len(line) - 2 and "[+]" in line[counter + 1]:
                nextWord = line[counter + 1].replace("[+]", "")
                newLine.append(line[counter] + nextWord)
                break
            else:
                if counter == len(line) - 1:
                    counter += 1
                else:
                    for i in range(counter + 1, len(line)):
                        if "[+]" in line[i]:
                            newWord += line[i].replace("[+]", "")
                            counter += 1
                        else:
                            counter += 1
                            break
        else:
            newWord = line[counter]
            counter += 1

        newLine.append(newWord)

    return " ".join(newLine)

def handleContinuousHashtags(line):
    match = re.search(r'(#( \[\+\]#)+)', line, re.IGNORECASE)
    if match:
        return line.replace(match.group(0), "#")
    return line

def handleEndOfWordHashtag(line):
    line = line.strip().split()
    for word in range(len(line)):
        match = re.search(r'[a-zA-Z0-9]+#$', line[word], re.IGNORECASE)
        if match:
            line[word] = line[word].replace("#", " #")
    return " ".join(line)

def handlePlus(line):

    line = line.strip().split(" ")
    newLine = ""
    hashLine = ""
    count = 0
    while count < len(line):
        twoPLusesMatch = re.search(r'(\[\+\])(\S+(\[\+\]))+', line[count], re.IGNORECASE)
        onePlusBefore = re.search(r'^(\[\+\])\S+', line[count], re.IGNORECASE) 
        onePlusAfter = re.search(r'\S+(\[\+\])$', line[count], re.IGNORECASE)
        
        # if there are more than one pluses in a  word 
        if twoPLusesMatch:
            newLine = newLine[:-1] + "[+]#[+]" + line[count + 1] + " "
            hashLine += line[count][3:-3] + " "
            count += 2
        
        elif onePlusBefore:
            newLine = newLine[:-1] + "[+]# "
            hashLine += line[count][3:] + " "
            count += 1
        
        elif onePlusAfter:
            newLine += "#[+]" + line[count + 1] + " "
            hashLine += line[count][:-3] + " "
            count += 2

        else:
            newLine += line[count] + " "
            count += 1


    print(hashLine)
    # hashFile.write(hashLine.strip() + "\n")
    return newLine.strip()


def handleTokenSeparation(gold):
    gold = gold.replace("[-]#", " [+]#")
    gold = preprocessor(gold)
    gold = handlePlus(gold)
    # gold = handleContinuousPluses(gold)
    # gold = handleContinuousHashtags(gold)
    # gold = handleEndOfWordHashtag(gold)
    return gold

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
            if "tag" in allWords[j].attrib and allWords[j].attrib["tag"] in ["punctuation"]:
                currGoldLine[wordsOfThisLineCounter] = "#"
            elif "tag" in allWords[j].attrib and allWords[j].attrib["tag"] in ["foreign"]:
                currGoldLine[wordsOfThisLineCounter] = handlePlus(changeForeignsToHash(preprocessor(allWords[j].text)))
            else:
                currGoldLine[wordsOfThisLineCounter] = handleTokenSeparation(currGoldLine[wordsOfThisLineCounter])

            wordsOfThisLineCounter += 1
        
        goldOutput.write(" ".join(currGoldLine) + "\n")
        tracker += numLines
        lineCounter += 1
        
arabiziOutput.close()
