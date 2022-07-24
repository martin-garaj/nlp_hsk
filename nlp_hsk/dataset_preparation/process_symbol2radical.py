"""
AUTHOR: Martin Garaj PhD.
DATE: 2022/07/23
LICENSE: MIT
CONTRIBUTORS: "YOUR_NAME_HERE", 

This script takes:
    /HSK/processed_data/list_of_HSK_symbols.pickle
    /webscaping/hanzi_net/raw_files/dict_symbols_and_radical2hanzi_kanji.pickle
And produces a human-readable file including a dictionary of 
symbols -> radicals.
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

#%% Functions
def recursively_search_radicals(radical, 
                                structure_to_search,
                                dictionary_to_grow,
                                debug=False):
    """
    Recursively search "radical" in "structure_to_grow" and add the results 
    to "dictionary_to_grow" until the "structure_to_search" doesnt include 
    sub-radicals.

    Parameters
    ----------
    radical : <char>
        DESCRIPTION.
    structure_to_search : <dict>
        Dictionary containing symbols decomposed to radicals.
    dictionary_to_grow : <dict>
        Dictionary that will grow, until there is no more radicals to add.
    Returns
    -------
    dictionary_to_grow

    """
    if radical in structure_to_search.keys():
        sub_radicals = structure_to_search[radical]['compositions']
        # remove sub_radicals that are the same as the radical
        for sub_radical in sub_radicals:
            # remove if duplicate
            if radical == sub_radical:
                sub_radicals.remove(sub_radical)

        # count the radicals after removing duplicates
        num_radicals = len(sub_radicals)
    else:
        # this condition braks the loop
        num_radicals = 0
    
    if radical in structure_to_search.keys() and num_radicals > 0:
        if debug:
            print(radical+": "+','.join(sub_radicals))
        for sub_radical in sub_radicals:
            dictionary_to_grow[sub_radical] = \
                recursively_search_radicals(sub_radical,
                                            structure_to_search,
                                            {},
                                            debug=debug)
    # return only-non-empty dictionary
    if len(dictionary_to_grow) > 0:
        return dictionary_to_grow
    # do not return empty dictionary, return None instead
    else:
        return None

#%% Process data
# load input data
with open(Path(path_list_of_HSK_symbols), 'rb') as handle:
    list_of_HSK_symbols = pickle.load(handle)
with open(Path(path_dict_symbols_and_radical2hanzi_kanji), 'rb') as handle:
    dict_symbols_and_radical2hanzi_kanji = pickle.load(handle)

# debugging - process only several symbols
if DEBUG:
    # use following articisal dataset to construct     
    list_of_HSK_symbols = 'a'
    dict_symbols_and_radical2hanzi_kanji['a']['compositions'] = ['b', 'B', '1']
    dict_symbols_and_radical2hanzi_kanji['b']['compositions'] = ['c', 'K']
    dict_symbols_and_radical2hanzi_kanji['B']['compositions'] = ['C']
    dict_symbols_and_radical2hanzi_kanji['c']['compositions'] = ['d']
    dict_symbols_and_radical2hanzi_kanji['C']['compositions'] = ['D']
    # for instance the following is an example of a case, when the recursion 
    # throws a RecursionError, since the 'D' is 2 levels BELOW and depends 
    # on 'B' which leads the recursion 2 levels UP, thus looping indefinitely.
    # dict_symbols_and_radical2hanzi_kanji['D']['compositions'] = ['B']

# create dict storing the processed output
dictionary = dict()

# loop through symbols
for symbol in list_of_HSK_symbols:
    # add symbol
    dictionary[symbol] = dict()
    
    try:
        dictionary[symbol] = \
            recursively_search_radicals(radical = symbol, 
                structure_to_search = dict_symbols_and_radical2hanzi_kanji,
                dictionary_to_grow = {},
                debug=DEBUG)
    except RecursionError:
        print('RecursionError: it seems like some sub-radicals of '+symbol\
              +' depend on each other, or in other words, one radical has a'\
              +' sub-radical, and that sun-radical has a sub-radical which is'\
              +' the same as the radical. This exception should logically not'\
              +' happen, since the symbols/radical/sub-radicals are being'\
              +' decomposed into SMALLER parts. Therefore every new level of'\
              +' decomposition has to be logically a subset of the pervious'\
              +' thus it cannot contain elements from super-set.')                
    
#%% Store the processed data
save2file(dictionary, output_name, path_output_file)
