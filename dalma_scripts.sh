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

python3 helpers/preprocess_fasttext_data.py --input_file=splits_ldc/source/source-without-dev-test.arabizi --output_file=splits_ldc/source/source-without-dev-test-preprocessed.arabizi
# Word-embeddings training
./fastText/fasttext skipgram -input splits_ldc/source/source-without-dev-test-preprocessed.arabizi -output pretrained_word_embeddings/arabizi_300_narrow -dim 300 -minn 2 -ws 2

python3 transliterate.py