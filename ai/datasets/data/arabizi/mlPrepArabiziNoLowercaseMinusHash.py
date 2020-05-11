"""
Usage: python3 mlPrepArabizi.py [old.arabizi] [new.arabizi]

Function -> MLprepArabizi(source):
    > accented letter => unaccented
    > compression: repetitions over 2 => reduced to 2
"""

import sys
import unicodedata as ud
import re
    
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
    line = removeAccents(line)
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