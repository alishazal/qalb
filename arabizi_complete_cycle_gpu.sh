#!/bin/bash
#SBATCH --gres=gpu:1
#SBATCH -p nvidia
#SBATCH --mail-type=ALL
#SBATCH --mail-user=as10505
#SBATCH --mem=30000
#SBATCH --time=48:00:00
module purge
module load all
module load anaconda/2-4.1.1
module load cuda/8.0
module load gcc/4.9.3
source activate capstone-gpu
python -m ai.tests.qalb --model_name=arabizi_baseline_gpu_4 --extension=arabizi --max_sentence_length=40 --output_path=output/arabizi_baseline_gpu_4

python -m ai.tests.qalb --model_name=arabizi_baseline_gpu_4 --decode=ai/datasets/data/arabizi/ldc-dev.arabizi --extension=arabizi --max_sentence_length=40 --beam_size=5 --output_path=output/arabizi_baseline_gpu_4/decoder_dev.out
