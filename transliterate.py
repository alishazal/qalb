# Written in python3

import subprocess
import sys
import os
import argparse
import time

from helpers.preprocess import preprocess
from helpers.tag import tag
from ai.tests.mle import train_mle, predict_mle
from camel_tools.utils.charmap import CharMapper

ar2bw = CharMapper.builtin_mapper('ar2bw')

def is_bool(s):
    return str(s) != 'False'
parser = argparse.ArgumentParser(description='This program rewrites (transliterates) from one language script to another')

# --model_name can take values "mle", "word2word", "line2line", or "hybrid"
parser.add_argument('--model_name', action="store", dest='model_name', default="word2word")
# --model_python_script specifies the path of the python script that runs the specific model
parser.add_argument('--model_python_script', action="store", dest='model_python_script', default="ai/tests/char_seq2seq.py")
# --train can take values True or False
parser.add_argument('--train', action="store", dest="train", default=True, type=is_bool)
# --predict can take values True or False
parser.add_argument('--predict', action="store", dest="predict", default=True, type=is_bool)
# --evaluate_accuracy can take values True or False
parser.add_argument('--evaluate_accuracy', action="store", dest="evaluate_accuracy", default=True, type=is_bool)
# --evaluate_bleu can take values True or False
parser.add_argument('--evaluate_bleu', action="store", dest="evaluate_bleu", default=True, type=is_bool)

#TRAINING
# --train_source_file takes the path to the source file for training
parser.add_argument('--train_source_file', action="store", dest='train_source_file', default="splits_ldc/train/train-source.arabizi")
# --train_target_file takes the path to the target file for training
parser.add_argument('--train_target_file', action="store", dest='train_target_file', default="splits_ldc/train/train-word-aligned-target.gold")
# --dev_source_file takes the path to the dev source file used during training
parser.add_argument('--dev_source_file', action="store", dest='dev_source_file', default="splits_ldc/dev/dev-source.arabizi")
# --dev_target_file takes the path to the dev target file used during training
parser.add_argument('--dev_target_file', action="store", dest='dev_target_file', default="splits_ldc/dev/dev-word-aligned-target.gold")
# --alignment takes the values word or sentence
parser.add_argument('--alignment', action="store", dest='alignment', default="word")
# --context is only for word2word models.
parser.add_argument('--context', action="store", dest='context', default=1)
# --include_fasttext checks if user wants to run fasttext
parser.add_argument('--include_fasttext', action="store", dest='include_fasttext', default=True, type=is_bool)
# --fasttext_executable takes the path to the fasttext executable file needed to load pretrained word embeddings
parser.add_argument('--fasttext_executable', action="store", dest='fasttext_executable', default="./fastText/fasttext")
# --fasttext_bin_file takes the path to the fasttext .bin file which has the pretrained word embeddings
parser.add_argument('--fasttext_bin_file', action="store", dest='fasttext_bin_file', default="pretrained_word_embeddings/arabizi_300_narrow.bin")
# --model_output_path takes the path to store the model and its associated files during training. This is used during
# prediction
parser.add_argument('--model_output_path', action="store", dest='model_output_path', default="output/models/word2word_model")

