"""
python3 checkAlignment.py [file1] [file2]
"""

import sys

file1 = open(sys.argv[1], "r")
file2 = open(sys.argv[2], "r")

lineCount = 0
file2Lines = file2.readlines()

misalignCount = 0
for line in file1:
    if len(line.strip().split()) != len(file2Lines[lineCount].strip().split()):
        print(line, "\n", file2Lines[lineCount])
        misalignCount += 1
    
    lineCount +=1 

if misalignCount == 0:
    print("Files are aligned perfectly")
else:
    print("Files are misaligned at", misalignCount, "instances")

file1.close()
file2.close()
