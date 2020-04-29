"""
Usage: python3 arabizi-to-arabic.py [input] [output]
"""
import sys

from camel_tools.utils.charmap import CharMapper
bw2ar = CharMapper.builtin_mapper('bw2ar')

iFile = open(sys.argv[1], "r")
oFile = open(sys.argv[2], "w")

for i in iFile:
    ar_output = bw2ar(i.strip())
    oFile.write(ar_output + "\n")

iFile.close()
oFile.close()