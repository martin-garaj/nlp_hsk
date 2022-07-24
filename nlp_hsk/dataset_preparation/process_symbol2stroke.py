"""
AUTHOR: Martin Garaj PhD.
DATE: 2022/07/23
LICENSE: MIT
CONTRIBUTORS: "YOUR_NAME_HERE", 

This script takes:
    /HSK/processed_data/list_of_HSK_symbols.pickle
    /webscaping/hanzi_net/raw_files/dict_symbols_and_radical2hanzi_kanji.pickle
And produces a human-readable file including a dictionary of 
symbols -> strokes.
"""

#%% Imports
from pathlib import Path
import pickle
from _support_functions import save2file
import os

#%% Inputs
# input files
path_list_of_HSK_symbols = 'HSK/processed_data/list_of_HSK_symbols.pickle'
path_dict_symbols_and_radical2hanzi_kanji = \
    'webscraping/hanzi_net/raw_files/' \
    'dict_symbols_and_radical2hanzi_kanji.pickle'

# path to output file
path_output_file = '../dataset'
# derive the output name from the scipt name
output_name = \
    os.path.basename(__file__).replace('process_','').replace('.py','')

# True for debugging, false for full-processing
DEBUG = False

#%% Process data
# load input data
with open(Path(path_list_of_HSK_symbols), 'rb') as handle:
    list_of_HSK_symbols = pickle.load(handle)
with open(Path(path_dict_symbols_and_radical2hanzi_kanji), 'rb') as handle:
    dict_symbols_and_radical2hanzi_kanji = pickle.load(handle)

# debugging - process only several symbols
if DEBUG:
    # use the following limited dataset to set teh functionality
    list_of_HSK_symbols = list_of_HSK_symbols[0:5]

# create dict storing the processed output symbol2radical
dictionary = dict()

# loop through symbols
for symbol in list_of_HSK_symbols:
    # add symbol
    dictionary[symbol] = \
        dict_symbols_and_radical2hanzi_kanji[symbol]['strokes']
    
#%% Store the processed data
save2file(dictionary, output_name, path_output_file)

