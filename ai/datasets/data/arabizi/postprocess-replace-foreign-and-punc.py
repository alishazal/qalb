"""
Usage: python3 postprocess-replace-foreign-and-punc.py [train.arabizi] [prediction.out] [source.arabizi] [new-prediction.out]
"""

import sys

train = open(sys.argv[1], "r")
trainLines = train.readlines()
output = open(sys.argv[2], "r")
outputLines = output.readlines()
source = open(sys.argv[3], "r")
sourceLines = source.readlines()
newOutput = open(sys.argv[4], "w")

for i in range(len(trainLines)):
    currTrainLine = trainLines[i].strip().split(" ")
    currOutputLine = outputLines[i].strip().split(" ")
    currSourceLine = sourceLines[i].strip().split(" ")

    for j in range(len(currTrainLine)):
        if currTrainLine[j] == "#" and j < len(currOutputLine):
            currOutputLine[j] = currSourceLine[j]
    
    newOutput.write(" ".join(currOutputLine) + "\n")

train.close()
output.close()
source.close()
newOutput.close()


