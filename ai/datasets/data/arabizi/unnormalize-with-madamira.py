"""
Usage: python3 unnormalize-with-madamira.py [mada-file] [output]
"""

import sys
import re

madaFile = open(sys.argv[1], "r")
outputFile = open(sys.argv[2], "w")

def removeDiacritics(line):
    for word in range(len(line)):
        newWord = ""
        for char in range(len(line[word])):
            if line[word][char] not in "aiuoFKN~`":
                newWord += line[word][char]
        line[word] = newWord
    return line

sentences = madaFile.read().split('SENTENCE BREAK')
for sentence in sentences:
    words = re.findall(r'diac:([^\s]+)', sentence)
    # removing svm_predictions
    words = words[1::2]
    words = removeDiacritics(words)
    outputFile.write(" ".join(words) + '\n')

madaFile.close()
outputFile.close()