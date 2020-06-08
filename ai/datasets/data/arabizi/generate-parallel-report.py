"""
Usage: python3 generate-parallel-report.py [source] [first-initial-output.out] [second-initial-output.out] 
    [initial-output.gold] [first-intermediate-output.out] [second-intermediate-output.out] 
    [intermediate-output.gold] [first-final-output.out] [second-final-output.out] [final-output.gold] 
    [report.txt]
"""
import sys
import math

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


def hashtagAccuracy(system, gold):
    system = system.strip().split(" ")
    gold = gold.strip().split(" ")

    total = 0
    correct = 0

    for i in range(len(system)):
        if gold[i] == "#":
            if system[i] == "#":
                correct += 1
            total += 1

    return str(round((correct/total) * 100, 1))

def checkHashtagAlignmentFromSystem(system, gold):
    system = system.strip().split(" ")
    gold = gold.strip().split(" ")

    count = 0
    for i in range(len(gold)):
        if i < len(system) and system[i] == "#" and gold[i] != "#":
            count += 1
    
    return str(count)

def checkHashtagGenerationFailure(system, gold):
    system = system.strip().split(" ")
    gold = gold.strip().split(" ")

    count = 0
    for i in range(len(gold)):
        if i < len(system) and gold[i] == "#" and system[i] != "#":
            count += 1

    return str(count)

def difference(gold, line1, line2, report):
    line1 = line1.strip().split(" ")
    line2 = line2.strip().split(" ")
    gold = gold.strip().split(" ")

    diff1 = []
    diff2 = []
    goldList = []
    for word in range(len(line1)):
        if len(line1) != len(line2):
            return

        if line1[word] != line2[word]:
            diff1.append(line1[word])
            diff2.append(line2[word])
            goldList.append(gold[word])
    
    report.write("\t".expandtabs(13) + "Line2Line:\t".expandtabs(5) + ("\t".expandtabs(10)).join(diff1) + "\n")
    report.write("DIFFERENCE - "+ "Word2Word:\t".expandtabs(5) + ("\t".expandtabs(10)).join(diff2) + "\n")
    report.write("\t".expandtabs(13) + "Gold:     \t".expandtabs(5) + ("\t".expandtabs(10)).join(goldList) + "\n")


source = open(sys.argv[1], "r").readlines()
firstInitialArabizi = open(sys.argv[2], "r").readlines()
secondInitialArabizi = open(sys.argv[3], "r").readlines()
initialGold = open(sys.argv[4], "r").readlines()
firstIntermediateArabizi = open(sys.argv[5], "r").readlines()
secondIntermediateArabizi = open(sys.argv[6], "r").readlines()
intermediateGold = open(sys.argv[7], "r").readlines()
firstFinalArabizi = open(sys.argv[8], "r").readlines()
secondFinalArabizi = open(sys.argv[9], "r").readlines()
finalGold = open(sys.argv[10], "r").readlines()

report = open(sys.argv[11], "w")

report.write("``This report is a comparison of two files only for the lines in which\n the initial outputs of both files were NOT same.``\n\n")
report.write("Overall Line2Line Initial Accuracy: " + overallAccuracy(firstInitialArabizi, initialGold) + "\n")
report.write("Overall Word2Word Initial Accuracy: " + overallAccuracy(secondInitialArabizi, initialGold) + "\n")

report.write("Overall Line2Line Intermediate Accuracy: " + overallAccuracy(firstIntermediateArabizi, intermediateGold) + "\n")
report.write("Overall Word2Word Intermediate Accuracy: " + overallAccuracy(secondIntermediateArabizi, intermediateGold) + "\n")

report.write("{}\n\n".format("-" * 97))

