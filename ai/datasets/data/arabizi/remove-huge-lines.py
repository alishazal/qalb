"""
Usage: python3 remove-huge-lines.py [orig-file] [new-file] [line-length-limit]
"""

import sys

orig = open(sys.argv[1], "r").readlines()
new = open(sys.argv[2], "w")
limit = int(sys.argv[3])

for line in orig:
    currLine = line.strip().split()

    bigWord = False
    for word in currLine:
        if len(word) >= limit:
            bigWord = True
            break
    
    if not bigWord:
        new.write(" ".join(currLine) + "\n")

new.close()