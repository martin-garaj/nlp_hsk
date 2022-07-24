# -*- coding: utf-8 -*-
"""
This script loads a list of chinese characters, sends a URL request to 
https://hanzii.net, reads the response and parses the response. The goal is to
get radicals, meaning and strokes of every symbol AND radical (radicals that 
are obtained from symbols are appended to the initial list and webscrapped
again, until the radical cannot be disassambled to radicals anymore).

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
import pickle
from collections import defaultdict 

#%% Inputs
# in case something goes wrong, the script can continue from any index
start_from_symbol_index = 0
# get the patter of URL
url_pattern = ["https://hanzii.net/search/kanji/","?hl=en-US"]
# file containing a list of unique symbols symbols
file_list_chinese_chars = 'list_of_HSK_symbols.pickle'
# path to processed data (contains file_HSK_symbols)
path_to_processed_data = '../../HSK/processed_data'
# output file containing a dictionary of symbol:list(radicals) pairs
file_symbols_radicals = 'dict_symbols_and_radical2hanzi_kanji'
# path to output data
path_to_output_data = 'raw_files/'

#%% Load list of symbols
# these symbols will be scrapped from internet one by one for radicals, 
# meaning, pinyin and strokes
list_chinese_chars = \
    pd.read_pickle(Path(path_to_processed_data, file_list_chinese_chars))

# debug - uncomment to webscrape several characters only
list_chinese_chars = list_chinese_chars[153:154]

#%% Web-scapping
# print to console
print('Web scrapper for "'+ url_pattern[0] + '" will attempt to obtain ' \
      'radicals for '+ str(len(list_chinese_chars)-start_from_symbol_index) \
      +' chinese symbols loaded from ' \
      +str(Path(path_to_processed_data, file_list_chinese_chars))+' file.')
if(start_from_symbol_index > 0):
    print('The web scrapper starts at ' \
          +str(start_from_symbol_index) +'th symbol.')

# allocate dictionary storing the scrapped radicals
dict_hanzi_net_kanji = defaultdict(dict)
# initialization
options = Options()
options.add_argument('--headless')
driver = webdriver.Firefox(options=options)
# fetch radicals for every chinese character
for idx_symbol, symbol in enumerate(list_chinese_chars):
    
    # skip symbols which are presumably already loaded
    if(start_from_symbol_index > idx_symbol):
        continue
        
    # for URL
    # url = "https://hanzii.net/search/kanji/"+symbol+"?hl=en-US"
    url = url_pattern[0]+symbol+url_pattern[1]
    
    # repeat the process until the website answers
    request_ongoing = True
    first_exeption = True
    while(request_ongoing):
        try:
            # list of retrieved radicals
            list_sets = []
            list_count = []
            list_strokes = []
            list_compositions = []
            list_super_compositions = []
            list_variants = []
            list_universal_dictionary = []
            
            # send URL request
            driver.get(url)
            # wait from 2 seconds
            time.sleep(2)
            
            # if there are more variants, click the one that has the same symbol
            result_hanzi = driver.find_elements(by=By.CLASS_NAME, value="result-hanzi")[0]
            item_detail_hanzi = result_hanzi.find_elements(by=By.CLASS_NAME, value="item-detail-hanzi")
            # check if there is a button
            if len(item_detail_hanzi) > 0:
                # find the right button
                for button in item_detail_hanzi:
                    if(button.text == symbol):
                        button.click()
                        break
            
            # check if the site successfully translated the symbol
            none_data = driver.find_elements(by=By.CLASS_NAME, value="none-data")
            if len(none_data) > 0:
                # the symbol has no meening on its own, there is nothing else to do
                pass
            else:
                ### get box-content
                box_content = result_hanzi.find_elements(by=By.CLASS_NAME, value="box-content")[0]
                # only "txt-main-word" elements contain the category
                elements = box_content.find_elements(by=By.CLASS_NAME, value="txt-main-word")
                # search for element that includes text "Compositions"
                for e in elements:
                    if('Compositions' in e.text):
                        # find parent element (since "Compositions" doesnt have sub-elements)
                        parent = e.find_element(by=By.XPATH, value="./..")
                        # within parent (includes CLASS="txt-main-word", 
                        # search for CLASS="item-detail", which includes radicals)
                        compositions = parent.find_elements(by=By.CLASS_NAME, value="item-detail")
                        # append the content of Compositions tp composition list
                        for c in compositions:
                            list_compositions.append(c.text)
                    if('Super compositions' in e.text):
                        parent = e.find_element(by=By.XPATH, value="./..")
                        super_compositions = parent.find_elements(by=By.CLASS_NAME, value="item-detail")
                        for sp in super_compositions:
                            list_super_compositions.append(sp.text)
                    if('Variants' in e.text):
                        parent = e.find_element(by=By.XPATH, value="./..")
                        variants = parent.find_elements(by=By.CLASS_NAME, value="item-detail")
                        for v in variants:
                            list_variants.append(v.text)
                # only "content-detail" elements contain the universal dictionary
                elements = box_content.find_elements(by=By.CLASS_NAME, value="content-detail")
                for e in elements:
                    universal_dictionary = e.text
                    universal_dictionary = universal_dictionary.replace('Universal dictionary:\n', '').split('\n')
                    for ud in universal_dictionary:
                        list_universal_dictionary.append(ud)
            
                ### get box-detail
                box_detail = driver.find_elements(by=By.CLASS_NAME, value="box-detail")[0]
                elements = box_detail.find_elements(by=By.CLASS_NAME, value="txt-detail")
                # search for element that includes text "Compositions"
                for e in elements:
                    if('Sets' in e.text):
                        # the element is a string containing 'Sets: ' and a list of symbols
                        sets = e.text
                        sets = sets.replace('Sets','').replace(' ','').replace(':','')
                        for s in sets:
                            list_sets.append(s)
                    if('Count' in e.text):
                        count = e.text
                        count = count.replace('Count','').replace(' ','').replace(':','')
                        list_count.append(int(count))
                    if('Strokes' in e.text):
                        strokes = e.text
                        strokes = strokes.replace('Strokes','').replace(' ','').replace(':','')
                        for s in strokes:
                            list_strokes.append(s)
        
            # data has been successfullt scrapped
            request_ongoing = False
        except Exception as e:
            if(first_exeption):
                # print error value
                print(e)
                first_exeption = False
            print('Waiting for 20 seconds, then I will try again ...')
            # wait a while and try again
            time.sleep(20)

    # store the data
    dict_hanzi_net_kanji[symbol]['sets'] = list_sets
    dict_hanzi_net_kanji[symbol]['count'] = list_count
    dict_hanzi_net_kanji[symbol]['strokes'] = list_strokes
    dict_hanzi_net_kanji[symbol]['compositions'] = list_compositions
    dict_hanzi_net_kanji[symbol]['super_compositions'] = list_super_compositions
    dict_hanzi_net_kanji[symbol]['variants'] = list_variants
    dict_hanzi_net_kanji[symbol]['universal_dictionary'] = list_universal_dictionary

    # save on every iteration in case of crash
    with open(Path(path_to_output_data, file_symbols_radicals+'.pickle'), 'wb') as handle:
        pickle.dump(dict_hanzi_net_kanji, handle, protocol=pickle.HIGHEST_PROTOCOL)

    print('('+str(idx_symbol+1)+'/'+str(len(list_chinese_chars))+') scrapped '+symbol+': '+', '.join(list_compositions))
    # data has been successfullt scrapped
    request_ongoing = False
    
    # extend the list_chinese_chars by additional characters discovered 
    # in current web scrapping of "Components"
    for c in list_compositions:
        if c not in list_chinese_chars:
            list_chinese_chars.append(c)

driver.quit()
