"""
Usage: python3 mlPrepArabizi.py [raw.arabizi] [new.arabizi]
Example: python3 mlPrepArabizi.py source/bolt-ldc-source-no-dev-test.arabizi source/bolt-ldc-source-ml-ready.arabizi

Function -> MLprepArabizi(source):
    > accented letter => unaccented
    > non-ascii characters => # (this converts arabic, graphic emojies and other foreign language chars to #)
    > text emoji /e.g. :) :P :-)/ => #
    > separate punctuations from words and add [+]
    > punctuations become hashtags
    > repetitions over 2 => reduced to 2
"""

import sys
import unicodedata as ud

def changeNonAsciiToHash(line):
    newLine = ""
    for char in line:
        # if ((0x00600 <= ord(char) <= 0x006FF) or (0x00750 <= ord(char) <= 0x0077F) or (0x008A0 <= ord(char) <= 0x008FF)
        # or (0x0FB50 <= ord(char) <= 0x0FDFF) or (0x0FE70 <= ord(char) <= 0x0FEFF) or (0x10E60 <= ord(char) <= 0x10E7F)
        # or (0x1EC70 <= ord(char) <= 0x1ECBF) or (0x1ED00 <= ord(char) <= 0x1ED4F) or (0x1EE00 <= ord(char) <= 0x1EEFF)
        # or (ud.category(char) == "So") or (ud.category(char) == "Co") or (ord(char) in range(0x1F3Fb, 0x1F400))):
        if ord(char) > 127:
            newLine += "#"

        else:
            newLine += char

    return newLine
        
def removeAccents(line):
    nfkd_form = ud.normalize('NFKD', line)
    return "".join([c for c in nfkd_form if not ud.combining(c)])

# repeatingCharacterDict = {}
# def recordLetterRepetitions(repeatingChar):
#     for i in repeatingChar:
#         if i in repeatingCharacterDict:
#             repeatingCharacterDict[i] += 1
#         else:
#             repeatingCharacterDict[i] = 1

# whichCategory = {
#     "vowelsOnly": 0,
#     "consonantsOnly": 0,
#     "digitsOnly": 0,
#     "mix": 0
# }
def compress(l, file):

    ans = ""
    currChar = ""
    currCharCounter = 1

    compressThese = '23567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_ '
    repeat = ""
    degree = 0
    for i in l:
        if i == currChar:
            currCharCounter += 1
        else:
            currChar = i
            currCharCounter = 1
            
        if currCharCounter < 3 or i not in compressThese:
            ans += i
        # else:
        #     if i not in repeat:
        #         repeat += i
        #     if currCharCounter > degree:
        #         degree = currCharCounter

    # # Checking number of vowels, consonants and digits in repeated letters
    # vowels = "aeiouAEIOU"
    # digits = "1234567890"
    # vowelCount = 0
    # consonantCount = 0
    # digitCount = 0
    # for letter in repeat:
    #     if letter in vowels:
    #         vowelCount += 1
    #     elif letter in digits:
    #         digitCount += 1
    #     else:
    #         consonantCount += 1

    # # Checking category that the repeated letters belong to
    # if vowelCount != 0 and consonantCount == 0 and digitCount == 0:
    #     category = "Vowels Only"
    #     whichCategory["vowelsOnly"] += 1
    # elif vowelCount == 0 and consonantCount != 0 and digitCount == 0:
    #     category = "Consonants Only"
    #     whichCategory["consonantsOnly"] += 1
    # elif vowelCount == 0 and consonantCount == 0 and digitCount != 0:
    #     category = "Digits Only"
    #     whichCategory["digitsOnly"] += 1
    # else:
    #     category = "Mix"
            
    # if ans != l:
    #     if category == "Mix": whichCategory["mix"] += 1
    #     recordLetterRepetitions(repeat)
    #     file.write(l + "\t" + repeat + "\t" + str(degree) + "\t" + category + "\t" + ans + "\n")

    return ans

def mlPrep(line):
    # line = line.lower()
    line = line.strip()
    line = removeAccents(line)
    line = changeNonAsciiToHash(line)
    return compress(line)

rawFile = open(sys.argv[1], "r")
newFile = open(sys.argv[2], "w")
# speechEffect = open("bolt-ldc-list-of-speech-effect-words.tsv", "w")
# speechEffect.write("Source\tRepeating-Letter(s)\tMax-Degree-of-Repetition-In-Line\tCategory\tTwo-Letter-Compression\n")

count = 1
for line in rawFile:
    if count % 10000 == 0:
        print("Lines processed:", count)

    newLine = mlPrep(line)
    newFile.write(newLine + "\n")
    
    count += 1

# repeatingLettersList = []
# for letter in repeatingCharacterDict:
#     currLetter = [letter, repeatingCharacterDict[letter]]
#     repeatingLettersList.append(currLetter)

# repeatingLettersList.sort(key = lambda l: l[1] ,reverse = True)
# print(repeatingLettersList)
# print(whichCategory)

rawFile.close()
newFile.close()
# speechEffect.close()