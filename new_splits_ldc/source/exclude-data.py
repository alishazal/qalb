"""
Usage: python3 exclude-data.py [big-source.arabizi] [data-to-exclude.arabizi] [new-big-source.arabizi]
"""

import sys

source = open(sys.argv[1], "r").readlines()
train = open(sys.argv[2], "r").readlines()
newSource = open(sys.argv[3], "w")

count = 1
for line in train:
    if count % 5000 == 0:
        print("Train lines read:", count)
    if line in source:
        source.remove(line)
    count += 1

count = 1
for line in source:
    if count % 5000 == 0:
        print("Lines written:", count)
    newSource.write(line.strip() + "\n")
    count += 1

newSource.close()