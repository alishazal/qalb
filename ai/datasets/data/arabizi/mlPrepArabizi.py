"""
Usage: python3 mlPrepArabizi.py [old.arabizi] [new.arabizi]

Function -> MLprepArabizi(source):
    > lowercase all letters
    > accented letter => unaccented
    > compression: repetitions over 2 => reduced to 2
    > non-ascii characters => # (this converts arabic, graphic emojis and other foreign language chars to #)
    > text emoji /e.g. :) :P :-)/ => #
    > punctuations => #
    > Emojis and punctuations attached to a word are kept as they are
"""

import sys
import unicodedata as ud
import re

def allNonAscii(word):
    for char in word:
        if ord(char) < 128:
            return False
    
    return True

def changeNonAsciiToHash(line):

    words = line.split()
    
    for i in range(len(words)):
        if allNonAscii(words[i]):
            words[i] = "#"

    return " ".join(words)

def isPunctuation(word):
    for char in word:
        if char not in ".,?!'\":;-()[]}{":
            return False

    return True

def changeTextEmojiAndPuncToHash(line):

    words = line.split()
    
    for i in range(len(words)):
        if isPunctuation(words[i]):
            words[i] = "#"

        else:
            # Handling <3 separately first
            match = re.search(r'(<3)+', words[i], re.IGNORECASE)
            if match and match.group(0) == words[i]:
                words[i] = "#"

            match = re.search(r'[=:;8xX>^()$*@][-_.\'"]*[XxOoPpsSDVv)(\][/\\Cc3><}{@|:;=0*L$^~]+', words[i], re.IGNORECASE) 
            if match:
                emoticon = match.group(0)
                if emoticon == words[i]:
                    words[i] = "#"


    return " ".join(words)

        
def removeAccents(line):
    
    newLine = []
    for word in line.split(" "):
        nfkd_form = ud.normalize('NFKD', word)
        res = "".join([c for c in nfkd_form if not ud.combining(c)])
        newLine.append(res.replace(' ', ''))
    return " ".join(newLine)

def compress(line, limit):

    ans = ""
    currChar = ""
    currCharCounter = 1

    compressThese = '23567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_ '

    for i in line:
        if i == currChar:
            currCharCounter += 1
        else:
            currChar = i
            currCharCounter = 1
            
        if currCharCounter < limit + 1 or i not in compressThese:
            ans += i
    
    return ans

def mlPrep(line):

    line = line.strip()
    line = compress(line, 2)
    line = line.lower()
    line = removeAccents(line)
    line = changeNonAsciiToHash(line)
    line = changeTextEmojiAndPuncToHash(line)
    return line

rawFile = open(sys.argv[1], "r")
newFile = open(sys.argv[2], "w")

count = 1
for line in rawFile:
    if count % 10000 == 0:
        print("Lines processed:", count)

    newLine = mlPrep(line)
    newFile.write(newLine + "\n")
    
    count += 1

rawFile.close()
newFile.close()