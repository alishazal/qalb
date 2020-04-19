"""
Usage: python3 remove-separation-tokens.py [original-file] [new-file]
"""

import sys

original = open(sys.argv[1], "r")
newFile = open(sys.argv[2], "w")

for line in original:

    line = line.replace("[+] ", "")
    line = line.replace("[-]", " ")
    line = line.replace("[+]", "")
    
    newFile.write(line)

original.close()
newFile.close()