# Transliteration Tool

There are 4 components of this tool. We will demostrate the use of each component using the [LDC BOLT Egyptian Arabic SMS/Chat and Transliteration](https://catalog.ldc.upenn.edu/LDC2017T07) data to transliterate Arabizi to Arabic.

This readme also contains a repository structure at the end.

## 1. Data Extraction from LDC XML Files
Download the [data](https://catalog.ldc.upenn.edu/LDC2017T07) and unzip the downloaded file. The annotated Arabizi-Arabic transliterated parallel corpus resides in bolt_sms_chat_ara_src_transliteration/data/transliteration as folder as xml files. We use these for training and testing of our tool. There are also unannotated Arabizi-only files in bolt_sms_chat_ara_src_transliteration/data/source; these are used for training word-embeddings using Fasttext.

### Extracting Data Splits: Train, Dev & Test

We split the chat and SMS transliteration files in the following way:
- Train: CHT_ARZ_{20121228.0001-20150101.0002} and SMS_ARZ_{20120223.0001-20130902.0002}
- Dev: CHT_ARZ_{20120130.0000-20121226.0003} and SMS_ARZ_{20110705.0000-20120220.0000}
- Test: CHT_ARZ_{20150101.0008-20160201.0001} and SMS_ARZ_{20130904.0001-20130929.0000}.

You can find the exact files for each split in this repo in split_ldc folder. The files are train.txt, dev.txt, and test.txt. These txt files can be used to move the xml files of a specific split into a separate folder using the script makeNewLDCSplits.py in splits_ldc folder. 

1. To split the xml files into train, dev and test, run the following three commands (one command for each split):

```unix
# train
python3 splits_ldc/makeSplits.py bolt_sms_chat_ara_src_transliteration/data/transliteration/ splits_ldc/train.txt splits_ldc/train/xml_files

# dev
python3 splits_ldc/makeSplits.py bolt_sms_chat_ara_src_transliteration/data/transliteration/ splits_ldc/dev.txt splits_ldc/dev/xml_files

# test
python3 splits_ldc/makeSplits.py bolt_sms_chat_ara_src_transliteration/data/transliteration/ splits_ldc/test.txt splits_ldc/test/xml_files
```

Now the xml files for each split will reside in the specific folder of the split. Next, extract data from these XML files.

2. Extract the source and target. To do this run the following three commands (one command for each split)

```unix
# training data
python3 splits_ldc/getSourceAndTarget.py splits_ldc/train/xml_files/ splits_ldc/train/train-source.arabizi splits_ldc/train/train-word-aligned-target.gold splits_ldc/train/train-sentence-aligned-target.gold

# dev data
python3 splits_ldc/getSourceAndTarget.py splits_ldc/dev/xml_files/ splits_ldc/dev/dev-source.arabizi splits_ldc/dev/dev-word-aligned-target.gold splits_ldc/dev/dev-sentence-aligned-target.gold

# test data
python3 splits_ldc/getSourceAndTarget.py splits_ldc/test/xml_files/ splits_ldc/test/test-source.arabizi splits_ldc/test/test-word-aligned-target.gold splits_ldc/test/test-sentence-aligned-target.gold
```

The difference between word-aligned-target.gold files and sentences-aligned-target.gold files is the presence and absence of [+] and [-] tokens.

At this point in each of the split folders (train, dev and test) there will be there files: source.arabizi, word-aligned-target.gold, and sentence-aligned-target.gold.

### Extracting Unannotated Arabizi Data

We also extract data from the unannotated Arabizi files. This data is used to train Fasttext for pre-trained word embeddings. The files include train, dev and test Arabizi lines and many more (they have ~1M word). However, in order to make sure that dev and test lines are unseen, we exclude them when extracting all lines. To do this, simply run the following command:

```unix
python3 splits_ldc/getSourceArabiziWithoutDevAndTest.py bolt_sms_chat_ara_src_transliteration/data/source splits_ldc/dev/xml_files splits_ldc/test/xml_files splits_ldc/source/source-without-dev-test.arabizi
```

### Training Fasttext with Unannotated Arabizi Data

Download fasttext at the root folder level by the following commands:

```unix
git clone https://github.com/facebookresearch/fastText.git

cd fastText

make
```

Now train word-embeddings on the unannotated arabizi data we extracted (without dev and test) using Fasttext. First, preprocess the data and then start training.

```unix
# Preprocess

cd ../ #move up one directory to come back to the root
python3 helpers/preprocess_fasttext_data.py --input_file=splits_ldc/source/source-without-dev-test.arabizi --output_file=splits_ldc/source/source-without-dev-test-preprocessed.arabizi

# Word-embeddings training
./fastText/fasttext skipgram -input splits_ldc/source/source-without-dev-test-preprocessed.arabizi -output pretrained_word_embeddings/arabizi_300_narrow -dim 300 -minn 2 -ws 2
```

This will save a .bin files at the output directory specified in the command. This bin file will be used in training to feed pre-trained word embeddings.

## 2. Training

## 3. Prediction with Evaluation

## 4. Prediction without Evaluation

# Repository Structure