"""
Usage: python3 identify-data.py [my-file] [big-corpus] [matched-file] [unmatched-file]
"""

import sys

f = open(sys.argv[1], "r")
myFile = f.readlines()

c = open(sys.argv[2], "r")
corpus = c.readlines()

matched = open(sys.argv[3], "w")
unmatched = open(sys.argv[4], "w")

count = 1
for i in myFile:
    if count % 50 == 0:
        print("Processed lines:", count)

    # i = i.strip()

    if i in corpus:
        matched.write(i)
    else:
        unmatched.write(i)
    
    count += 1

f.close()
c.close()
matched.close()
unmatched.close()