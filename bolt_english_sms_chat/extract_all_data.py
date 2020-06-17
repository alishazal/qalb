# -*- coding: utf-8 -*-

"""
Usage: python3 extract_sample_of_data.py [file-name.english]
"""

import xml.etree.ElementTree as ET
import os
import sys

english = open(sys.argv[1], "w")

files = os.listdir("data")
files.sort()

fileCount = 1
lineCount = 0
for file in files:

    if fileCount % 200 == 0:
        print(str(fileCount) + " files read. " + str(lineCount) + " lines processed.")

    if file[-3:] != "xml":
        continue

    tree = ET.parse("data/" + file)
    root = tree.getroot()
    allLines = root.findall("./messages/message/body")
    for line in allLines:
        if line.text == None:
            continue
        english.write(line.text.strip() + "\n")
        lineCount += 1
    fileCount += 1

english.close()