"""This module takes care of all data parsing for the Qatar Arabic Language
   Bank (QALB) dataset released in 2015; including both the L1 dataset of
   corrections from native speakers and the L2 dataset of corrections from
   mistakes made by students of Arabic as a foreign language."""

from __future__ import print_function

from abc import ABCMeta, abstractmethod
import os

from six.moves import xrange
import numpy as np

from ai.datasets import BaseDataset


def parse_correction(correction_line):
  """Parse a raw line describing corrections into data, with the format
     (start_id, end_id, correction_type, correction_content). The type can be:
     (1) add_token_before -- insert a token in front of another token
     (2) merge -- merge multiple tokens
     (3) split -- split a token into multiple tokens
     (4) delete_token -- delete a token
     (5) edit -- replace a token with a different token
     (6) move_before -- move a token to a new location in the sentence."""
  correction_line = correction_line[2:].split('|||')  # remove the A marker
  start_id, end_id = map(int, correction_line[0].split())
  return (start_id, end_id, correction_line[1], correction_line[2])

def apply_corrections(text, corrections):
  """Given a text string and a list of corrections in the format returned by
     the `parse_correction` method, return a string of corrected text. Note
     this method is not at all optimized and uses lists."""
  words = text.split()
  # Reverse the corrections to avoid modifying indices (corrections are sorted)
  for start, end, _, content in reversed(corrections):
    # All corrections can be handled with this line (neat!!!)
    words = words[:start] + content.split() + words[end:]
  return ' '.join(words) + '\n'

def max_length_seq(pairs):
  """Get the maximum sequence length of the examples in the provided pairs."""
  return [max(map(len, seq)) for seq in zip(*pairs)]


class BaseQALB(BaseDataset):
  """Abstract class for QALB data parsing. This parent class takes care of
     reading and preprocessing the data files, and children classes can specify
     different tokenizations (word-based, character-based, etc)."""
  __metaclass__ = ABCMeta
  
  def __init__(self, file_root, extension='.sbw', **kw):
    """Arguments:
       `file_root`: the root name of the files in the data/qalb directory.
        The constructor searches for .*.sent, .*.m2, where * is train and dev.
       Keyword arguments:
       `extension`: name of the data file extensions (or none if it's falsy).
       Note on usage: to account for the _GO and _EOS tokens that the labels
       have inserted, if the maximum length sequences are in the labels, use
       two extra time steps if the goal is to not truncate anything."""
    super(BaseQALB, self).__init__(**kw)
    self.file_root = file_root
    if not extension:
      extension = ''
    self.extension = extension
    data_dir = os.path.join('ai', 'datasets', 'data', 'qalb')
    # Prepare training data
    train_input_path = os.path.join(
      data_dir, self.file_root + '.train.sent' + self.extension
    )
    train_labels = self.flatten_gold(
      os.path.join(data_dir, self.file_root + '.train')  # method completes it
    )
    with open(train_input_path) as train_file:
      self.train_pairs = self.make_pairs(train_file.readlines(), train_labels)
    # Prepare validation data
    valid_input_path = os.path.join(
      data_dir, self.file_root + '.dev.sent' + self.extension
    )
    valid_labels = self.flatten_gold(
      os.path.join(data_dir, self.file_root + '.dev')
    )
    with open(valid_input_path) as valid_file:
      self.valid_pairs = self.make_pairs(valid_file.readlines(), valid_labels)
  
  def flatten_gold(self, file_root):
    """Create and return the contents a provided filename that generates a
       parallel corpus to the inputs, following the corrections provided in the
       default gold file m2 format. Note that this step is necessary for
       seq2seq training, and code cannot be borrowed from the evaluation script
       because it never flattens the system output; instead, it finds the
       minimum number of corrections that map the input into the output."""
    with open(file_root + '.m2' + self.extension) as m2_file:
      raw_m2_data = m2_file.read().split('\n\n')[:-1]  # remove last empty str
    result = []
    for raw_pair in raw_m2_data:
      text = raw_pair.split('\n')[0][2:]  # remove the S marker
      corrections = map(parse_correction, raw_pair.split('\n')[1:])
      result.append(apply_corrections(text, corrections))
    with open(file_root + '.gold' + self.extension, 'w') as gold_file:
      gold_file.writelines(result)
    return result
  
  def make_pair(self, input_line, label_line):
    """Given an input and label in text or list form, convert the n-grams to
       their unique type id's. This also takes care of padding and adding
       other tokens that are helpful for the decoder RNN. If the arguments are
       strings, the `tokenize` method will iterate over the strings resulting
       in character-level types. If they are iterables instead, the method will
       use the elements (or their n-grams) as their types."""
    # This already takes care of making the n-grams their own unique types.
    input_ids = self.tokenize(input_line)
    label_ids = self.tokenize(label_line)
    label_ids.append(self.type_to_ix['_EOS'])
    return input_ids, label_ids
  
  @abstractmethod
  def get_batch(self):
    """Return a batch of examples according to the `batch_size` attribute.
       This method must be overriden because the seq2seq task could use batches
       from buckets or dynamically pad the batches based on what was drawn."""
    pass
  
  # TODO: make two different methods for pair making in parent class to avoid
  # child method with different arguments. One method to make the pairs from
  # respective train and validation files, and one to make the pairs from a
  # single file and allowing to specify the ratio of data used for training.
  # pylint: disable=signature-differs
  @abstractmethod
  def make_pairs(self, input_lines, label_lines):
    """Given the raw input and label text lines, process and save the pairs
       into attributes. This method must be overriden because it is unclear
       whether to call the `make_pair` method with words or characters."""
    pass


