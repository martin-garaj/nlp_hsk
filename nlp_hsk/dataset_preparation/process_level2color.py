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
from _support_functions import save2file
import os

#%% Inputs

# path to output file
path_output_file = '../dataset'
# derive the output name from the scipt name
output_name = \
    os.path.basename(__file__).replace('process_','').replace('.py','')
    
# True for debugging, false for full-processing
DEBUG = False

#%% Process data
dictionary = {1: '#fda51d',
              2: '#2f8288',
              3: '#f36f25',
              4: '#b22222',
              5: '#053772',
              6: '#631e61'
              }

# # in case RGB is required
# import matplotlib
# dictionary_rgb = dict()
# for (key, value) in dictionary.items():
#     dictionary_rgb[key] = matplotlib.colors.to_rgb(value)

#%% Store the processed data
save2file(dictionary, output_name, path_output_file)
