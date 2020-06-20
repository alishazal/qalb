"""
Usage: python3 make-unigram-probability-vector-embeddings.py [english.arabizi] [arabizi.arabizi] [output]
"""

import sys
import time
import math
from collections import Counter

english = open(sys.argv[1], "r").readlines()
arabizi = open(sys.argv[2], "r").readlines()
output = open(sys.argv[3], "w")

englishFlat = []
for line in english:
    englishFlat += line.strip().split()
englishUnique = list(set(englishFlat))
englishWords = Counter(englishFlat)

arabiziFlat = []
for line in arabizi:
    arabiziFlat += line.strip().split()
arabiziUnique = list(set(arabiziFlat))
arabiziWords = Counter(arabiziFlat)

print("Total unique words", len(englishUnique) + len(arabiziUnique))
print("All english words:", len(englishFlat))
print("All arabizi words:", len(arabiziFlat))

embeddings = {}
count = 1
start = time.time()
for word in englishUnique:
    if count % 10000 == 0:
        print("Words read:", count)
        start = time.time()

    if word not in embeddings:
        embeddings[word] = True
        englishCount = englishWords.get(word, 0)
        arabiziCount = arabiziWords.get(word, 0)
        total = englishCount + arabiziCount

        if englishCount == 0:
            englishProbability = -(math.log(0.000001, 10))
        else:
            englishProbability = -(math.log(englishCount / total, 10))
        
        if arabiziCount == 0:
            arabiziProbability = -(math.log(0.000001, 10))
        else:
            arabiziProbability = -(math.log(arabiziCount / total, 10))

        output.write(word + " " + str(arabiziProbability) + " " + str(englishProbability) + "\n")
    
    count += 1

for word in arabiziUnique:
    if count % 10000 == 0:
        print("Words read:", count)
        start = time.time()

    if word not in embeddings:
        embeddings[word] = True
        englishCount = englishWords.get(word, 0)
        arabiziCount = arabiziWords.get(word, 0)
        total = englishCount + arabiziCount

        if englishCount == 0:
            englishProbability = -(math.log(0.000001, 10))
        else:
            englishProbability = -(math.log(englishCount / total, 10))
        
        if arabiziCount == 0:
            arabiziProbability = -(math.log(0.000001, 10))
        else:
            arabiziProbability = -(math.log(arabiziCount / total, 10))

        output.write(word + " " + str(arabiziProbability) + " " + str(englishProbability) + "\n")

    count += 1

output.close()