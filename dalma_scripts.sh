# ---- Working on July 18, 2020 ----
# Script 1: word2word-train-predict-evaluate.sh
#!/bin/bash
#SBATCH --gres=gpu:1
#SBATCH -p nvidia
#SBATCH --mail-type=ALL
#SBATCH --mail-user=as10505
#SBATCH --mem=30000
#SBATCH --time=24:00:00
module purge
module load all
module load anaconda/2-4.1.1
module load cuda/8.0
module load gcc/4.9.3
source activate capstone-gpu
# Preprocess the fasttext training input data
python3 helpers/preprocess_fasttext_data.py --input_file=splits_ldc/source/source-without-dev-test.arabizi --output_file=splits_ldc/source/source-without-dev-test-preprocessed.arabizi
# Word-embeddings training
./fastText/fasttext skipgram -input splits_ldc/source/source-without-dev-test-preprocessed.arabizi -output pretrained_word_embeddings/arabizi_300_narrow -dim 300 -minn 2 -ws 2
# Run complete word2word system; it is the default so we dont need to pass any flags
python3 transliterate.py

# Script 2: line2line-train-predict-evaluate.sh
#!/bin/bash
#SBATCH --gres=gpu:1
#SBATCH -p nvidia
#SBATCH --mail-type=ALL
#SBATCH --mail-user=as10505
#SBATCH --mem=30000
#SBATCH --time=24:00:00
module purge
module load all
module load anaconda/2-4.1.1
module load cuda/8.0
module load gcc/4.9.3
source activate capstone-gpu
# Run complete line2line system
python3 transliterate.py --model_name=line2line --model_output_path=output/models/line2line_model --prediction_loaded_model_training_train_input=temp/line2line_training_train_input --prediction_loaded_model_training_train_output=temp/line2line_training_train_output --prediction_loaded_model_training_dev_input=temp/line2line_training_dev_input --prediction_loaded_model_training_dev_output=temp/line2line_training_dev_output --predict_output_file=output/predictions/line2line-dev.out --evaluation_results_file=output/evaluations/line2line_evaluation_results.txt --batch_size=1024