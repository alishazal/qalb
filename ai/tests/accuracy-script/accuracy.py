# import sys

# systemOutput = sys.argv[1]
# gold = sys.argv[2]
# arabizi = sys.argv[3]
# maxLength = int(sys.argv[4])

# systemOutputfile = open(systemOutput, "r")
# soLines = systemOutputfile.readlines()

# goldFile = open(gold, "r")
# gfLines = goldFile.readlines()

# arabiziFile = open(arabizi, "r")
# afLines = arabiziFile.readlines()

# correct = 0
# total = 0

# soCount = 0
# for i in range(len(afLines)):
#     if len(afLines[i]) > maxLength:
#         continue
    
#     currSysSentence = soLines[soCount].split()
#     currGoldSentence = gfLines[i].split()

#     soCount += 1

#     if len(currGoldSentence) != len(currSysSentence):
#         continue

#     for j in range(len(currGoldSentence)):
#         if currGoldSentence[j] == currSysSentence[j]:
#             correct += 1
#         total += 1

# print("Accuracy is:", (correct/total)*100)

# systemOutputfile.close()
# goldFile.close()
# arabiziFile.close()
