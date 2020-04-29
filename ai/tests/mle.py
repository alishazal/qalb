"""
Usage: python3 mle.py [train.arabizi] [train.gold] [dev.arabizi] [pred.out]
"""
import sys

trainA = open(sys.argv[1], "r").readlines()
trainG = open(sys.argv[2], "r").readlines()
devA = open(sys.argv[3], "r").readlines()
pred = open(sys.argv[4], "w")

mle = {}
"""
mle = {
    "habibi": [["hAbibi", 2], ["habibi", 5]]
}
"""

# LEARN ALL WORDS
for line in range(len(trainA)):
    currArabiziLine = trainA[line].strip().split()
    currGoldLine = trainG[line].strip().split()

    # go over every word of line
    for word in range(len(currArabiziLine)):
        currWord = currArabiziLine[word]
        goldWord = currGoldLine[word]
        # check if the word exists in our dict i.e if it has been seen before
        if currWord in mle:
            found = False
            wordsList = mle[currWord]
            # check if the gold of that word has been seen before
            for i in range(len(wordsList)):
                if wordsList[i][0] == goldWord:
                    mle[currWord][i][1] += 1
                    found = True
                    break

            # if that gold is never seen, put it in our dict for the word we're looking at
            if not found:
                mle[currWord].append([goldWord , 1])
        
        # if arabizi word doesn't exist in our dict
        else:
            mle[currWord] = [[goldWord, 1]]

# MLE PART
for i in mle:
    mle[i].sort(key=lambda x: x[1], reverse=True)
    mle[i] = mle[i][0][0]

# DECODING PART
for line in range(len(devA)):
    currArabiziLine = devA[line].strip().split()
    ans = []

    for word in range(len(currArabiziLine)):
        currWord = currArabiziLine[word]
        if currWord in mle:
            ans.append(mle[currWord])
        else:
            ans.append(currWord)
    
    ans = " ".join(ans)
    pred.write(ans + "\n")

pred.close()