"""
Usage: python3 investigate-hashtag.py [source] [system.out] [gold]
"""

import sys

source = open(sys.argv[1], "r").readlines()
output = open(sys.argv[2], "r").readlines()
gold = open(sys.argv[3], "r").readlines()

for line in range(len(output)):
    currSourceLine = source[line].strip().split(" ")
    currOutputLine = output[line].strip().split(" ")
    currGoldLine = gold[line].strip().split(" ")

    for word in range(len(currOutputLine)):
        if len(currOutputLine) != len(currSourceLine):
            continue
        currSourceWord = currSourceLine[word]
        currOutputWord = currOutputLine[word]
        currGoldWord = currGoldLine[word]

        if currOutputWord == "#" and currSourceWord != currGoldWord:
            print(currSourceWord, currGoldWord)