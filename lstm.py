"""Automatic generation of text similar to a given input document.

Usage:
  lstm.py train [-i <file>] [--maxlen <l>]
                [--checkpoint_path <p>] [--no_autoload]
  lstm.py generate [-o <file>]
                   [-c <n>] [--maxlen <l>] [--temperature <T>]
  lstm.py -h | --help

Options:
  -h --help
  -i <file> --input <file>   Input text file [default: input.txt]
  -o <file> --output <file>  Output generated file [default: output.txt]
  -c <n> --count <n>         Number of characters generated [default: 1000]
  --maxlen <l>               Maximum length of sequences [default: 20]
  --temperature <T>          Novelty in the generation, usually between 0. and 2.
                             If not provided, output will be generated with
                             several temperatures [default: 1.0]
  --checkpoint_path <p>      Name of the model snapshots that will be saved at
                             each checkpoint. [default: model-save]
  --no_autoload              Do not load the last saved checkpoint model even
                             if it exists
"""

from __future__ import absolute_import, division, print_function
import os, sys, re
import pickle
import tflearn
from tflearn.data_utils import *
from docopt import docopt

""" Build dataset from textfile: input data, labels and dictionary"""
def build_dataset(input, maxlen, char_idx=None, char_idx_file='char_idx.pickle'):
    X, Y, char_idx = \
        textfile_to_semi_redundant_sequences(input, seq_maxlen=maxlen,
            redun_step=3, pre_defined_char_idx=char_idx)
    pickle.dump(char_idx, open(char_idx_file,'wb'))
    return X, Y, char_idx

""" Load a saved dictionary from a file"""
def load_dictionary(char_idx_file='char_idx.pickle'):
    char_idx = None
    if os.path.isfile(char_idx_file):
        print('Loading dictionary from %s' % char_idx_file)
        char_idx = pickle.load(open(char_idx_file, 'rb'))
    return char_idx

""" Build the deep neural network model for generating sequences"""
def build_model(maxlen, char_idx, checkpoint_path):
    g = tflearn.input_data([None, maxlen, len(char_idx)])
    g = tflearn.lstm(g, 512, return_seq=True)
    g = tflearn.dropout(g, 0.5)
    g = tflearn.lstm(g, 512, return_seq=True)
    g = tflearn.dropout(g, 0.5)
    g = tflearn.lstm(g, 512)
    g = tflearn.dropout(g, 0.5)
    g = tflearn.fully_connected(g, len(char_idx), activation='softmax')
    g = tflearn.regression(g, optimizer='adam', loss='categorical_crossentropy',
                           learning_rate=0.001)

    return tflearn.SequenceGenerator(g, dictionary=char_idx,
                                     seq_maxlen=maxlen,
                                     clip_gradients=5.0,
                                     checkpoint_path=checkpoint_path)

""" Load a saved model from a file"""
def load_model(model):
    if os.path.isfile('checkpoint'):
        f = open('checkpoint', 'r')
        regex = re.compile('model_checkpoint_path:\s\"(.*)\"')
        filename = regex.findall(f.read())
        if filename:
            print('Loading model from %s' % filename[0])
            model.load(filename[0])

""" Build or load the dataset, dictionary and model"""
def prepare(parameters, dataset_needed=False):
    if not parameters['--no_autoload']:
        char_idx = load_dictionary()
    if not char_idx or dataset_needed:
        X, Y, char_idx = build_dataset(parameters['--input'], parameters['--maxlen'], char_idx)
    else:
        X, Y = None, None
    model = build_model(parameters['--maxlen'], char_idx, parameters['--checkpoint_path'])
    if not parameters['--no_autoload']:
        load_model(model)
    return model, X, Y

""" Train a model on the input dataset"""
def train(parameters):
    model, X, Y = prepare(parameters, dataset_needed=True)
    for i in range(50):
        model.fit(X, Y, validation_set=0.1, batch_size=128,
            n_epoch=1, run_id='lstm')

        print("-- TESTING...")
        seed = random_sequence_from_textfile(parameters['--input'], parameters['--maxlen'])
        print("-- Test with temperature of 1.0 --")
        print(model.generate(600, temperature=1.0, seq_seed=seed))
        print("-- Test with temperature of 0.5 --")
        print(model.generate(600, temperature=0.5, seq_seed=seed))
        print("-- Test with temperature of 0.25 --")
        print(model.generate(600, temperature=0.25, seq_seed=seed))
    f.close()

""" Generate new content from the trained model"""
def generate(parameters):
    model, _, _ = prepare(parameters)
    seed = random_sequence_from_textfile(parameters['--input'], parameters['--maxlen'])
    print("Generating", parameters['--count'],
        "characters with a temperature of", parameters['--temperature'],'...')
    s = model.generate(parameters['--count'],
                       temperature=parameters['--temperature'],
                       seq_seed=seed)
    with open(parameters['--output'], 'w') as f:
      f.write(s)

""" Cast numeric parameters"""
def cast_parameters(parameters):
    parameters['--count'] = int(parameters['--count'])
    parameters['--maxlen'] = int(parameters['--maxlen'])
    parameters['--temperature'] = float(parameters['--temperature'])
    return parameters

if __name__ == '__main__':
    parameters = cast_parameters(docopt(__doc__))
    if parameters['train']:
        train(parameters)
    elif parameters['generate']:
        generate(parameters)
