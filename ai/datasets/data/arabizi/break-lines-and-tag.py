# """
# Usage: python3 break-lines-and-tag.py [original.arabizi] [original.gold] [newArabizi.arabizi] [new.gold] [new.lines] [chunk-length]
# """

# import sys

# origArabizi = open(sys.argv[1], "r").readlines()
# origGold = open(sys.argv[2], "r").readlines()
# newArabizi = open(sys.argv[3], "w")
# newGold = open(sys.argv[4], "w")
# linesFile = open(sys.argv[5], "w")
# length = int(sys.argv[6])

# for line in origArabizi:
#     line = line.strip()
#     line = line.split()

#     linesFile.write(str(len(line)) + "\n")

#     line = (["<bos>"] * context) + line  + (["<eos>"] * context)
#     for word in range(context, len(line) - context):