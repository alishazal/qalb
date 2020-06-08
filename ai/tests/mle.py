"""
Usage: python3 mle.py [train.arabizi] [train.gold] [dev.arabizi] [dev-source.arabizi] [pred.out] [unknown.out] [in-vocab-number]
"""
import sys

trainA = open(sys.argv[1], "r").readlines()
trainG = open(sys.argv[2], "r").readlines()
devA = open(sys.argv[3], "r").readlines()
devS = open(sys.argv[4], "r").readlines()
pred = open(sys.argv[5], "w")

# Unknown words file is created to help in combining seq2seq with mle
unknown = open(sys.argv[6], "w")

inVocabNum = int(sys.argv[7])

def postprocess(line):
    for word in range(1, len(line)):
        if line[word] == "#" and "[+]" in line[word - 1]:
            line[word - 1] = line[word - 1].replace("[+]", "")
    
    return line

mle = {}
inVocabulary = {}
"""
mle = {
    "habibi": [["hAbibi", 2], ["habibi", 5]]
}
"""

# TRAINING
for line in range(len(trainA)):
    currArabiziLine = trainA[line].strip().split()
    currGoldLine = trainG[line].strip().split()

    # go over every word of line
    for word in range(len(currArabiziLine)):
        currWord = currArabiziLine[word]
        goldWord = currGoldLine[word]
        # check if the word exists in our dict i.e if it has been seen before
        if currWord in mle:
            inVocabulary[currWord] += 1
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
            inVocabulary[currWord] = 1

# Keeping the highest frequency gold for each arabizi word
for i in mle:
    mle[i].sort(key=lambda x: x[1], reverse=True)
    mle[i] = mle[i][0][0]

# DECODING PART
unknownWordCounter = 0
totalWords = 0
for line in range(len(devA)):
    currArabiziLine = devA[line].strip().split()
    currArabiziSourceLine = devS[line].strip().split()
    ans = []
    unk = []

    for word in range(len(currArabiziLine)):
        currWord = currArabiziLine[word]
        currSourceWord = currArabiziSourceLine[word]
        if currWord in mle and inVocabulary[currWord] >= inVocabNum:
            ans.append(mle[currWord])
            unk.append("0")
        else:
            unknownWordCounter += 1
            ans.append(currSourceWord)
            unk.append("1")
        
        totalWords += 1
    
    ans = postprocess(ans)
    ans = " ".join(ans)
    pred.write(ans + "\n")
    unknown.write(" ".join(unk) + "\n")

pred.close()
unknown.close()

print("Total words:", totalWords)
print("No. of unkown words:", unknownWordCounter)