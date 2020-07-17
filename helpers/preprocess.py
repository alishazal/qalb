"""
Function -> preprocess(source):
    > compression: repetitions over 2 => reduced to 2
    > lowercase all letters
    > accented letter => unaccented
"""

import sys
import unicodedata as ud
import re
from helpers.tag import tag

def allNonAscii(word):
    for char in word:
        if ord(char) < 128:
            return False
    
    return True

def copyNonAscii(input_line, copy_marker, output_line, is_prediction):

    input_words = input_line.split()
    if not is_prediction: output_words = output_line.split()
    
    for i in range(len(input_words)):
        if allNonAscii(input_words[i]):
            input_words[i] = copy_marker
            if not is_prediction: output_words[i] = copy_marker

    if is_prediction: return " ".join(input_words)
    return " ".join(input_words), " ".join(output_words)

def isPunctuation(word):
    for char in word:
        if char not in ".,?!'\":;-()[]}{":
            return False

    return True

def copyTextEmojiAndPunctuation(input_line, copy_marker, output_line, is_prediction):

    input_words = input_line.split()
    if not is_prediction: output_words = output_line.split()
    
    for i in range(len(input_words)):
        if isPunctuation(input_words[i]):
            input_words[i] = copy_marker
            if not is_prediction: output_words[i] = copy_marker

        else:
            # Handling <3 separately first
            match = re.search(r'(<3)+', input_words[i], re.IGNORECASE)
            if match and match.group(0) == input_words[i]:
                input_words[i] = copy_marker
                if not is_prediction: output_words[i] = copy_marker

            match = re.search(r'[=:;8xX>^()$*@][-_.\'"]*[XxOoPpsSDVv)(\][/\\Cc3><}{@|:;=0*L$^~]+', input_words[i], re.IGNORECASE) 
            if match:
                emoticon = match.group(0)
                if emoticon == input_words[i]:
                    input_words[i] = copy_marker
                    if not is_prediction: output_words[i] = copy_marker

    if is_prediction: return " ".join(input_words)
    return " ".join(input_words), " ".join(output_words)

def removeAccents(line):
    
    newLine = []
    for word in line.split(" "):
        nfkd_form = ud.normalize('NFKD', word)
        res = "".join([c for c in nfkd_form if not ud.combining(c)])
        newLine.append(res.replace(' ', ''))
    return " ".join(newLine)

def compress(line, limit):

    ans = ""
    currChar = ""
    currCharCounter = 1

    compressThese = '23567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_ '

    for i in line:
        if i == currChar:
            currCharCounter += 1
        else:
            currChar = i
            currCharCounter = 1
            
        if currCharCounter < limit + 1 or i not in compressThese:
            ans += i
    
    return ans

def copy_tokens(input_line, output_line, copy_marker):
    input_line = input_line.split()
    output_line = output_line.split()

    new_output = []
    for word in range(len(output_line)):
        if input_line[word] == output_line[word]: new_output.append(copy_marker)
        else: new_output.append(output_line[word])
        
    return " ".join(new_output)

def aligned_lines(all_input_lines, all_output_lines):
    new_input_lines = []
    new_output_lines = []
    for line in range(len(all_input_lines)):
        if len(all_input_lines[line].split()) == len(all_output_lines[line].split()):
            new_input_lines.append(all_input_lines[line])
            new_output_lines.append(all_output_lines[line])
    
    return new_input_lines, new_output_lines

def preprocess(all_input_lines, all_output_lines, is_train, is_predict, alignment, copy_unchanged_tokens, 
            copy_marker, model_name, context, writing_system):
    if is_train:
        if alignment == "word":
            # get lines which are word-aligned
            all_input_lines, all_output_lines = aligned_lines(all_input_lines, all_output_lines)

        for line in range(len(all_input_lines)):
            input_line = all_input_lines[line].strip()
            output_line = all_output_lines[line].strip()
            #convert unchanged words to a special character (default: #) to protect them in output
            if is_train and copy_unchanged_tokens and alignment == "word":
                output_line = copy_tokens(input_line, output_line, copy_marker)
            #preprocessing
            input_line = compress(input_line, 2)
            input_line = input_line.lower()
            input_line = removeAccents(input_line)
            if alignment == "word":
                if writing_system == "latin":
                    input_line, output_line = copyNonAscii(input_line, copy_marker, output_line, False)
                input_line, output_line = copyTextEmojiAndPunctuation(input_line, copy_marker, output_line, False)
            all_input_lines[line] = input_line
            all_output_lines[line] = output_line
        # making sure input and output lines are aligned
        all_input_lines, all_output_lines = aligned_lines(all_input_lines, all_output_lines)

        if model_name == "word2word":
            tagged_input_lines, tagged_output_lines, lines_record = tag(all_input_lines, all_output_lines, context, "train") 
            return tagged_input_lines, tagged_output_lines, lines_record

        return all_input_lines, all_output_lines

    if is_predict:
        for line in range(len(all_input_lines)):
            input_line = all_input_lines[line].strip()

            #preprocessing
            input_line = compress(input_line, 2)
            input_line = input_line.lower()
            input_line = removeAccents(input_line)
            if alignment == "word":
                if writing_system == "latin":
                    input_line = copyNonAscii(input_line, copy_marker, None, True)
                input_line = copyTextEmojiAndPunctuation(input_line, copy_marker, None, True)
            all_input_lines[line] = input_line

        if model_name == "word2word":
            tagged_input_lines, lines_record = tag(all_input_lines, [], context, "predict") 
            return tagged_input_lines, lines_record

        return all_input_lines
