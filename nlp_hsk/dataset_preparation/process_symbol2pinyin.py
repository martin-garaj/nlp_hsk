"""
AUTHOR: Martin Garaj PhD.
DATE: 2022/07/23
LICENSE: MIT
CONTRIBUTORS: "YOUR_NAME_HERE", 

This script takes:
    /HSK/processed_data/list_of_HSK_symbols.pickle
    /webscaping/hanzi_net/raw_files/path_dict_symbols2mdbg_pinyin_and_phrase.pickle
And produces a human-readable file including a dictionary of 
symbols -> pinyin.
"""

#%% Imports
from pathlib import Path
import pickle
from _support_functions import save2file
import re 
import os

#%% Inputs
# input files
path_list_of_HSK_symbols = 'HSK/processed_data/list_of_HSK_symbols.pickle'
path_dict_symbols2mdbg_pinyin_and_phrase = \
    'webscraping/mdbg/raw_files/' \
    'dict_symbols2mdbg_pinyin_and_phrase.pickle'

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
with open(Path(path_dict_symbols2mdbg_pinyin_and_phrase), 'rb') as handle:
    dict_symbols2mdbg_pinyin_and_phrase = pickle.load(handle)

# debugging - process only several symbols
if DEBUG:
    # use the following limited dataset to set teh functionality
    list_of_HSK_symbols = list_of_HSK_symbols[0:5]

# create dict storing the processed output
dictionary = dict()

# loop through symbols
for symbol in list_of_HSK_symbols:
    # pinyins as strings
    str_pinyins = list()
    # get all pinyins for the particular symbol
    for row in dict_symbols2mdbg_pinyin_and_phrase[symbol]:
        # check both 'value' and 'hanzi', if it matches the symbol, 
        # get the pinyin
        if row['value'] == symbol or row['hanzi'] == symbol:
            str_pinyins.append(row['pinyin'])
    
    if len(str_pinyins) == 0:
        print('WARNING: the symbol '+symbol+' has no pinyin in MDBG data,' \
              +' wider search is applied.')
        # get all pinyins for the particular symbol by widening the search 
        # within phrases, not just single symbols
        for row in dict_symbols2mdbg_pinyin_and_phrase[symbol]:
            # locate the symbol within phrases using 'value' field
            if symbol in row['value']:
                # find position of the first symbol occurance
                symbol_pos = row['value'].find(symbol)
                # cut the pinyin into separate pieces
                pinyin_list = row['pinyin'].split(' ')
                # get pinyin belonging to the symbol
                pinyin_symbol = pinyin_list[symbol_pos]
                # append pinyin to strings of pinyins
                str_pinyins.append(pinyin_symbol)
                
                # check whether 'value' and 'hanzi' are the same, 
                # if not continue processing 'hanzi' the same way
                if row['value'] != row['hanzi']:
                    # locate the symbol within phrases using 'hanzi' field
                    if symbol in row['hanzi']:
                        # find position of the first symbol occurance
                        symbol_pos = row['hanzi'].find(symbol)
                        # cut the pinyin into separate pieces
                        pinyin_list = row['pinyin'].split(' ')
                        # get pinyin belonging to the symbol
                        pinyin_symbol = pinyin_list[symbol_pos]
                        # append pinyin to strings of pinyins
                        str_pinyins.append(pinyin_symbol)
        
        if len(str_pinyins) > 0:
            print('Successfully located pinyin from phrases: '\
                  +','.join(str_pinyins))
        else:
            raise ValueError('No pinyin has been found for symbol '+symbol)
            
    # process pinyins to get a list of tuples 
    # (pinyin split to string for pronounciation and integer for tone)
    pinyins = list()
    for str_pinyin in str_pinyins:
        # get tone, if there is no tone specified, use None
        tone = re.findall('[0-9]+', str_pinyin)
        if len(tone) > 1:
            print('ERROR: multiple tones are detected for symbol '+symbol)
        else:
            tone = tone[0]
        tone = None if tone=='' else int(tone)
        # remove tone from pronounciation
        pronounciation = str_pinyin.replace(str(tone), '')
        pronounciation = None if pronounciation=='' else pronounciation.lower()
        # make it into tuple
        pinyin = tuple([pronounciation, tone])
        # append to the list, but prevent duplicates
        if pinyin not in pinyins:
            pinyins.append(pinyin)
        
    # keep the list of tuples in a dictionary
    dictionary[symbol] = pinyins
    
#%% Store the processed data
save2file(dictionary, output_name, path_output_file)
