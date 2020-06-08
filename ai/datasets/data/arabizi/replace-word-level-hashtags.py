"""
Usage: python3 replace-word-level-hashtags.py [source.arabizi] [file-with-hashtags.arabizi] [new-file.arabizi]
"""

import sys

source = open(sys.argv[1], "r")
sourceLines = source.readlines()
file = open(sys.argv[2], "r")
fileLines = file.readlines()
newFile = open(sys.argv[3], "w")

for i in range(len(fileLines)):
    currFileLine = fileLines[i].strip().split(" ")
    currSourceLine = sourceLines[i].strip().split(" ")
    for j in range(len(currFileLine)):
        if currFileLine[j] == "#" and j < len(currSourceLine):
            currFileLine[j] = currSourceLine[j]
    
    newFile.write(" ".join(currFileLine) + "\n")

source.close()
file.close()
newFile.close()