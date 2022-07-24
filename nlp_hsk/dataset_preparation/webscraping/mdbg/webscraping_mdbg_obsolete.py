# -*- coding: utf-8 -*-
"""
This script loads a list of chinese characters, sends a URL request to 
https://mdbg.net, reads the response and parses the response to get pinyin.

HOW TO parse data from HTML was motivated by the following StackOverFlow 
question:
https://stackoverflow.com/questions/30002313/selenium-finding-elements-by-class-name-in-python
"""

#%% Imports
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd
from pathlib import Path
import numpy as np
import pickle
import json

#%% Inputs
# in case something goes wrong, the script can continue from any index
start_from_symbol_index = 1
# get the patter of URL
url_pattern = ["https://www.mdbg.net/chinese/chindict_ac_wdqb.php?st=0&l=15&i="]
# file containing a list of unique symbols symbols with HSK level
file_dict_symbols2levels = 'dict_symbol2levels.pickle'
# path to processed data (contains file_HSK_symbols)
path_to_processed_data = '../../New_HSK/processed_data'
# output file containing a dictionary of symbol:list(radicals) pairs
file_symbols_radicals = 'dict_pinyin_start_index_'+str(start_from_symbol_index)
# path to output data
path_to_output_data = '../../New_HSK/web_scrapped/'

#%% Load list of symbols
# these symbols will be scrapped from internet one by one for radicals
dict_symbols2levels = pd.read_pickle(Path(path_to_processed_data, file_dict_symbols2levels))
# get the list of symbols
list_chinese_chars = list(dict_symbols2levels.keys())

# debug - un-comment to run the script for 3 symbols only
list_chinese_chars = list_chinese_chars[0:3]

#%% Web-scapping
# print to console
print('Web scrapper for "'+ url_pattern[0] + '" will attempt to obtain ' \
      'pinyin for '+ str(len(list_chinese_chars)-start_from_symbol_index) \
      +' chinese symbols loaded from ' \
      +str(Path(path_to_processed_data, file_dict_symbols2levels))+' file.')
if(start_from_symbol_index > 0):
    print('The web scrapper starts at ' \
          +str(start_from_symbol_index) +'th symbol.')



# allocate dictionary storing the scrapped radicals
dict_symbol2pinyin = dict()
# initialization
from selenium.webdriver.firefox.options import Options as FirefoxOptions
options = FirefoxOptions()
options.set_preference('devtools.jsonview.enabled', False)
# options = Options()
options.add_argument('--headless')
driver = webdriver.Firefox(options=options)
# fetch radicals for every chinese character
for idx_symbol, symbol in enumerate(list_chinese_chars):
    
    # skip symbols which are presumably already loaded
    if(start_from_symbol_index > idx_symbol):
        continue
    
    # for URL
    # url = "https://www.mdbg.net/chinese/chindict_ac_wdqb.php?st=0&l=15&i="+symbol
    url = url_pattern[0]+symbol
    
    # repeat the process until the website answers as expected
    request_ongoing = True
    while(request_ongoing):
        try:
            # send URL request
            driver.get(url)
            # wait from 2 seconds
            time.sleep(2)
            
            content = driver.page_source
            content = driver.find_element(By.TAG_NAME, "pre").text
            
            # list caontaining entries retrieved from the dictionary, which finds 
            # the given symbol and words containing the symbol
            list_of_dicts = json.loads(content)
            # data has been successfullt scrapped
            request_ongoing = False
        except Exception as e:
            # print error value
            print(e)
            print('Waiting for 20 seconds, then I will try again ...')
            # wait a while and try again
            time.sleep(20)
            
    # store the data
    dict_symbol2pinyin[symbol] = list_of_dicts
    # save on every iteration in case of crash
    with open(Path(path_to_output_data, file_symbols_radicals+'.pickle'), 'wb') as handle:
        pickle.dump(dict_symbol2pinyin, handle, protocol=pickle.HIGHEST_PROTOCOL)

    print('('+str(idx_symbol+1)+'/'+str(len(list_chinese_chars))+') scrapped '+symbol+': '+', '.join(list_radicals))

driver.quit()
    
