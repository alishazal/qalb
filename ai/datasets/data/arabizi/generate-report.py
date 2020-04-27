"""
Usage: python3 generate-report.py [source] [initial-output.out] [initial-output.gold] 
        [intermediate-output.out] [intermediate-output.gold] [final-output.out] 
        [final-output.gold] [report.txt]
"""
import sys
import math

def countAlignedLines(system, gold):
    count = 0
    for i in range(len(system)):
        if len(system[i].split()) == len(gold[i].split()):
            count += 1
    return count

def countUnalignedLines(system, gold):
    count = 0
    for i in range(len(system)):
        if len(system[i].split()) != len(gold[i].split()):
            count += 1
    return count

def overallAccuracyOfUnalignedLines(system, gold):
    correct = 0
    total = 0

    for i in range(len(system)):
        currPredLine = system[i].split(" ")
        currGoldLine = gold[i].split(" ")
        
        if len(currPredLine) > len(currGoldLine):
            for j in range(len(currPredLine)):
                if j < len(currGoldLine) and currPredLine[j] == currGoldLine[j]:
                    correct += 1
                total += 1
        elif len(currPredLine) < len(currGoldLine):
            for j in range(len(currGoldLine)):
                if j < len(currPredLine) and currPredLine[j] == currGoldLine[j]:
                    correct += 1
                total += 1

    return str(round((correct/total) * 100, 1))

def overallAccuracyOfAlignedLines(system, gold):
    correct = 0
    total = 0

    for i in range(len(system)):
        currPredLine = system[i].split(" ")
        currGoldLine = gold[i].split(" ")

        if len(currPredLine) == len(currGoldLine):
            for j in range(len(currPredLine)):
                if currPredLine[j] == currGoldLine[j]:
                    correct += 1
                total += 1

    return str(round((correct/total) * 100, 1))

def overallAccuracy(system, gold):
    correct = 0
    total = 0

    for i in range(len(system)):
        currPredLine = system[i].split(" ")
        currGoldLine = gold[i].split(" ")

        if len(currPredLine) == len(currGoldLine):
            for j in range(len(currPredLine)):
                if currPredLine[j] == currGoldLine[j]:
                    correct += 1
                total += 1
        
        elif len(currPredLine) > len(currGoldLine):
            for j in range(len(currPredLine)):
                if j < len(currGoldLine) and currPredLine[j] == currGoldLine[j]:
                    correct += 1
                total += 1
        else:
            for j in range(len(currGoldLine)):
                if j < len(currPredLine) and currPredLine[j] == currGoldLine[j]:
                    correct += 1
                total += 1

    return str(round((correct/total) * 100, 1))

def accuracy(system, gold):
    system = system.strip().split(" ")
    gold = gold.strip().split(" ")
    
    total = 0
    correct = 0
    for i in range(len(system)):
        if system[i] == gold[i]:
            correct += 1
        total += 1

    return str(round((correct/total) * 100, 1))

globalHashtagTotal = 0
globalHashtagCorrect = 0
def hashtagAccuracy(system, gold):
    global globalHashtagTotal
    global globalHashtagCorrect

    system = system.strip().split(" ")
    gold = gold.strip().split(" ")

    total = 0
    correct = 0

    for i in range(len(system)):
        if gold[i] == "#":
            if system[i] == "#":
                correct += 1
                globalHashtagCorrect += 1
            total += 1
            globalHashtagTotal += 1

    return str(round((correct/total) * 100, 1))

def checkHashtagAlignmentFromSystem(system, gold):
    system = system.strip().split(" ")
    gold = gold.strip().split(" ")

    count = 0
    for i in range(len(system)):
        if system[i] == "#" and gold[i] != "#":
            count += 1
    
    return str(count)

def checkHashtagGenerationFailure(system, gold):
    system = system.strip().split(" ")
    gold = gold.strip().split(" ")

    count = 0
    for i in range(len(system)):
        if gold[i] == "#" and system[i] != "#":
            count += 1

    return str(count)

def prettyBins(dict):
    listOfAccuracies = list(dict.keys())
    listOfAccuracies.sort()

    for acc in listOfAccuracies:
        print(("|" + str(acc) + "%|" + "\t").expandtabs(10), end = "")
    print()

    for acc in listOfAccuracies:
        print(("|" + str(dict[acc]) + "|" + "\t").expandtabs(10), end = "")
    print()

def lineBreakdown(ia, ig, inta, intg, fa, fg, groupsOf):
    totalLines = len(ia)
    numberOfGroupsOfThousands = totalLines // groupsOf

    count = 0
    for i in range(numberOfGroupsOfThousands):
        print("Accuracy of {}-{} lines: Initial {}, Intermediate {}, Final {}"
        .format(count, count + groupsOf, overallAccuracy(ia[count:count+groupsOf+1], ig[count:count+groupsOf+1]),
        overallAccuracy(inta[count:count+groupsOf+1], intg[count:count+groupsOf+1]), 
        overallAccuracy(fa[count:count+groupsOf+1], fg[count:count+groupsOf+1])))

        count += groupsOf

    print("Accuracy of {}-{} lines: Initial {}, Intermediate {}, Final {}"
        .format(count, totalLines, overallAccuracy(ia[count:totalLines], ig[count:totalLines]),
        overallAccuracy(inta[count:totalLines], intg[count:totalLines]), 
        overallAccuracy(fa[count:totalLines], fg[count:totalLines])))
    # Dont forget to check the last 504 lines

source = open(sys.argv[1], "r").readlines()
initialArabizi = open(sys.argv[2], "r").readlines()
initialGold = open(sys.argv[3], "r").readlines()
intermediateArabizi = open(sys.argv[4], "r").readlines()
intermediateGold = open(sys.argv[5], "r").readlines()
finalArabizi = open(sys.argv[6], "r").readlines()
finalGold = open(sys.argv[7], "r").readlines()

