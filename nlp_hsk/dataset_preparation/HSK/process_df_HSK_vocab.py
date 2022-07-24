# -*- coding: utf-8 -*-

"""
This script loads the .txt files from /New_HSK and outputs a DataFrame with
a vocabulary including symbols, pinyin, meaning and HSK level.
"""
#%% Imports
import pandas as pd
from pathlib import Path

#%% Inputs

# dictionary of files including New HSK vocabulary with according level
vocab_files =  {1:'New_HSK_1.txt',
                2:'New_HSK_2.txt',
                3:'New_HSK_3.txt',
                4:'New_HSK_4.txt',
                5:'New_HSK_5.txt',
                6:'New_HSK_6.txt'
                }
# path to vocab files
path_to_vocab_files = 'raw_files'
# path to save the output into
output_file = 'df_HSK_vocab.pickle'
path_to_output = 'processed_data'


#%% Constants
# column names in the DataFrame
COLUMN_NAMES = ['#', 'symbol', 'pinyin', 'meaning']

#%% Load Data
# load data into dictionary according to HSK level
dict_HSK_vocab = dict()
for (HSK_level, HSK_file) in vocab_files.items():
    dict_HSK_vocab[HSK_level] = pd.read_csv(Path(path_to_vocab_files, HSK_file), \
                                       delimiter='\t', names=COLUMN_NAMES, \
                                        index_col='#')
        
#%% Process Data

# allocate temporary working DataFrame
df_HSK_vocab = pd.DataFrame()
# join all HSK levels into single DataFrame and add "HSK_level" column
for (HSK_level, tmp_df_HSK_vocab) in dict_HSK_vocab.items():
    tmp_df_HSK_vocab['HSK_level'] = HSK_level
    df_HSK_vocab = df_HSK_vocab.append(tmp_df_HSK_vocab)
df_HSK_vocab = df_HSK_vocab.reset_index()

#%% Store Data
# visually check what was processed
print('--- '+ str(len(df_HSK_vocab)) +' vocabulary entries:')
print(df_HSK_vocab)

# save the data
df_HSK_vocab.to_pickle( Path(path_to_output, output_file) )


