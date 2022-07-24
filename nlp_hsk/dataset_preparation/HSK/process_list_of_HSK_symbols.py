# -*- coding: utf-8 -*-
"""
This script loads df_HSK_symbols and creates a dictionary of symbols, with 
ALL HSK levels, where they appear.
"""

#%% Imports
import pandas as pd
from pathlib import Path
import pickle
from collections import defaultdict

#%% Inputs
# file containing the list of radicals
file_df_HSK_vocab = 'df_HSK_vocab.pickle'
# path to save the output data
path_to_processed_data = 'processed_data'


#%% Load data
df_HSK_vocab = pd.read_pickle(Path(path_to_processed_data, file_df_HSK_vocab))

#%% Process data
# get all symbols and the related HSK level
list_of_HSK_symbols = list()

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
            if(char not in list_of_HSK_symbols):
                # add character and the level
                list_of_HSK_symbols.append(char)
            else:
                pass
        # also collect non-chinese characters
        else:
            pass

# Console print
print(str(len(list_of_HSK_symbols))+' unique chinese symbols found:')
print(list_of_HSK_symbols)

#%% Store data
with open(Path(path_to_processed_data, 'list_of_HSK_symbols.pickle'), 'wb') as handle:
    pickle.dump(list_of_HSK_symbols, handle, protocol=pickle.HIGHEST_PROTOCOL)
