 ------ Debugging on Dec 17, 2019 ------

 --- First trying arabizi data (very small one, only 100 lines)
python -m ai.tests.qalb-debugging --model_name=debugging-1 --extension=arabizi --output_path=output/debugging-1
python -m ai.tests.qalb-debugging --model_name=debugging-1 --decode=ai/datasets/data/arabizi/small-dev.arabizi --extension=arabizi --beam_size=5 --output_path=output/debugging-1/decoder_dev.out

It worked!
Now lets try with the length flag again. I think that is the problem

--- Now adding the max_sentence_length flag
python -m ai.tests.qalb-debugging --max_sentence_length=40 --model_name=debugging-3 --extension=arabizi --output_path=output/debugging-3
python -m ai.tests.qalb-debugging --model_name=debugging-3 --max_sentence_length=40 --decode=ai/datasets/data/arabizi/small-dev.arabizi --extension=arabizi --beam_size=5 --output_path=output/debugging-3/decoder_dev.out

Now it failed.
Maybe that was the problem all along. 
--- Lets increase the length of the data to 5000 now now. 
head -255 ai/datasets/data/arabizi/ldc-train.arabizi > ai/datasets/data/arabizi/bigger-train.arabizi
head -255 ai/datasets/data/arabizi/ldc-train.gold > ai/datasets/data/arabizi/bigger-train.gold
head -255 ai/datasets/data/arabizi/ldc-dev.gold > ai/datasets/data/arabizi/bigger-dev.gold
head -255 ai/datasets/data/arabizi/ldc-dev.arabizi > ai/datasets/data/arabizi/bigger-dev.arabizi

WAITTT. I think there is a problem in the code. In the decode function, we're not passsing in the flag of max_sentence_length.
Lets change the code and see.
python -m ai.tests.qalb-debugging --model_name=debugging-4 --max_sentence_length=40 --extension=arabizi --output_path=output/debugging-4
python -m ai.tests.qalb-debugging --model_name=debugging-4 --max_sentence_length=40 --decode=ai/datasets/data/arabizi/small-dev.arabizi --extension=arabizi --beam_size=5 --output_path=output/debugging-4/decoder_dev.out

Yes, the problem was the max_sentence_length was not passed in decode function. AND now that i've changed the code, it works. 
But it still fails for inputs that are bigger than max_sentence_length. For e.g a 60 length sentence would fail the program
if the max len flag is for 40. 
So i've now made a check to skip all sentences with length greater than the flag. Now it works fully.
Now we have two options:
1. We set a flag of 35 or 40 and run the whole system with the edited code.
2. We run the system with the default 400 flag, meaning that the flag for the max length is basically useless (because all 
our sentences are less than 400). We will accomodate the length of every sentence.

Now lets run both the scripts for both of these options:
--- Option 1: (arabizi_40.sh)
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

python -m ai.tests.qalb-debugged --model_name=arabizi-max-length-40 --max_sentence_length=40 --extension=arabizi --output_path=output/arabizi-max-length-40
python -m ai.tests.qalb-debugged --model_name=arabizi-max-length-40 --max_sentence_length=40 --decode=ai/datasets/data/arabizi/ldc-dev.arabizi --extension=arabizi --beam_size=5 --output_path=output/arabizi-max-length-40/decoder_dev.out

--- Option 2: (arabizi_400.sh)
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

python -m ai.tests.qalb --model_name=arabizi-default-length-400 --extension=arabizi --output_path=output/arabizi-default-length-400
python -m ai.tests.qalb --model_name=arabizi-default-length-400 --decode=ai/datasets/data/arabizi/ldc-dev.arabizi --extension=arabizi --beam_size=5 --output_path=output/arabizi-default-length-400/decoder_dev.out


------- Working on Dec 19 -------

The accuracy was really shit. Only 24.67. So we're running the system on 20, 70 and 100 sentence lengths.

--- Script 1: (arabizi_70.sh)
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

python -m ai.tests.qalb-debugged --model_name=arabizi-max-length-70 --max_sentence_length=70 --extension=arabizi --output_path=output/arabizi-max-length-70
python -m ai.tests.qalb-debugged --model_name=arabizi-max-length-70 --max_sentence_length=70 --decode=ai/datasets/data/arabizi/ldc-dev.arabizi --extension=arabizi --beam_size=5 --output_path=output/arabizi-max-length-70/decoder_dev.out
python ai/tests/accuracy-script/accuracy.py output/arabizi-max-length-70/decoder_dev.out ai/datasets/data/arabizi/ldc-dev.gold ai/datasets/data/arabizi/ldc-dev.arabizi 70

--- Script 2: (arabizi_100.sh)
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