# PREDICTION
# ---- For cases where the model was trained somewhere other than our system we have the following 4 flags to 
# get the data the model was trained on to load fasttext word embeddings of that data. Of course, in this case,
# the user will have to provide their own fasttext bin file too using the --fasttext_bin_file flag above. ----
# --prediction_loaded_model_training_train_input takes the path to the training train-set input file that was
# used to train the model that we're loading for prediction
parser.add_argument('--prediction_loaded_model_training_train_input', action="store", dest='prediction_loaded_model_training_train_input', default="temp/word2word_training_train_input")
# --prediction_loaded_model_training_train_output takes the path to the training train-set output file that was
# used to train the model that we're loading for prediction
parser.add_argument('--prediction_loaded_model_training_train_output', action="store", dest='prediction_loaded_model_training_train_output', default="temp/word2word_training_train_output")
# --prediction_loaded_model_training_dev_input takes the path to the training dev-set input file that was
# used to train the model that we're loading for prediction
parser.add_argument('--prediction_loaded_model_training_dev_input', action="store", dest='prediction_loaded_model_training_dev_input', default="temp/word2word_training_dev_input")
# --prediction_loaded_model_training_dev_output takes the path to the training dev-set output file that was
# used to train the model that we're loading for prediction
parser.add_argument('--prediction_loaded_model_training_dev_output', action="store", dest='prediction_loaded_model_training_dev_output', default="temp/word2word_training_dev_output")
# --predict_input_file takes the path to the input file for prediction
parser.add_argument('--predict_input_file', action="store", dest='predict_input_file', default="splits_ldc/dev/dev-source.arabizi")
# --predict_output_file takes the path where the prediction output file will be stored
parser.add_argument('--predict_output_file', action="store", dest='predict_output_file', default="output/predictions/word2word-dev.out")
# --predict_output_word_aligned_gold takes the path of the word-aligned gold file for evaluation of system's prediction
parser.add_argument('--predict_output_word_aligned_gold', action="store", dest='predict_output_word_aligned_gold', default="splits_ldc/dev/dev-word-aligned-target.gold")
# --predict_output_sentence_aligned_gold takes the path of the sentence-aligned gold file for evaluation of system's prediction
parser.add_argument('--predict_output_sentence_aligned_gold', action="store", dest='predict_output_sentence_aligned_gold', default="splits_ldc/dev/dev-sentence-aligned-target.gold")

# EVALUATION
# --evaluation_results_file takes the path where the evaluation result will be stored
parser.add_argument('--evaluation_results_file', action="store", dest='evaluation_results_file', default="output/evaluations/word2word_evaluation_results.txt")

# PREPROCESSING
# --preprocess can take values True or False
parser.add_argument('--preprocess', action="store", dest='preprocess', default=True, type=is_bool)
# --copy_unchanged_tokens can take values True or False. It protects words that should remain untouched in
# training input and training output by converting training output to a special marker (default: "#"; see below flag).
parser.add_argument('--copy_unchanged_tokens', action="store", dest='copy_unchanged_tokens', default=True, type=is_bool)
# special marker that signals that a token should be copied as is in the output
parser.add_argument('--copy_marker', action="store", dest='copy_marker', default="#")
# --input_writing_system could be "latin" or "other"; we need this flag for the preprocesser because it assumes latin
# scripts and turns all words that have a non ASCII-128 character in it to hashtag. So the preprocessor would 
# need to know if the input_writing_system of the data is something other than latin so it doesn't convert everything
# to hashtag
parser.add_argument('--input_writing_system', action="store", dest='input_writing_system', default="latin")
# Adding this flag so that ay-normalized evaluation is only run when the output language is arabic
parser.add_argument('--output_language', action="store", dest='output_language', default="arabic")

