"""
Usage: python3 wb-tags.py [original-file] [new-file]
"""

import sys

orig = open(sys.argv[1], "r")
new = open(sys.argv[2], "w")

for line in orig:
    newLine = "<wb> "
    wordList = line.strip().split(" ")
    taggedLine = " <wb> ".join(wordList)
    newLine += taggedLine + " <wb> "

    new.write(newLine + "\n")

orig.close()
new.close()