python -m ai.tests.qalb-debugged --model_name=arabizi-max-length-100 --max_sentence_length=100 --extension=arabizi --output_path=output/arabizi-max-length-100
python -m ai.tests.qalb-debugged --model_name=arabizi-max-length-100 --max_sentence_length=100 --decode=ai/datasets/data/arabizi/ldc-dev.arabizi --extension=arabizi --beam_size=5 --output_path=output/arabizi-max-length-100/decoder_dev.out
python ai/tests/accuracy-script/accuracy.py output/arabizi-max-length-100/decoder_dev.out ai/datasets/data/arabizi/ldc-dev.gold ai/datasets/data/arabizi/ldc-dev.arabizi 100

--- Script 3: (arabizi_20.sh)
#!/bin/bash
#SBATCH --gres=gpu:1
#SBATCH -p nvidia
#SBATCH --mail-type=ALL
#SBATCH --mail-user=as10505
#SBATCH --mem=30000
#SBATCH --time=12:00:00
module purge
module load all
module load anaconda/2-4.1.1
module load cuda/8.0
module load gcc/4.9.3
source activate capstone-gpu

python -m ai.tests.qalb-debugged --model_name=arabizi-max-length-20 --max_sentence_length=20 --extension=arabizi --output_path=output/arabizi-max-length-20
python -m ai.tests.qalb-debugged --model_name=arabizi-max-length-20 --max_sentence_length=20 --decode=ai/datasets/data/arabizi/ldc-dev.arabizi --extension=arabizi --beam_size=5 --output_path=output/arabizi-max-length-20/decoder_dev.out
python ai/tests/accuracy-script/accuracy.py output/arabizi-max-length-20/decoder_dev.out ai/datasets/data/arabizi/ldc-dev.gold ai/datasets/data/arabizi/ldc-dev.arabizi 20

--- Script 3: (arabizi_30.sh)
#!/bin/bash
#SBATCH --gres=gpu:1
#SBATCH -p nvidia
#SBATCH --mail-type=ALL
#SBATCH --mail-user=as10505
#SBATCH --mem=30000
#SBATCH --time=12:00:00
module purge
module load all
module load anaconda/2-4.1.1
module load cuda/8.0
module load gcc/4.9.3
source activate capstone-gpu


python -m ai.tests.qalb-debugged --model_name=arabizi-max-length-30 --max_sentence_length=30 --decode=ai/datasets/data/arabizi/ldc-dev.arabizi --extension=arabizi --beam_size=5 --output_path=output/arabizi-max-length-30/decoder_dev.out
python ai/tests/accuracy-script/accuracy.py output/arabizi-max-length-30/decoder_dev.out ai/datasets/data/arabizi/ldc-dev.gold ai/datasets/data/arabizi/ldc-dev.arabizi 30


Results so far with different max_sentence_lengths:
arabizi_100: 8.28%
arabizi_70: 10.3%
arabizi_40: 26.7%
arabizi_30: 28.78%
arabizi_20: 30.72%
arabizi_10: 42.79%

------- Working on Feb 6 -------
python tag.py ldc-train.arabizi ldc-train.gold ldc-tagged-train.arabizi ldc-tagged-train.gold ldc-train.lines 2
python tag.py ldc-dev.arabizi ldc-dev.gold ldc-tagged-dev.arabizi ldc-tagged-dev.gold ldc-dev.lines 2

#!/bin/bash
#SBATCH --gres=gpu:1
#SBATCH -p nvidia
#SBATCH --mail-type=ALL
#SBATCH --mail-user=as10505
#SBATCH --mem=30000
#SBATCH --time=12:00:00
module purge
module load all
module load anaconda/2-4.1.1
module load cuda/8.0
module load gcc/4.9.3
source activate capstone-gpu

python -m ai.tests.qalb-debugged --model_name=tagged --max_sentence_length=100 --extension=arabizi --output_path=output/tagged
python -m ai.tests.qalb-debugged --model_name=tagged --max_sentence_length=100 --decode=ai/datasets/data/arabizi/ldc-tagged-dev.arabizi --extension=arabizi --beam_size=5 --output_path=output/tagged/decoder_dev.out


------- Working on Feb 7 -------
python tag.py ldc-train.arabizi ldc-train.gold ldc-4-tagged-train.arabizi ldc-4-tagged-train.gold ldc-4-train.lines 4
python tag.py ldc-dev.arabizi ldc-dev.gold ldc-4-tagged-dev.arabizi ldc-4-tagged-dev.gold ldc-4-dev.lines 4

python tag.py ldc-train.arabizi ldc-train.gold ldc-6-tagged-train.arabizi ldc-6-tagged-train.gold ldc-6-train.lines 6
python tag.py ldc-dev.arabizi ldc-dev.gold ldc-6-tagged-dev.arabizi ldc-6-tagged-dev.gold ldc-6-dev.lines 6

