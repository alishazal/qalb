"""
Usage: python3 combine-mle-seq2seq.py [mle.out] [mle-unknown.out] [seq2seq.out] [new.out]
"""

import sys

mle = open(sys.argv[1], "r").readlines()
mleUnknown = open(sys.argv[2], "r").readlines()
seq2seq = open(sys.argv[3], "r").readlines()
new = open(sys.argv[4], "w")

for line in range(len(mleUnknown)):
    currMleUnknownLine = mleUnknown[line].strip().split(" ")
    currMleLine = mle[line].strip().split(" ")
    currSeq2seqLine = seq2seq[line].strip().split(" ")

    newLine = []
    for word in range(len(currMleUnknownLine)):
        if word >= len(currSeq2seqLine):
            break
        if currMleUnknownLine[word] == "0":
            newLine.append(currMleLine[word])
        else:
            newLine.append(currSeq2seqLine[word])
    
    new.write(" ".join(newLine) + "\n")

new.close()