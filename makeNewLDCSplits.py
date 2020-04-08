# -*- coding: utf-8 -*-

"""
Usage: python3 makeNewLDCSplits.py [split.txt] [splitFolder]
Example: python3 makeNewLDCSplits.py new_splits_ldc/dev/dev.txt new_splits_ldc/dev 
"""

import xml.etree.ElementTree as ET
import os
import sys
import shutil

# Read the txt file
splitTxt = open(sys.argv[1], "r")

for xmlFile in splitTxt.readlines():
    xmlFile = xmlFile.strip()

    # Copy the xml to the correct split folder
    shutil.copy("bolt_sms_chat_ara_src_transliteration/data/transliteration/" + xmlFile, sys.argv[2])

splitTxt.close()