report = open(sys.argv[8], "w")
incorrectHashtag = 0
hashtagFailure = 0
incorrectInitialAlignment = 0
incorrectIntermediateAlignment = 0
incorrectFinalAlignment = 0
initialAccuracyBin = {}
intermediateAccuracyBin = {}
finalAccuracyBin = {}

for i in range(len(source)):
    report.write(("Source: \t" + source[i]).expandtabs(20))
    report.write(("InitialOut: \t" + initialArabizi[i]).expandtabs(20))
    report.write(("InitialGold: \t" + initialGold[i]).expandtabs(20))
    
    report.write(("IntermediateOut: \t" + intermediateArabizi[i]).expandtabs(20))
    report.write(("IntermediateGold: \t" + intermediateGold[i]).expandtabs(20))
    
    report.write(("FinalOut: \t" + finalArabizi[i]).expandtabs(20))
    report.write(("FinalGold: \t" + finalGold[i]).expandtabs(20))

    if "#" in initialArabizi[i]:
        hashtagMisalignmentCount = checkHashtagAlignmentFromSystem(initialArabizi[i], initialGold[i])
        if hashtagMisalignmentCount != "0":
            report.write("ERROR: Incorrect hashtag in " + hashtagMisalignmentCount + " place(s)\n")
            incorrectHashtag += 1

    if "#" in initialGold[i]:
        hashtagGenerationFailureCount = checkHashtagGenerationFailure(initialArabizi[i], initialGold[i])
        if hashtagGenerationFailureCount != "0":
            report.write("ERROR: Failed to generate hashtag in " + hashtagGenerationFailureCount + " place(s)\n")
            hashtagFailure += 1

        if len(initialArabizi[i].split(" ")) == len(initialGold[i].split(" ")):
            report.write("Hashtag Accuracy: " + hashtagAccuracy(initialArabizi[i], initialGold[i]) + "\n")

    if len(initialArabizi[i].split(" ")) != len(initialGold[i].split(" ")):
        report.write("ERROR: Incorrect alignment in intial output\n")
        incorrectInitialAlignment += 1
    else:
        initialAccuracy = accuracy(initialArabizi[i], initialGold[i])
        intInitialAccuracy = round(int(float(initialAccuracy)), -1)
        if intInitialAccuracy in initialAccuracyBin:
            initialAccuracyBin[intInitialAccuracy] += 1
        else:
            initialAccuracyBin[intInitialAccuracy] = 1
        report.write("Initial accuracy: " + initialAccuracy + "\n")

    if len(intermediateArabizi[i].split(" ")) != len(intermediateGold[i].split(" ")):
        incorrectIntermediateAlignment += 1
        report.write("ERROR: Incorrect alignment in intermediate output\n")
    else:
        intermediateAccuracy = accuracy(intermediateArabizi[i], intermediateGold[i])
        intIntermediateAccuracy = round(int(float(intermediateAccuracy)), -1)
        if intIntermediateAccuracy in intermediateAccuracyBin:
            intermediateAccuracyBin[intIntermediateAccuracy] += 1
        else:
            intermediateAccuracyBin[intIntermediateAccuracy] = 1
        report.write("Intermediate accuracy: " + intermediateAccuracy + "\n")

    if len(finalArabizi[i].split(" ")) != len(finalGold[i].split(" ")):
        incorrectFinalAlignment += 1
        report.write("ERROR: Incorrect alignment in final output\n")
    else:
        finalAccuracy = accuracy(finalArabizi[i], finalGold[i])
        intFinalAccuracy = round(int(float(finalAccuracy)), -1)
        if intFinalAccuracy in finalAccuracyBin:
            finalAccuracyBin[intFinalAccuracy] += 1
        else:
            finalAccuracyBin[intFinalAccuracy] = 1

        report.write("Final accuracy: " + finalAccuracy + "\n")

    report.write("\n")

report.close()


print("\tInitial Accuracy Bins".expandtabs(35))
prettyBins(initialAccuracyBin)
print("\tIntermediate Accuracy Bins".expandtabs(35))
prettyBins(initialAccuracyBin)
print("\tFinal Accuracy Bins".expandtabs(35))
prettyBins(finalAccuracyBin)
print()
lineBreakdown(initialArabizi, initialGold, intermediateArabizi, intermediateGold, finalArabizi, finalGold, 1000)
print()
print("Accuracy of {} aligned lines: {}".format(countAlignedLines(finalArabizi, finalGold), overallAccuracyOfAlignedLines(finalArabizi, finalGold)))
print("Accuracy of {} unaligned lines: {}".format(countUnalignedLines(finalArabizi, finalGold), overallAccuracyOfUnalignedLines(finalArabizi, finalGold)))
print()
print("Overall Initial Accuracy: " + overallAccuracy(initialArabizi, initialGold))
print("Overall Intermediate Accuracy: " + overallAccuracy(intermediateArabizi, intermediateGold))
print("Overall Final Accuracy: " + overallAccuracy(finalArabizi, finalGold))
print("Overall Hashtag Accuracy: " + str(round((globalHashtagCorrect/globalHashtagTotal)*100, 1)))
print()
print("Total incorrect hashtag errors: " + str(incorrectHashtag))
print("Total missing hashtags: " + str(hashtagFailure))
print("Total incorrect initial alignment errors: " + str(incorrectInitialAlignment))
print("Total incorrect intermediate alignment errors: " + str(incorrectIntermediateAlignment))
print("Total incorrect final alignment errors: " + str(incorrectFinalAlignment))
print("{}\n".format("-" * 97))