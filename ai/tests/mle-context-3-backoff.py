"""
Usage: python3 mle-context-3-backoff.py [train.arabizi] [train.gold] [dev.arabizi] [pred.out] [unknown.out]
"""
import sys
import time

trainA = open(sys.argv[1], "r").readlines()
trainG = open(sys.argv[2], "r").readlines()
devA = open(sys.argv[3], "r").readlines()
pred = open(sys.argv[4], "w")

# Unknown words file is created to help in combining seq2seq with mle
unknown = open(sys.argv[5], "w")

def postprocess(line):
    for word in range(1, len(line)):
        if line[word] == "#" and "[+]" in line[word - 1]:
            line[word - 1] = line[word - 1].replace("[+]", "")
    
    return line

def checkWord(d, word, gold):
    # check if the word exists in our dict i.e if it has been seen before
    if word in d:
        found = False
        wordsList = d[word]
        # check if the gold of that word has been seen before
        for i in range(len(wordsList)):
            if wordsList[i][0] == gold:
                d[word][i][1] += 1
                found = True
                break

        # if that gold is never seen, put it in our dict for the word we're looking at
        if not found:
            d[word].append([gold , 1])
    
    # if arabizi word doesn't exist in our dict
    else:
        d[word] = [[gold, 1]]

    return d

def keepHighestFrequency(d):
    for i in d:
        d[i].sort(key=lambda x: x[1], reverse=True)
        d[i] = d[i][0][0]
    return d

mleNoContext = {}
mleMinusOne = {}
mlePlusOne = {}
mlePlusMinusOne = {}
mlePlusMinusTwo = {}
mlePlusMinusThree = {}

"""
mle = {
    "habibi": [["hAbibi", 2], ["habibi", 5]]
}
"""

trainStartTime = time.time()
# TRAINING
for line in range(len(trainA)):
    currArabiziLine = ["<bos>", "<bos>", "<bos>"] + trainA[line].strip().split() + ["<eos>", "<eos>", "<eos>"]
    currGoldLine = trainG[line].strip().split()

    count = 0
    # go over every word of line
    for word in range(3, len(currArabiziLine) - 3):
        currWord = currArabiziLine[word]
        goldWord = currGoldLine[count]
        
        mleNoContext = checkWord(mleNoContext, currWord, goldWord)
        mleMinusOne = checkWord(mleMinusOne, (currArabiziLine[word-1], currWord), goldWord)
        mlePlusOne = checkWord(mlePlusOne, (currWord, currArabiziLine[word+1]), goldWord)
        mlePlusMinusOne = checkWord(mlePlusMinusOne, (currArabiziLine[word-1], currWord, currArabiziLine[word+1]), goldWord)
        mlePlusMinusTwo = checkWord(mlePlusMinusTwo, (currArabiziLine[word-2], currArabiziLine[word-1], currWord, currArabiziLine[word+1], currArabiziLine[word+2]), goldWord)
        mlePlusMinusThree = checkWord(mlePlusMinusThree, (currArabiziLine[word-3], currArabiziLine[word-2], currArabiziLine[word-1], currWord, currArabiziLine[word+1], currArabiziLine[word+2], currArabiziLine[word+3]), goldWord)
        count += 1
        

# Keeping the highest frequency gold for each arabizi word
mleNoContext = keepHighestFrequency(mleNoContext)
mleMinusOne = keepHighestFrequency(mleMinusOne)
mlePlusOne = keepHighestFrequency(mlePlusOne)
mlePlusMinusOne = keepHighestFrequency(mlePlusMinusOne)
mlePlusMinusTwo = keepHighestFrequency(mlePlusMinusTwo)
mlePlusMinusThree = keepHighestFrequency(mlePlusMinusThree)

print("Training time is:", time.time() - trainStartTime, "seconds")

# DECODING PART
decodeStartTime = time.time()
unknownWordCounter = 0
totalWords = 0
for line in range(len(devA)):
    currArabiziLine = ["<bos>", "<bos>", "<bos>"] + devA[line].strip().split() + ["<eos>", "<eos>", "<eos>"]
    ans = []
    unk = []

    for word in range(3, len(currArabiziLine) - 3):
        currWord = currArabiziLine[word]
        currWordMinusOne = (currArabiziLine[word-1], currWord)
        currWordPlusOne = (currWord, currArabiziLine[word+1])
        currWordPlusMinusOne = (currArabiziLine[word-1], currWord, currArabiziLine[word+1])
        currWordPlusMinusTwo = (currArabiziLine[word-2], currArabiziLine[word-1], currWord, currArabiziLine[word+1], currArabiziLine[word+2])
        currWordPlusMinusThree = (currArabiziLine[word-3], currArabiziLine[word-2], currArabiziLine[word-1], currWord, currArabiziLine[word+1], currArabiziLine[word+2], currArabiziLine[word+3])

        if currWordPlusMinusThree in mlePlusMinusThree:
            ans.append(mlePlusMinusThree[currWordPlusMinusThree])
            unk.append("0")

        elif currWordPlusMinusTwo in mlePlusMinusTwo:
            ans.append(mlePlusMinusTwo[currWordPlusMinusTwo])
            unk.append("0")

        elif currWordPlusMinusOne in mlePlusMinusOne:
            ans.append(mlePlusMinusOne[currWordPlusMinusOne])
            unk.append("0")
        
        elif currWordMinusOne in mleMinusOne:
            ans.append(mleMinusOne[currWordMinusOne])
            unk.append("0")

        elif currWordPlusOne in mlePlusOne:
            ans.append(mlePlusOne[currWordPlusOne])
            unk.append("0")

        elif currWord in mleNoContext:
            ans.append(mleNoContext[currWord])
            unk.append("0")
        else:
            ans.append("#")
            unk.append("1")
            unknownWordCounter += 1

        totalWords += 1
    
    ans = postprocess(ans)
    ans = " ".join(ans)
    pred.write(ans + "\n")
    unknown.write(" ".join(unk) + "\n")

print("Decoding time is", time.time() - decodeStartTime, "seconds")

pred.close()
unknown.close()

print("Total words:", totalWords)
print("No. of unkown words:", unknownWordCounter)