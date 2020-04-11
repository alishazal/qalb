"""
Usage: python3 sourcePreprocess.py [raw.arabizi] [preprocessed.arabizi]
Example: python3 sourcePreprocess.py source/bolt-ldc-source-no-dev-test.arabizi source/bolt-ldc-source-preprocessed.arabizi

Function -> sourcePreprocess(source):
    > separate punctuations from words and add [+]
    > dont touch digit
    > dont touch digits that are with punctuations such as 15-15-15, 12.6, etc
"""

import sys
import re
import unicodedata as ud

def isPunctuation(char, position):

    if position == "opening":
        if char in "'\"-([{":
            return True
        else:    
            return False
    else:
        if char in ".,?!'\":;-()[]}{=":
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
            if not isPunctuation(word[i], "opening"): #As soon as the first non-punctuation char is encountered, put the separation mark [+]
                word = word[:i] + "[+] " + word[i:] 
                break

    if isPunctuation(lastChar, "closing"): #If the last char of word is a punctiation 
        for i in range(len(word)-1, -1, -1): #Go over the word backwards
            if not isPunctuation(word[i], "closing"): #As soon as the first non-punctuation char is encountered, put the separation mark [+]
                word = word[:i+1] + " [+]" + word[i+1:]    
                break
    
    else: # If last char is not punc (for example it is :D, :P, etc)
        #match for text emoticons like :D :-) ;) etc
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

rawFile = open(sys.argv[1], "r")    
preprocessedFile = open(sys.argv[2], "w")

count = 1
for line in rawFile:
    if count % 10000 == 0:
        print("Lines processed:", count)

    preprocessedLine = preprocessor(line)
    preprocessedFile.write(preprocessedLine + "\n")
    
    count += 1

rawFile.close()
preprocessedFile.close()