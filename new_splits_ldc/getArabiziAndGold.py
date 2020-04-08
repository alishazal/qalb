# import xml.etree.ElementTree as ET
# import os

# dirs = os.listdir("./")
# dirs.sort()

# arabizi = open("bolt-ldc-transliteration.arabizi", "w")

# for i in dirs:
#     if i[-3:] != "xml":
#         continue
#     tree = ET.parse(i)
#     root = tree.getroot()

#     tracker = 0
#     allWords = root.findall("./su/annotated_arabizi/token")
#     for source in root.findall("./su/source"):
#         numLines = 0
#         if source.text == None:
#             continue

#         numLines = len(source.text.split())
        
#         currLine = ""
#         if tracker >= len(allWords):
#             continue
#         for j in range(tracker, tracker + numLines):
#             currLine += allWords[j].text + " "
        
#         arabizi.write(currLine.strip() + "\n")
#         tracker += numLines
        
# arabizi.close()
