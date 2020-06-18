"""
Usage: python3 make-probability-vector-embeddings.py [english.arabizi] [arabizi.arabizi] [output]
"""

import sys
import time

english = open(sys.argv[1], "r").readlines()
arabizi = open(sys.argv[2], "r").readlines()
output = open(sys.argv[3], "w")

englishFlat = []
for line in english:
    englishFlat += line.strip().split()
englishUnique = list(set(englishFlat))

arabiziFlat = []
for line in arabizi:
    arabiziFlat += line.strip().split()
arabiziUnique = list(set(arabiziFlat))

print("Total unique words", len(englishUnique) + len(arabiziUnique))
print("All english words:", len(englishFlat))
print("All arabizi words:", len(arabiziFlat))

embeddings = {}
count = 1
start = time.time()
for word in englishUnique:
    if count % 500 == 0:
        print("Words read:", count)
        print("Time taken", time.time() - start, "seconds")
        start = time.time()

    if word not in embeddings:
        embeddings[word] = True
        englishCount = englishFlat.count(word)
        arabiziCount = arabiziFlat.count(word)
        total = englishCount + arabiziCount

        if englishCount == 0:
            englishProbability = 0.0
        else:
            englishProbability = englishCount / total
        
        if arabiziCount == 0:
            arabiziProbability = 0.0
        else:
            arabiziProbability = arabiziCount / total

        output.write(word + " " + str(arabiziProbability) + " " + str(englishProbability) + "\n")
    
    count += 1

for word in arabiziUnique:
    if count % 500 == 0:
        print("Words read:", count)
        print("Time taken", time.time() - start, "seconds")
        start = time.time()

    if word not in embeddings:
        embeddings[word] = True
        englishCount = englishFlat.count(word)
        arabiziCount = arabiziFlat.count(word)
        total = englishCount + arabiziCount

        if englishCount == 0:
            englishProbability = 0.0
        else:
            englishProbability = englishCount / total
        
        if arabiziCount == 0:
            arabiziProbability = 0.0
        else:
            arabiziProbability = arabiziCount / total

        output.write(word + " " + str(arabiziProbability) + " " + str(englishProbability) + "\n")

    count += 1

output.close()