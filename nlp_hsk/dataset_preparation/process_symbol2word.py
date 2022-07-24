"""
AUTHOR: Martin Garaj PhD.
DATE: 2022/07/23
LICENSE: MIT
CONTRIBUTORS: "YOUR_NAME_HERE", 

This script takes:
    /HSK/processed_data/list_of_HSK_symbols.pickle
    /webscaping/hanzi_net/raw_files/dict_symbols_and_radical2hanzi_kanji.pickle
And produces a human-readable file including a dictionary of 
symbols -> phrases.
"""

#%% Imports
from pathlib import Path
import pickle
from _support_functions import save2file
from _support_functions import locate_ignored_characters_in_context
import os

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

list_other_chars = ['｜','（','）','、','〇',' ','¹','²','…']

ignore_substrings_including_symbols = \
    ['形', '量', '副', '动', '代', '名', '数', '助', '介', '连', '叹', ]

check_ignored_symbols_in_valid_context = list()


dictionary = dict()

phrases = list()

# collect all chinese and non-chinese characters
for index, row in df_HSK_vocab.iterrows():
    phrase = ''
    # get HSK level
    HSK_level = row['HSK_level']
    # get symbols (including other non-chinese symbols)
    valid_substring = row['symbol']
    
    # clean extra symbols
    valid_substring = valid_substring.replace('¹', '')
    valid_substring = valid_substring.replace('²', '')
    valid_substring = valid_substring.replace('…', '')
    valid_substring = valid_substring.replace(' ', '')
    
    # remove ABBREVIATIONS
    if '｜' in valid_substring:
        index_or = valid_substring.find('｜')
        valid_substring = valid_substring[0:index_or]
        invalid_substring = valid_substring.replace(valid_substring, '')
        if DEBUG:
            print('ABBREV: '+invalid_substring+' was removed from '\
                  +valid_substring+invalid_substring\
                  +', the result is '+valid_substring)
                
    # remove invalid symbols without meaning
    invalid_substring, check_ignored_symbols_in_valid_context = \
        locate_ignored_characters_in_context(ignore_substrings_including_symbols,
        valid_substring,
        check_ignored_symbols_in_valid_context)
    if isinstance(invalid_substring, str):
        if DEBUG:
            print('IGNORE: '+invalid_substring+' in '+valid_substring)
        valid_substring = valid_substring.replace(invalid_substring, '')

    # at this point, all the symbols are valid, 
    # even if they are in between brackets, therefore check the content 
    # between brackets and decide how to use it
    bracket_start_index = valid_substring.find('（')
    bracket_end_index = valid_substring.find('）')
    if (bracket_start_index+bracket_end_index) == -2:
        # the strind is definitely valid, lets use it as it is
        phrase = valid_substring
        pass
    else:
        use_in_between_brackets = False
        # decide whether to use the string in between brackets
        between_brackets = \
            valid_substring[bracket_start_index+1:bracket_end_index]
        for char in valid_substring:
            if char == '（':
                # I need to decide what to use
                
                # stopr processing any further, I already have the very 
                # final output
                break
            if( char >= u'\u4e00' and u'\u9fff' >= char ):
                if char in between_brackets:
                    use_in_between_brackets = True
                    break
        if use_in_between_brackets:
            phrase = between_brackets
        else:
            phrase = valid_substring[0:bracket_start_index]

    # compare the original data from dataframe with the processed data
    if phrase != row['symbol'] and DEBUG:
        print('CHANGE: '+phrase+' --- '+row['symbol'])
    
    phrases.append(phrase)
    
check_ignored_symbols_in_valid_context.sort()
ignore_substrings_including_symbols.sort()
if check_ignored_symbols_in_valid_context==ignore_substrings_including_symbols:
    print('All symbols marked as possibly ignored were found in valid context.')
else:
    print('WARNING: Not all ignored symbols were found in valid context,'\
          ' the output dictionary is likely not reversible.')
    set_0 = set(check_ignored_symbols_in_valid_context)
    set_1 = set(ignore_substrings_including_symbols)
    non_phrasal_symbols = set_0 ^ set_1
    print(non_phrasal_symbols)
    
### at this point, there is a list of phrases, 
#   containing all the symbols in the whole vocabulary, 
#   except non_phrasal_symbols

# loop through phrases    
for phrase in phrases:
    # loop through symbols
    for symbol in phrase:
        if symbol in list_of_HSK_symbols:
            # initialize dictionary entry
            if symbol not in dictionary.keys():
                dictionary[symbol] = list()
            # prevent appending the same phrase twice
            if phrase not in dictionary[symbol]:
                dictionary[symbol].append(phrase)
        else:
            raise ValueError('ERROR: a symbol outside of the standard'\
                             +' vocabulary has slipped in.'\
                             +' The symbol in question is '+ symbol+'.')
    
# #%% Store the processed data
save2file(dictionary, output_name, path_output_file)
