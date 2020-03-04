import os
import csv

files = os.listdir("MADAR-Shared-Task-Subtask-1")
arabicFile = open("MADAR-CAI-arabic.txt", "w")

count = 0
for i in files:
    if i[-3:] == "tsv":
        with open("MADAR-Shared-Task-Subtask-1/" + i) as tsvfile:
            reader = csv.reader(tsvfile, delimiter='\t')
            for row in reader:
                if row[1] == "CAI":
                    arabicFile.write(row[0] + "\n")