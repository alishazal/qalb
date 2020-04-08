# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import os
import shutil

def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

def getFirstTokenLine(file):

    tree = ET.parse("bolt_sms_chat_ara_src_transliteration/data/transliteration/" + file)
    root = tree.getroot()

    tracker = 0
    allWords = root.findall("./su/annotated_arabizi/token")

    for source in root.findall("./su/source"):
        numLines = 0
        if source.text == None:
            continue

        numLines = len(source.text.split())

        currLine = ""
        if tracker >= len(allWords):
            continue
        for j in range(tracker, tracker + numLines):
            currLine += allWords[j].text + " "
        
        currLine = currLine.strip()
        tracker += numLines

        if isEnglish(currLine):
            return currLine
    
    # In case no line is english just return the last one scanned
    return currLine
    
def finalCheck(file, split):

    allLinesInFile = []
    
    tree = ET.parse("bolt_sms_chat_ara_src_transliteration/data/transliteration/" + file)
    root = tree.getroot()

    tracker = 0
    allWords = root.findall("./su/annotated_arabizi/token")

    for source in root.findall("./su/source"):
        numLines = 0
        if source.text == None:
            continue

        numLines = len(source.text.split())
        
        currLine = ""
        if tracker >= len(allWords):
            continue
        for j in range(tracker, tracker + numLines):
            currLine += allWords[j].text + " "
        
        allLinesInFile.append(currLine.strip())
        tracker += numLines

    # Limit variable is to check only a certain no
    # of lines and not all of them
    limit = 0
    for line in allLinesInFile:
        if limit >= 3:
            return True

        if isEnglish(line) and line not in split:
            return False

        limit += 1
    
    return True

rawBolt = os.listdir("bolt_sms_chat_ara_src_transliteration/data/transliteration")
bolt = []
for i in rawBolt:
    if i[-3:] == "xml":
        bolt.append(i)

train = list(map(str.strip, open("ai/datasets/data/arabizi/ldc-train.arabizi").readlines()))
dev = list(map(str.strip, open("ai/datasets/data/arabizi/ldc-dev.arabizi").readlines()))
test = list(map(str.strip, open("ai/datasets/data/arabizi/ldc-test.arabizi").readlines()))
# train_S = map(str.strip, open("ai/datasets/data/arabizi/train80.arabizi").readlines())

splits = {
    "train": [],
    "dev": [],
    "test": [],
    "none": []
}

count = 1
for i in bolt:

    if count % 20 == 0:
        print("Processed files:", count)
    
    line = getFirstTokenLine(i)

    if line in train and finalCheck(i, train):
        splits["train"].append(i)
        shutil.copy("bolt_sms_chat_ara_src_transliteration/data/transliteration/" + i, "ldc_3arrib_splits_mapping/train")
    
    elif line in dev and finalCheck(i, dev):
        splits["dev"].append(i)
        shutil.copy("bolt_sms_chat_ara_src_transliteration/data/transliteration/" + i, "ldc_3arrib_splits_mapping/dev")

    elif line in test and finalCheck(i, test):
        splits["test"].append(i)
        shutil.copy("bolt_sms_chat_ara_src_transliteration/data/transliteration/" + i, "ldc_3arrib_splits_mapping/test")

    else:
        splits["none"].append(i)
        shutil.copy("bolt_sms_chat_ara_src_transliteration/data/transliteration/" + i, "ldc_3arrib_splits_mapping/none")

    count += 1

print("Train Files:", len(splits["train"]), "\nDev Files:", len(splits["dev"]), "\nTest Files:", len(splits["test"]), "\nNo Match Files:", len(splits["none"]))

            