script 1: tagged-4.sh
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

python -m ai.tests.qalb-debugged ldc-4-tagged --model_name=tagged-4 --max_sentence_length=150 --extension=arabizi --output_path=output/tagged-4
python -m ai.tests.qalb-debugged ldc-4-tagged --model_name=tagged-4 --max_sentence_length=150 --decode=ai/datasets/data/arabizi/ldc-4-tagged-dev.arabizi --extension=arabizi --beam_size=5 --output_path=output/tagged-4/decoder_dev.out
python ai/tests/accuracy-script/accuracy.py output/tagged-4/decoder_dev.out ai/datasets/data/arabizi/ldc-4-tagged-dev.gold

script 2: tagged-6.sh
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

python -m ai.tests.qalb-debugged ldc-6-tagged --model_name=tagged-6 --max_sentence_length=180 --extension=arabizi --output_path=output/tagged-6
python -m ai.tests.qalb-debugged ldc-6-tagged --model_name=tagged-6 --max_sentence_length=180 --decode=ai/datasets/data/arabizi/ldc-6-tagged-dev.arabizi --extension=arabizi --beam_size=5 --output_path=output/tagged-6/decoder_dev.out
python ai/tests/accuracy-script/accuracy.py output/tagged-6/decoder_dev.out ai/datasets/data/arabizi/ldc-6-tagged-dev.gold


------- Working on Feb 10 -------
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
python -m ai.tests.qalb-debugged ldc-4-tagged --model_name=tagged-4 --max_sentence_length=150 --decode=ai/datasets/data/arabizi/ldc-4-tagged-dev.arabizi --extension=arabizi --beam_size=5 --output_path=output/tagged-4/decoder_dev.out
python -m ai.tests.qalb-debugged ldc-6-tagged --model_name=tagged-6 --max_sentence_length=180 --decode=ai/datasets/data/arabizi/ldc-6-tagged-dev.arabizi --extension=arabizi --beam_size=5 --output_path=output/tagged-6/decoder_dev.out


python tag.py ldc-train.arabizi ldc-train.gold ldc-1-tagged-train.arabizi ldc-1-tagged-train.gold ldc-1-train.lines 1
python tag.py ldc-dev.arabizi ldc-dev.gold ldc-1-tagged-dev.arabizi ldc-1-tagged-dev.gold ldc-1-dev.lines 1

script 1: tagged-1.sh
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

python -m ai.tests.qalb-debugged ldc-1-tagged --model_name=tagged-1 --max_sentence_length=150 --extension=arabizi --output_path=output/tagged-1
python -m ai.tests.qalb-debugged ldc-1-tagged --model_name=tagged-1 --max_sentence_length=150 --decode=ai/datasets/data/arabizi/ldc-1-tagged-dev.arabizi --extension=arabizi --beam_size=5 --output_path=output/tagged-1/decoder_dev.out
python ai/tests/accuracy-script/accuracy.py output/tagged-1/decoder_dev.out ai/datasets/data/arabizi/ldc-1-tagged-dev.gold

python no-context.py ldc-train.arabizi ldc-train.gold ldc-0-tagged-train.arabizi ldc-0-tagged-train.gold
python no-context.py ldc-dev.arabizi ldc-dev.gold ldc-0-tagged-dev.arabizi ldc-0-tagged-dev.gold

script 2: tagged-0.sh
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

python -m ai.tests.qalb-debugged ldc-0-tagged --model_name=tagged-0 --max_sentence_length=80 --extension=arabizi --output_path=output/tagged-0
python -m ai.tests.qalb-debugged ldc-0-tagged --model_name=tagged-0 --max_sentence_length=80 --decode=ai/datasets/data/arabizi/ldc-0-tagged-dev.arabizi --extension=arabizi --beam_size=5 --output_path=output/tagged-0/decoder_dev.out
python ai/tests/accuracy-script/accuracy.py output/tagged-0/decoder_dev.out ai/datasets/data/arabizi/ldc-0-tagged-dev.gold

------- Working on Feb 12 -------
script 1: tagged-1-batchsize-64.sh
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

python -m ai.tests.qalb-debugged ldc-1-tagged --batch_size=64 --model_name=tagged-1-batchsize-64 --max_sentence_length=150 --extension=arabizi --output_path=output/tagged-1-batchsize-64
python -m ai.tests.qalb-debugged ldc-1-tagged --batch_size=64 --model_name=tagged-1-batchsize-64 --max_sentence_length=150 --decode=ai/datasets/data/arabizi/ldc-1-tagged-dev.arabizi --extension=arabizi --beam_size=5 --output_path=output/tagged-1-batchsize-64/decoder_dev.out
python ai/tests/accuracy-script/accuracy.py output/tagged-1-batchsize-64/decoder_dev.out ai/datasets/data/arabizi/ldc-1-tagged-dev.gold

