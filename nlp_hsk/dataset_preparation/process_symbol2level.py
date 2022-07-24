"""
AUTHOR: Martin Garaj PhD.
DATE: 2022/07/23
LICENSE: MIT
CONTRIBUTORS: "YOUR_NAME_HERE", 

This script takes:
    /HSK/processed_data/list_of_HSK_symbols.pickle
    /HSK/processed_data/df_HSK_vocab.pickle
And produces a human-readable file including a dictionary of 
symbols -> level.
"""

#%% Imports
from pathlib import Path
import pickle
from _support_functions import save2file
import os
from collections import defaultdict

#%% Inputs
# input files
path_list_of_HSK_symbols = 'HSK/processed_data/list_of_HSK_symbols.pickle'
path_df_HSK_vocab = 'HSK/processed_data/df_HSK_vocab.pickle'
    

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
with open(Path(path_df_HSK_vocab), 'rb') as handle:
    df_HSK_vocab = pickle.load(handle)

# debugging - process only several symbols
if DEBUG:
    # use the following limited dataset to set teh functionality
    df_HSK_vocab = df_HSK_vocab.loc[[0,1,2,3,4,5]]

# # create dict storing the processed output
# get all symbols and the related HSK level
dictionary = dict()
# get all non-chinese symbols
list_other_chars = []

# collect all chinese and non-chinese characters
for index, row in df_HSK_vocab.iterrows():
    # get HSK level
    HSK_level = row['HSK_level']
    # get symbols (including other non-chinese symbols)
    all_chars = row['symbol']
    
    for char in all_chars:
        # check for chinese symbol
        if( char >= u'\u4e00' and u'\u9fff' >= char ):
            # check if it is already added
            if(char not in dictionary.keys()):
                dictionary[char] = list()
                # add character and the level
                dictionary[char].append(HSK_level)
            else:
                # check for duplicate level 
                if(HSK_level not in dictionary[char]):
                    # add new level
                    dictionary[char].append(HSK_level)
                    # sort
                    dictionary[char].sort()
                else:
                    # prevent duplicating levels in dictionary
                    pass 
        # also collect non-chinese characters
        else:
            # check if it is already added
            if(char not in list_other_chars):
                # add character to the list
                list_other_chars.append(char)
    
print('Other characters present in df_HSK_vocab '+','.join(list_other_chars))    
    
if list_of_HSK_symbols.sort() != list(df_HSK_vocab.keys()).sort():
    raise ValueError('There seems to be a problem, where the total number of'\
                     +' symbols is inconsistent when compared to'\
                     +' "list_of_HSK_symbols", which is a colelctiona of'\
                     +' parsed symbols from "df_HSK_vocab"')

# #%% Store the processed data
save2file(dictionary, output_name, path_output_file)
