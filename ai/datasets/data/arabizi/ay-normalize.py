"""
Usage: python ay-normalize.py [original-file] [normalized-file]
"""

import sys

unNormalizedFile = open(sys.argv[1], "r")
unfLines = unNormalizedFile.readlines()
normalizedFile = open(sys.argv[2], "w")

unwantedChars = ["<", ">", "|"]
for i in unfLines:
    for char in unwantedChars:
       if char in i:
           i = i.replace(char, "A")
           
    if "Y" in i:
        i = i.replace("Y", "y")

    normalizedFile.write(i)

unNormalizedFile.close()
normalizedFile.close()