class DynamicQALB(BaseQALB):
  """Non-bucket based data parser for QALB dataset."""
  
  def __init__(self, file_root, max_input_length=None, max_label_length=None,
               **kw):
    """Extra keyword arguments:
       `max_input_length`: maximum sequence length for the inputs,
       `max_label_length`: maximum sequence length for the labels."""
    super(DynamicQALB, self).__init__(file_root, **kw)
    self.max_input_length = max_input_length
    self.max_label_length = max_label_length
  
  def get_batch(self, draw_from_valid=False):
    """Draw random examples and pad them to the largest sequence drawn.
       The batch can be drawn from the validation set if the keyowrd argument
       `draw_from_valid` is set to True."""
    batch = []
    while len(batch) < self.batch_size:
      if draw_from_valid:
        sequence = self.valid_pairs[np.random.randint(len(self.valid_pairs))]
      else:
        sequence = self.train_pairs[np.random.randint(len(self.train_pairs))]
      if len(sequence[0]) <= self.max_input_length and \
         len(sequence[1]) <= self.max_label_length:
        batch.append(sequence)
    for i in xrange(self.batch_size):
      max_input_length = self.max_input_length
      max_label_length = self.max_label_length
      if max_input_length is None or max_label_length is None:
        max_input_length, max_label_length = max_length_seq(batch)
      while len(batch[i][0]) < max_input_length:
        batch[i][0].append(self.type_to_ix['_PAD'])
      while len(batch[i][1]) < max_label_length:
        batch[i][1].append(self.type_to_ix['_PAD'])
    return zip(*batch)  # return as (batch_of_inputs, batch_of_labels)


class BucketQALB(BaseQALB):
  """Bucket-based data parser for QALB dataset."""
  
  def __init__(self, file_root, buckets=None, **kw):
    """TODO: add documentation for buckets"""
    super(BucketQALB, self).__init__(file_root, **kw)
    self.buckets = buckets
    self.pad_and_bucket_pairs()
  
  def pad_and_bucket_pairs(self):
    """Adds padding to the inputs and labels, depending on the initialized
       buckets. Note this method requires the `train_pairs` and `valid_pairs`
       attributes to be fully built by the `make_pairs` method, and that they
       will be changed to the form (bucket_1, ..., bucket_k)."""
    if not self.buckets:
      # Get the max lengths of the input and label sequences (quick one-liners)
      # pylint: disable=deprecated-lambda
      max_train = max_length_seq(self.train_pairs)
      max_valid = max_length_seq(self.valid_pairs)
      # Build single bucket with the max of each so everything can be fed
      self.buckets = [map(max, zip(max_train, max_valid))]
    # Actually do the padding
    temp_train_pairs = [[] for _ in self.buckets]
    temp_valid_pairs = [[] for _ in self.buckets]
    for i, pair_set in enumerate([self.train_pairs, self.valid_pairs]):
      for input_seq, label_seq in pair_set:
        for b_id, (max_i, max_l) in enumerate(self.buckets):
          if len(input_seq) <= max_i and len(label_seq) <= max_l:
            while len(input_seq) < max_i:
              input_seq.append(self.type_to_ix['_PAD'])
            while len(label_seq) < max_l:
              label_seq.append(self.type_to_ix['_PAD'])
            if i == 0:
              temp_train_pairs[b_id].append([input_seq, label_seq])
            else:
              temp_valid_pairs[b_id].append([input_seq, label_seq])
            break
    self.train_pairs = temp_train_pairs
    self.valid_pairs = temp_valid_pairs
  
  def get_batch(self):
    """Pick a bucket randomly and make a batch of random examples from it."""
    # TODO: make this precisely match the distribution of the bucket contents
    bucket_id = np.random.randint(len(self.buckets))
    pairs = self.train_pairs[bucket_id]
    return [pairs[np.random.randint(len(pairs))]
            for _ in xrange(self.batch_size)]


class CharQALB(BaseQALB):
  """Character-level data parser for QALB dataset."""
  
  def make_pairs(self, input_lines, label_lines):
    pairs = []
    for i in xrange(len(input_lines)):
      # Remove the document id (first word) and truncate to max char length
      input_line = ' '.join(input_lines[i].split()[1:])
      label_line = label_lines[i]
      pairs.append(self.make_pair(input_line, label_line))
    return pairs


class WordQALB(BaseQALB):
  """Word-level data parser for QALB dataset."""
  
  def make_pairs(self, input_lines, label_lines):
    pairs = []
    for i in xrange(len(input_lines)):
      # Compensate for document id
      input_line = input_lines[i].split()[1:]
      label_line = label_lines[i].split()
      pairs.append(self.make_pair(input_line, label_line))
    return pairs