# ----------Seq2Seq MODEL FLAGS: Details of use and implementation in ai/tests/char_seq2seq.py----------
# inintial learning rate
parser.add_argument('--lr', action="store", dest='lr', default=0.0001)
# batch size
parser.add_argument('--batch_size', action="store", dest='batch_size', default=2048)
# embedding dimension
parser.add_argument('--embedding_size', action="store", dest='embedding_size', default=256)
# number of hidden units
parser.add_argument('--hidden_size', action="store", dest='hidden_size', default=256)
# number of RNN layers
parser.add_argument('--rnn_layers', action="store", dest='rnn_layers', default=2)
# whether to use a bidirectional RNN in the encoder's 1st layer
parser.add_argument('--bidirectional_encoder', action="store", dest='bidirectional_encoder', default=True, type=is_bool)
# --bidirectional_mode options are add, concat or project
parser.add_argument('--bidirectional_mode', action="store", dest='bidirectional_mode', default="add")
# set --use_lstm to false to use GRUs
parser.add_argument('--use_lstm', action="store", dest='use_lstm', default=False, type=is_bool)
# --attention options are luong or bahdanau
parser.add_argument('--attention', action="store", dest='attention', default="luong")
# probability for dropout on the RNN's non-recurrent connections
parser.add_argument('--dropout', action="store", dest='dropout', default=0.9)
# clip gradients to this norm
parser.add_argument('--max_grad_norm', action="store", dest='max_grad_norm', default=11.5)
# beam search size
parser.add_argument('--beam_size', action="store", dest='beam_size', default=5)
# initial decoder sampling probability (0 = ground truth; 1 = use predictions)
parser.add_argument('--initial_p_sample', action="store", dest='initial_p_sample', default=0.35)
# final decoder sampling probability (0 = ground truth; 1 = use predictions)
parser.add_argument('--final_p_sample', action="store", dest='final_p_sample', default=0.35)
# duration in epochs of schedule sampling (determines the rate of change)
parser.add_argument('--epochs_p_sample', action="store", dest='epochs_p_sample', default=20)
# Set False for sigmoid decay
parser.add_argument('--linear_p_sample', action="store", dest='linear_p_sample', default=True, type=is_bool)
# Set this greater than 1 to compress contiguous patterns in the data pipeline
parser.add_argument('--parse_repeated', action="store", dest='parse_repeated', default=0)
# Denominator constant
parser.add_argument('--epsilon', action="store", dest='epsilon', default=1e-8)
# first order moment decay
parser.add_argument('--beta1', action="store", dest='beta1', default=0.9)
# second order moment decay
parser.add_argument('--beta2', action="store", dest='beta2', default=0.999)
# backpropagation on or off; default is off (False)
parser.add_argument('--train_word_embeddings', action="store", dest='train_word_embeddings', default=False, type=is_bool)
# maximum number of characters in input and output
parser.add_argument('--max_sentence_length', action="store", dest='max_sentence_length', default=110)
# number of steps to wait before running the graph with the dev set
parser.add_argument('--num_steps_per_eval', action="store", dest='num_steps_per_eval', default=50)
# number of epochs to run; 0 = no limit
parser.add_argument('--max_epochs', action="store", dest='max_epochs', default=40)
# restore an existing model or not
parser.add_argument('--restore', action="store", dest='restore', default=True, type=is_bool)
# ----------//Seq2Seq MODEL FLAGS: Details of use and implementation in ai/tests/char_seq2seq.py//----------

args = parser.parse_args()

def list_to_file(input_list, file_name):
    f = open(file_name, "w")
    for line in input_list:
        line = line.strip()
        f.write(line + "\n")
    f.close()

def create_temp_input_output_files(ml_train_input_lines, ml_train_output_lines, ml_dev_input_lines, ml_dev_output_lines):
    list_to_file(ml_train_input_lines, f"temp/{args.model_name}_training_train_input")
    list_to_file(ml_train_output_lines, f"temp/{args.model_name}_training_train_output")
    list_to_file(ml_dev_input_lines, f"temp/{args.model_name}_training_dev_input")
    list_to_file(ml_dev_output_lines, f"temp/{args.model_name}_training_dev_output")

def create_temp_line_record_files(train_lines_record, dev_lines_record):
    list_to_file(train_lines_record, f"temp/{args.model_name}_training_train_lines_record")
    list_to_file(dev_lines_record, f"temp/{args.model_name}_training_dev_lines_record")

