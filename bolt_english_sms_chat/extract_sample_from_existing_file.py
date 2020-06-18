"""
Usage: python3 extract_sample_from_existing_file.py [file-name.english] [new-file.english] [sample-size]
"""

import sys
import random
random.seed(1)

def getNoOfWordsInList(l):
    count = 0
    for line in l:
        count += len(line.strip().split())

    return count

orig = open(sys.argv[1], "r").readlines()
new = open(sys.argv[2], "w")
sampleSize = int(sys.argv[3])

#Taking out a sample of data
print("Now sampling data")
sampledOrigLines = orig
noOfSampledLines = len(orig)
noOfSampledWords = getNoOfWordsInList(sampledOrigLines)
while noOfSampledWords > sampleSize:
    currSample = random.sample(sampledOrigLines, noOfSampledLines)
    noOfSampledWords = getNoOfWordsInList(currSample)
    if noOfSampledLines > 5000:
        noOfSampledLines -= 5000
    else:
        noOfSampledLines -= 100

print("Sampling completed. Writing to file")
for line in currSample:
    new.write(line.strip() + "\n")
        
new.close()