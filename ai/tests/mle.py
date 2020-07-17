def predict_mle(model, predict_input_file, predict_output_file, unknown_words_file):
    predict_output_file = open(predict_output_file, "w")
    unknown_words_file = open(unknown_words_file, "w") # this file will help in combining seq2seq with mle for the hybrid model
    
    for line in range(len(predict_input_file)):
        currLine = predict_input_file[line].strip().split()
        ans = []
        unk = []
        for word in range(len(currLine)):
            currWord = currLine[word]
            if currWord in model:
                ans.append(model[currWord])
                unk.append("0")
            else:
                ans.append("#")
                unk.append("1")
        ans = " ".join(ans)
        predict_output_file.write(ans + "\n")
        unknown_words_file.write(" ".join(unk) + "\n")

    predict_output_file.close()
    unknown_words_file.close()

def train_mle(train_input, train_output, model_output_path):
    model = {}
    for line in range(len(train_input)):
        currArabiziLine = train_input[line].strip().split()
        currGoldLine = train_output[line].strip().split()
        # go over every word of line
        for word in range(len(currArabiziLine)):
            currWord = currArabiziLine[word]
            goldWord = currGoldLine[word]
            # check if the word exists in our dict i.e if it has been seen before
            if currWord in model:
                found = False
                wordsList = model[currWord]
                # check if the gold of that word has been seen before
                for i in range(len(wordsList)):
                    if wordsList[i][0] == goldWord:
                        model[currWord][i][1] += 1
                        found = True
                        break
                # if that gold is never seen, put it in our dict for the word we're looking at
                if not found:
                    model[currWord].append([goldWord , 1])
            # if arabizi word doesn't exist in our dict
            else:
                model[currWord] = [[goldWord, 1]]

    # keeping the highest frequency gold for each arabizi word
    for word in model:
        model[word].sort(key=lambda x: x[1], reverse=True)
        model[word] = model[word][0][0]
    
    # save the model
    model_output_path_file = open(model_output_path, "w")
    for word in model:
        model_output_path_file.write(f"{word} {model[word]}\n")
    model_output_path_file.close()