def get_default_flags_string():
    return (f"--lr={args.lr} --batch_size={args.batch_size} --embedding_size={args.embedding_size} "
    f"--hidden_size={args.hidden_size} --rnn_layers={args.rnn_layers} --bidirectional_encoder={args.bidirectional_encoder} "
    f"--bidirectional_mode={args.bidirectional_mode} --use_lstm={args.use_lstm} "
    f"--attention={args.attention} --dropout={args.dropout} --max_grad_norm={args.max_grad_norm} "
    f"--beam_size={args.beam_size} --initial_p_sample={args.initial_p_sample} --final_p_sample={args.final_p_sample} "
    f"--epochs_p_sample={args.epochs_p_sample} --linear_p_sample={args.linear_p_sample} "
    f"--parse_repeated={args.parse_repeated} --epsilon={args.epsilon} --beta1={args.beta1} "
    f"--beta2={args.beta2} "
    f"--max_sentence_length={args.max_sentence_length} --num_steps_per_eval={args.num_steps_per_eval} "
    f"--max_epochs={args.max_epochs} --restore={args.restore} ")

def convert_path_to_module(path):
    path = path.replace(".py", "")
    return path.replace("/", ".")

def run_command(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    #start displaying output immediately
    while True:
        line = p.stdout.readline()
        sys.stdout.write(line.decode("utf-8"))
        sys.stdout.flush()
        if not line: break

def train_seq2seq():
    if args.include_fasttext:
        command = (f"python -m {convert_path_to_module(args.model_python_script)} "
        f"--train_input=temp/{args.model_name}_training_train_input "
        f"--train_output=temp/{args.model_name}_training_train_output --dev_input=temp/{args.model_name}_training_dev_input "
        f"--dev_output=temp/{args.model_name}_training_dev_output --model_output_dir={args.model_output_path} "
        f"--fasttext_executable={args.fasttext_executable} --word_embeddings={args.fasttext_bin_file} "
        f"--train_word_embeddings={args.train_word_embeddings} "
        f"{get_default_flags_string()}")    
    else:
        command = (f"python -m {convert_path_to_module(args.model_python_script)} "
        f"--train_input=temp/{args.model_name}_training_train_input "
        f"--train_output=temp/{args.model_name}_training_train_output --dev_input=temp/{args.model_name}_training_dev_input "
        f"--dev_output=temp/{args.model_name}_training_dev_output --model_output_dir={args.model_output_path} "
        f"{get_default_flags_string()}")

    run_command(command)

def predict_seq2seq():
    if args.include_fasttext:
        command = (f"python -m {convert_path_to_module(args.model_python_script)} "
        f"--train_input={args.prediction_loaded_model_training_train_input} "
        f"--train_output={args.prediction_loaded_model_training_train_output} --dev_input={args.prediction_loaded_model_training_dev_input} "
        f"--dev_output={args.prediction_loaded_model_training_dev_output} --model_output_dir={args.model_output_path} "
        f"--fasttext_executable={args.fasttext_executable} "
        f"--word_embeddings={args.fasttext_bin_file} --train_word_embeddings={args.train_word_embeddings} "
        f"--predict_input_file=temp/{args.model_name}_prediction_ml_input --predict_output_file={args.predict_output_file}")    
    else:
        command = (f"python -m {convert_path_to_module(args.model_python_script)} "
        f"--train_input={args.prediction_loaded_model_training_train_input} "
        f"--train_output={args.prediction_loaded_model_training_train_output} --dev_input={args.prediction_loaded_model_training_dev_input} "
        f"--dev_output={args.prediction_loaded_model_training_dev_output} --model_output_dir={args.model_output_path} "
        f"--predict_input_file=temp/{args.model_name}_prediction_ml_input " 
        f"--predict_output_file={args.predict_output_file}")

    run_command(command)

def load_mle():
    model_file = open(args.model_output_path, "r")
    model_lines = model_file.readlines()
    model_file.close()

    model = {}
    for line in model_lines:
        line = line.strip().split()
        model[line[0]] = line[1]

    return model

def join_lines(output_files_lines, lines_record):
    new_pred_lines = []
    predFileLinesTracker = 0
    for num in lines_record:
        num = int(num.strip())
        
        finalLine = ""
        for i in range(predFileLinesTracker, predFileLinesTracker + num):
            finalLine += output_files_lines[i].strip() + " "

        predFileLinesTracker += num
        new_pred_lines.append(finalLine.strip())

    return new_pred_lines

def remove_plus_before_foreign(line):
    for word in range(1, len(line)):
        if line[word] == "#" and "[+]" in line[word - 1]:
            line[word - 1] = line[word - 1].replace("[+]", "")
    return line

def replace_hashes_from_source(source_line, hashes_line):
    source_line = source_line.strip().split()
    hashes_line = hashes_line.strip().split()
    for i in range(len(hashes_line)):
        if hashes_line[i] == "#" and i < len(source_line):
            hashes_line[i] = source_line[i]
    return " ".join(hashes_line)

def postprocess():
    output_file = open(args.predict_output_file, "r")
    output_file_lines = output_file.readlines()
    output_file.close()

    # join tagged lines
    if args.model_name == "word2word":
        lines_record_file = open(f"temp/{args.model_name}_prediction_lines_record", "r")
        lines_record_file_lines = lines_record_file.readlines()
        lines_record_file.close()
        output_file_lines = join_lines(output_file_lines, lines_record_file_lines)

    source_file = open(args.predict_input_file, "r")
    source_file_lines = source_file.readlines()
    source_file.close()
    for line in range(len(output_file_lines)):
        # remove [+] tokens before foreign words
        output_file_lines[line] = remove_plus_before_foreign(output_file_lines[line])
        # fill in hashtags from source
        output_file_lines[line] = replace_hashes_from_source(source_file_lines[line], output_file_lines[line])

    return output_file_lines

def accuracy(system_output, gold):
    system_output_file = open(system_output, "r")
    system_output_file_lines = system_output_file.readlines()
    system_output_file.close()
    gold_file = open(gold, "r")
    gold_files_lines = gold_file.readlines()
    gold_file.close()

    correct = 0
    total = 0
    for i in range(len(system_output_file_lines)):
        curr_prediction_line = system_output_file_lines[i].split(" ")
        curr_gold_line = gold_files_lines[i].split(" ")
        if len(curr_prediction_line) == len(curr_gold_line):
            for j in range(len(curr_prediction_line)):
                if curr_prediction_line[j] == curr_gold_line[j]:
                    correct += 1
                total += 1
        elif len(curr_prediction_line) > len(curr_gold_line):
            for j in range(len(curr_prediction_line)):
                if j < len(curr_gold_line) and curr_prediction_line[j] == curr_gold_line[j]:
                    correct += 1
                total += 1
        else:
            for j in range(len(curr_gold_line)):
                if j < len(curr_prediction_line) and curr_prediction_line[j] == curr_gold_line[j]:
                    correct += 1
                total += 1
    return (correct/total)*100

def create_ay_normalized_file(file, new_file):
    file = open(file, "r")
    file_lines = file.readlines()
    file.close()

    normalized_lines = []
    unwantedChars = ["<", ">", "|"]
    for line in file_lines:
        line = ar2bw(line.strip())
        for char in unwantedChars:
            if char in line:
                line = line.replace(char, "A")
        if "Y" in line:
            line = line.replace("Y", "y")
        normalized_lines.append(line)

    list_to_file(normalized_lines, new_file) 

def evaluate_bleu(system_output, gold):
    cmd = f"perl ai/tests/bleu/multi-bleu.perl {gold} < {system_output}"
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    result = p.communicate()[0]
    return result.decode("utf-8")[7:12]

def create_file_with_plus_minus_tokens_removed(system_output, new_file):
    system_output = open(system_output, "r")
    new_file = open(new_file, "w")
    for line in system_output:
        line = line.replace("[+] ", "")
        line = line.replace("[-]", " ")
        line = line.replace("[+]", "")
        new_file.write(line)
    system_output.close()
    new_file.close()

if args.train:
    if args.model_name not in ["mle", "word2word", "line2line"]:
        raise ValueError("Invalid model name. Can be only 'mle', 'word2word' or 'line2line'")

    # Open training files
    train_source_file = open(args.train_source_file, "r")
    train_source_file_lines = train_source_file.readlines()
    train_source_file.close()
    train_target_file = open(args.train_target_file, "r")
    train_target_file_lines = train_target_file.readlines()
    train_target_file.close()
    # Open dev files
    dev_source_file = open(args.dev_source_file, "r")
    dev_source_file_lines = dev_source_file.readlines()
    dev_source_file.close()
    dev_target_file = open(args.dev_target_file, "r")
    dev_target_file_lines = dev_target_file.readlines()
    dev_target_file.close()

    if len(train_source_file_lines) != len(train_target_file_lines): raise ValueError(
    "Train source file and train target file have unequal number of lines")
    if len(dev_source_file_lines) != len(dev_target_file_lines): raise ValueError(
    "Dev source file and dev target file have unequal number of lines")

    if args.model_name != "mle":
        if args.model_name == "word2word":
            ml_train_input_lines, ml_train_output_lines, train_lines_record = preprocess(train_source_file_lines, train_target_file_lines, True, False, args.alignment, args.copy_unchanged_tokens, args.copy_marker, args.model_name, args.context, args.input_writing_system)
            ml_dev_input_lines, ml_dev_output_lines, dev_lines_record = preprocess(dev_source_file_lines, dev_target_file_lines, True, False, args.alignment, args.copy_unchanged_tokens, args.copy_marker, args.model_name, args.context, args.input_writing_system)
            create_temp_input_output_files(ml_train_input_lines, ml_train_output_lines, ml_dev_input_lines, ml_dev_output_lines)
            create_temp_line_record_files(train_lines_record, dev_lines_record)
        else:
            ml_train_input_lines, ml_train_output_lines = preprocess(train_source_file_lines, train_target_file_lines, True, False, args.alignment, args.copy_unchanged_tokens, args.copy_marker, args.model_name, None, args.input_writing_system)
            ml_dev_input_lines, ml_dev_output_lines = preprocess(dev_source_file_lines, dev_target_file_lines, True, False, args.alignment, args.copy_unchanged_tokens, args.copy_marker, args.model_name, None, args.input_writing_system)
            create_temp_input_output_files(ml_train_input_lines, ml_train_output_lines, ml_dev_input_lines, ml_dev_output_lines)

        print("Starting Seq2Seq training")
        training_start_time = time.time()
        train_seq2seq()
        total_training_time = time.time() - training_start_time
        print("Seq2Seq training completed")

    else:
        if args.alignment != "word":
            raise ValueError("MLE is only allowed for word-aligned lines")
        ml_train_input_lines, ml_train_output_lines = preprocess(train_source_file_lines, train_target_file_lines, True, False, args.alignment, args.copy_unchanged_tokens, args.copy_marker, args.model_name, None, args.input_writing_system)
        list_to_file(ml_train_input_lines, f"temp/{args.model_name}_training_train_input")
        list_to_file(ml_train_output_lines, f"temp/{args.model_name}_training_train_output")

        print("Starting MLE training")
        training_start_time = time.time()
        train_mle(ml_train_input_lines, ml_train_output_lines, args.model_output_path)  
        total_training_time = time.time() - training_start_time  
        print("MLE training completed")

if args.predict:
    predict_input_file = open(args.predict_input_file, "r")
    predict_input_file_lines = predict_input_file.readlines()
    predict_input_file.close()

    if args.model_name != "mle":
        if args.model_name == "word2word":
            ml_input_lines, lines_record = preprocess(predict_input_file_lines, [], False, True, args.alignment, None, args.copy_marker, args.model_name, args.context, args.input_writing_system)
            list_to_file(ml_input_lines, f"temp/{args.model_name}_prediction_ml_input")
            list_to_file(lines_record, f"temp/{args.model_name}_prediction_lines_record")
        else:
            ml_input_lines = preprocess(predict_input_file_lines, [], False, True, args.alignment, None, args.copy_marker, args.model_name, None, args.input_writing_system)
            list_to_file(ml_input_lines, f"temp/{args.model_name}_prediction_ml_input")

        print("Starting Seq2Seq prediction")
        prediction_start_time = time.time()
        predict_seq2seq()
        total_prediction_time = time.time() - prediction_start_time
        print("Seq2Seq prediction completed")

    else:
        ml_input_lines = preprocess(predict_input_file_lines, [], False, True, args.alignment, None, args.copy_marker, args.model_name, None, args.input_writing_system)
        list_to_file(ml_input_lines, f"temp/{args.model_name}_prediction_ml_input")
        mle_model = load_mle()

        print("Starting MLE prediction")
        prediction_start_time = time.time()
        predict_mle(mle_model, ml_input_lines, args.predict_output_file, "temp/mle_unknown.out")
        total_prediction_time = time.time() - prediction_start_time
        print("MLE prediction completed")

    prediction_final_output = postprocess()
    list_to_file(prediction_final_output, args.predict_output_file)

if args.evaluate_accuracy or args.evaluate_bleu:
    evaluation_results_file = open(args.evaluation_results_file, "w")

    if args.evaluate_accuracy:
        exact_system_accuracy = accuracy(args.predict_output_file, args.predict_output_word_aligned_gold)
        evaluation_results_file.write(f"Exact Accuracy: {str(round(exact_system_accuracy, 2))}%\n")
        if args.output_language == "arabic":
            create_ay_normalized_file(args.predict_output_file, f"temp/{args.model_name}_ay_normalized_word_aligned_output")
            create_ay_normalized_file(args.predict_output_word_aligned_gold, f"temp/{args.model_name}_ay_normalized_word_aligned_gold")
            ay_normalized_system_accuracy = accuracy(f"temp/{args.model_name}_ay_normalized_word_aligned_output", f"temp/{args.model_name}_ay_normalized_word_aligned_gold")
            evaluation_results_file.write(f"AY-Normalized Accuracy: {str(round(ay_normalized_system_accuracy, 2))}%\n")

    if args.evaluate_bleu:
        create_file_with_plus_minus_tokens_removed(args.predict_output_file, f"temp/{args.model_name}_sentence_aligned_output")
        exact_system_bleu = evaluate_bleu(f"temp/{args.model_name}_sentence_aligned_output", args.predict_output_sentence_aligned_gold)
        evaluation_results_file.write(f"Exact BLEU Score: {exact_system_bleu}\n")
        if args.output_language == "arabic":
            create_ay_normalized_file(f"temp/{args.model_name}_sentence_aligned_output", f"temp/{args.model_name}_ay_normalized_sentence_aligned_output")
            create_ay_normalized_file(args.predict_output_sentence_aligned_gold, f"temp/{args.model_name}_ay_normalized_sentence_aligned_gold")
            normalized_system_bleu = evaluate_bleu(f"temp/{args.model_name}_ay_normalized_sentence_aligned_output", f"temp/{args.model_name}_ay_normalized_sentence_aligned_gold")
            evaluation_results_file.write(f"AY-Normalized BLEU Score: {normalized_system_bleu}\n")
    
    evaluation_results_file.close()

# Print accuracy and time stats
print("\n")
if args.train: print(f"Training time was {total_training_time} seconds")
if args.predict: print(f"Prediction time was {total_prediction_time} seconds")
if args.evaluate_accuracy: print(f"Exact Accuracy: {round(exact_system_accuracy, 2)}% \nAY-Normalized Accuracy: {round(ay_normalized_system_accuracy, 2)}%")
if args.evaluate_bleu: print(f"Exact BLEU Score: {exact_system_bleu} \nAY-Normalized BLEU Score: {normalized_system_bleu}")