--- stop n check for accuracy
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
python -m ai.tests.qalb-debugged ldc-1-tagged --batch_size=64 --model_name=tagged-1-batchsize-64 --max_sentence_length=150 --decode=ai/datasets/data/arabizi/ldc-1-tagged-dev.arabizi --extension=arabizi --beam_size=5 --output_path=output/tagged-1-batchsize-64/decoder_dev.out
python ai/tests/accuracy-script/accuracy.py output/tagged-1-batchsize-64/decoder_dev.out ai/datasets/data/arabizi/ldc-1-tagged-dev.gold

script 2: tagged-1-batchsize-256.sh
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

python -m ai.tests.qalb-debugged ldc-1-tagged --batch_size=256 --model_name=tagged-1-batchsize-256 --max_sentence_length=150 --extension=arabizi --output_path=output/tagged-1-batchsize-256
python -m ai.tests.qalb-debugged ldc-1-tagged --batch_size=256 --model_name=tagged-1-batchsize-256 --max_sentence_length=150 --decode=ai/datasets/data/arabizi/ldc-1-tagged-dev.arabizi --extension=arabizi --beam_size=5 --output_path=output/tagged-1-batchsize-256/decoder_dev.out
python ai/tests/accuracy-script/accuracy.py output/tagged-1-batchsize-256/decoder_dev.out ai/datasets/data/arabizi/ldc-1-tagged-dev.gold

--- stop n check for accuracy
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
python -m ai.tests.qalb-debugged ldc-1-tagged --batch_size=256 --model_name=tagged-1-batchsize-256 --max_sentence_length=150 --decode=ai/datasets/data/arabizi/ldc-1-tagged-dev.arabizi --extension=arabizi --beam_size=5 --output_path=output/tagged-1-batchsize-256/decoder_dev.out
python ai/tests/accuracy-script/accuracy.py output/tagged-1-batchsize-256/decoder_dev.out ai/datasets/data/arabizi/ldc-1-tagged-dev.gold


script 3: tagged-1-rnn-1.sh
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

python -m ai.tests.qalb-debugged ldc-1-tagged --rnn_layers=1 --model_name=tagged-1-rnn-1 --max_sentence_length=150 --extension=arabizi --output_path=output/tagged-1-rnn-1
python -m ai.tests.qalb-debugged ldc-1-tagged --rnn_layers=1 --model_name=tagged-1-rnn-1 --max_sentence_length=150 --decode=ai/datasets/data/arabizi/ldc-1-tagged-dev.arabizi --extension=arabizi --beam_size=5 --output_path=output/tagged-1-rnn-1/decoder_dev.out
python ai/tests/accuracy-script/accuracy.py output/tagged-1-rnn-1/decoder_dev.out ai/datasets/data/arabizi/ldc-1-tagged-dev.gold

script 4: tagged-1-rnn-3.sh
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

python -m ai.tests.qalb-debugged ldc-1-tagged --rnn_layers=3 --model_name=tagged-1-rnn-3 --max_sentence_length=150 --extension=arabizi --output_path=output/tagged-1-rnn-3
python -m ai.tests.qalb-debugged ldc-1-tagged --rnn_layers=3 --model_name=tagged-1-rnn-3 --max_sentence_length=150 --decode=ai/datasets/data/arabizi/ldc-1-tagged-dev.arabizi --extension=arabizi --beam_size=5 --output_path=output/tagged-1-rnn-3/decoder_dev.out
python ai/tests/accuracy-script/accuracy.py output/tagged-1-rnn-3/decoder_dev.out ai/datasets/data/arabizi/ldc-1-tagged-dev.gold

------- Working on Feb 12 -------

python tag.py ldc-train.arabizi ldc-train.gold ldc-3-tagged-train.arabizi ldc-3-tagged-train.gold ldc-3-train.lines 3
python tag.py ldc-dev.arabizi ldc-dev.gold ldc-3-tagged-dev.arabizi ldc-3-tagged-dev.gold ldc-3-dev.lines 3

script 1: tagged-3.sh
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

python -m ai.tests.qalb-debugged ldc-3-tagged --model_name=tagged-3 --max_sentence_length=150 --extension=arabizi --output_path=output/tagged-3
python -m ai.tests.qalb-debugged ldc-3-tagged --model_name=tagged-3 --max_sentence_length=150 --decode=ai/datasets/data/arabizi/ldc-3-tagged-dev.arabizi --extension=arabizi --beam_size=5 --output_path=output/tagged-3/decoder_dev.out
python ai/tests/accuracy-script/accuracy.py output/tagged-3/decoder_dev.out ai/datasets/data/arabizi/ldc-3-tagged-dev.gold