"""
Usage: python arabic-to-buckwalter.py [file] [new-file]
"""

import sys
from camel_tools.utils.charmap import CharMapper
ar2bw = CharMapper.builtin_mapper('ar2bw')

originalFile = open(sys.argv[1], "r").readlines()
newFile = open(sys.argv[2], "w")

for i in originalFile:
    bw_output = ar2bw(i).replace("،", ",").replace("؟", "?").strip()
    newFile.write(bw_output + "\n")
    