for i in range(len(source)):

    if firstInitialArabizi[i] == secondInitialArabizi[i]:
        continue

    report.write(("Source: \t" + source[i]).expandtabs(30))

    report.write(("Line2LineInitialOut: \t" + firstInitialArabizi[i]).expandtabs(30))
    report.write(("Word2WordInitialOut: \t" + secondInitialArabizi[i]).expandtabs(30))
    report.write(("InitialGold: \t" + initialGold[i]).expandtabs(30))
    if "#" in firstInitialArabizi[i]:
        hashtagMisalignmentCount = checkHashtagAlignmentFromSystem(firstInitialArabizi[i], initialGold[i])
        if hashtagMisalignmentCount != "0":
            report.write("ERROR: Incorrect hashtag in Line2Line in" + hashtagMisalignmentCount + " place(s)\n")
    
    if "#" in secondInitialArabizi[i]:
        hashtagMisalignmentCount = checkHashtagAlignmentFromSystem(secondInitialArabizi[i], initialGold[i])
        if hashtagMisalignmentCount != "0":
            report.write("ERROR: Incorrect hashtag in Word2Word in " + hashtagMisalignmentCount + " place(s)\n")

    if "#" in initialGold[i]:
        hashtagGenerationFailureCount = checkHashtagGenerationFailure(firstInitialArabizi[i], initialGold[i])
        if hashtagGenerationFailureCount != "0":
            report.write("ERROR: Failed to generate hashtag in Line2Line in " + hashtagGenerationFailureCount + " place(s)\n")
        
        hashtagGenerationFailureCount = checkHashtagGenerationFailure(secondInitialArabizi[i], initialGold[i])
        if hashtagGenerationFailureCount != "0":
            report.write("ERROR: Failed to generate hashtag in Word2Word in " + hashtagGenerationFailureCount + " place(s)\n")

        if len(firstInitialArabizi[i].split(" ")) == len(initialGold[i].split(" ")):
            report.write("Line2Line Hashtag Accuracy: " + hashtagAccuracy(firstInitialArabizi[i], initialGold[i]) + "\n")

        if len(secondInitialArabizi[i].split(" ")) == len(initialGold[i].split(" ")):
            report.write("Word2Word Hashtag Accuracy: " + hashtagAccuracy(secondInitialArabizi[i], initialGold[i]) + "\n")

    if len(firstInitialArabizi[i].split(" ")) != len(initialGold[i].split(" ")):
        report.write("ERROR: Incorrect alignment in Line2Line intial output\n")
    else:
        initialAccuracy = accuracy(firstInitialArabizi[i], initialGold[i])
        intInitialAccuracy = round(int(float(initialAccuracy)), -1)
        report.write("Line2Line Initial Accuracy: " + initialAccuracy + "\n")

    if len(secondInitialArabizi[i].split(" ")) != len(initialGold[i].split(" ")):
        report.write("ERROR: Incorrect alignment in Word2Word intial output\n")
    else:
        initialAccuracy = accuracy(secondInitialArabizi[i], initialGold[i])
        intInitialAccuracy = round(int(float(initialAccuracy)), -1)
        report.write("Word2Word Initial Accuracy: " + initialAccuracy + "\n")
    report.write("\n")
    
    report.write(("Line2LineIntermediateOut: \t" + firstIntermediateArabizi[i]).expandtabs(30))
    report.write(("Word2WordIntermediateOut: \t" + secondIntermediateArabizi[i]).expandtabs(30))
    report.write(("IntermediateGold: \t" + intermediateGold[i]).expandtabs(30))
    if len(firstIntermediateArabizi[i].split(" ")) != len(intermediateGold[i].split(" ")):
        report.write("ERROR: Incorrect alignment in Line2Line intermediate output\n")
    else:
        intermediateAccuracy = accuracy(firstIntermediateArabizi[i], intermediateGold[i])
        intIntermediateAccuracy = round(int(float(intermediateAccuracy)), -1)
        report.write("Line2Line accuracy: " + intermediateAccuracy + "\n")

    if len(secondIntermediateArabizi[i].split(" ")) != len(intermediateGold[i].split(" ")):
        report.write("ERROR: Incorrect alignment in Word2Word intermediate output\n")
    else:
        intermediateAccuracy = accuracy(secondIntermediateArabizi[i], intermediateGold[i])
        intIntermediateAccuracy = round(int(float(intermediateAccuracy)), -1)
        report.write("Word2Word accuracy: " + intermediateAccuracy + "\n")
    difference(intermediateGold[i], firstIntermediateArabizi[i], secondIntermediateArabizi[i], report)
    report.write("\n")
    
    report.write(("Line2LineFinalOut: \t" + firstFinalArabizi[i]).expandtabs(30))
    report.write(("Word2WordFinalOut: \t" + secondFinalArabizi[i]).expandtabs(30))
    report.write(("FinalGold: \t" + finalGold[i]).expandtabs(30))
    if len(firstFinalArabizi[i].split(" ")) != len(finalGold[i].split(" ")):
        report.write("ERROR: Incorrect alignment in Line2Line final output\n")
        
    if len(secondFinalArabizi[i].split(" ")) != len(finalGold[i].split(" ")):
        report.write("ERROR: Incorrect alignment in Word2Word final output\n")

    report.write("\n")
    report.write("{}\n".format("-" * 40))

report.close()