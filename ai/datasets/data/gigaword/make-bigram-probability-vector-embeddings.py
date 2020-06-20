"""
Usage: python3 make-bigram-probability-vector-embeddings.py [english.arabizi] [arabizi.arabizi] [output]
"""

import sys
import time
import math

english = open(sys.argv[1], "r").readlines()
arabizi = open(sys.argv[2], "r").readlines()
output = open(sys.argv[3], "w")

englishBigrams = {}
englishBigramsCounter = 0
for line in english:
    line = line.strip().split()
    for word in range(1, len(line)):
        currBigram = (line[word - 1], line[word])
        if currBigram in englishBigrams:
            englishBigrams[currBigram] += 1
        else:
            englishBigrams[currBigram] = 1
        
        englishBigramsCounter += 1


arabiziBigrams = {}
arabiziBigramsCounter = 0
for line in arabizi:
    line = line.strip().split()
    for word in range(1, len(line)):
        currBigram = (line[word - 1], line[word])
        if currBigram in arabiziBigrams:
            arabiziBigrams[currBigram] += 1
        else:
            arabiziBigrams[currBigram] = 1

        arabiziBigramsCounter += 1

print("Total english bigrams:", englishBigramsCounter)
print("Total arabizi bigrams:", arabiziBigramsCounter)

embeddings = {}
count = 1
start = time.time()
for bigram in englishBigrams:
    if count % 10000 == 0:
        print("Bigrams processed:", count)
        start = time.time()

    if bigram not in embeddings:
        embeddings[bigram] = True
        englishCount = englishBigrams.get(bigram, 0)
        arabiziCount = arabiziBigrams.get(bigram, 0)
        total = englishCount + arabiziCount

        if englishCount == 0:
            englishProbability = -(math.log(0.000001, 10))
        else:
            englishProbability = -(math.log(englishCount / total, 10))
        
        if arabiziCount == 0:
            arabiziProbability = -(math.log(0.000001, 10))
        else:
            arabiziProbability = -(math.log(arabiziCount / total, 10))

        output.write(bigram[0] + " " + bigram[1] + " " + str(arabiziProbability) + " " + str(englishProbability) + "\n")
    
    count += 1

for bigram in arabiziBigrams:
    if count % 10000 == 0:
        print("Bigrams processed:", count)
        start = time.time()

    if bigram not in embeddings:
        embeddings[bigram] = True
        englishCount = englishBigrams.get(bigram, 0)
        arabiziCount = arabiziBigrams.get(bigram, 0)
        total = englishCount + arabiziCount

        if englishCount == 0:
            englishProbability = -(math.log(0.000001, 10))
        else:
            englishProbability = -(math.log(englishCount / total, 10))
        
        if arabiziCount == 0:
            arabiziProbability = -(math.log(0.000001, 10))
        else:
            arabiziProbability = -(math.log(arabiziCount / total, 10))

        output.write(bigram[0] + " " + bigram[1] + " " + str(arabiziProbability) + " " + str(englishProbability) + "\n")

    count += 1

output.close()