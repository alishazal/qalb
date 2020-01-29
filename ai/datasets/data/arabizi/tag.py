import sys

arabizi = sys.argv[1]
arabiziFile = open(arabizi, "r")
afLines = arabiziFile.readlines()

gold = sys.argv[2]
goldFile = open(gold, "r")
gfLines = goldFile.readlines()

newArabiziFile = open(sys.argv[3], "w")
newGoldFile = open(sys.argv[4], "w")


# Making tagged version of arabizi file
for line in afLines:
    line = line.strip()
    line = line.split()

    wordCtr = 0
    for word in line:
        newLine = []

        # if wordCtr == 0:
        #     newline += "<bos><bow>" + word + "<eow>"
        
        for i in [-2, -1, 0, 1, 2]:
            if wordCtr + i >= 0 and wordCtr + i < len(line):
                if wordCtr + i  == 0:
                    newLine.append("<bos>")
            
                if i == 0:
                    newLine.extend(["<bow>", word, "<eow>"])
                elif len(newLine) != 0 and newLine[-1] not in ["<bow>", "<eow>", "<bos>", "<eos>"]:
                    newLine.extend(["<s>", line[wordCtr + i]])
                else:
                    newLine.append(line[wordCtr + i])

                if wordCtr + i == len(line) - 1:
                    newLine.append("<eos>")

        strLine = ''.join(newLine) + "\n"
        newArabiziFile.write(strLine)
        wordCtr += 1

# Making single word per line version of gold file
for line in gfLines:
    line = line.strip()
    line = line.split()
    for word in line:
        newGoldFile.write(word + "\n")
        print(word)

arabiziFile.close()
goldFile.close()
newArabiziFile.close()
newGoldFile.close()