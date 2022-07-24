# NLP_HSK

**NLP_HSK** is a small repo primarily based on providing well-curated dataset 
for **New HSK** (new standard for HSK introduced in March 2022). 
HSK (a.k.a **H**anyu **S**huiping **K**aoshi) is a standardized way of 
learning Mandarin chinese and testing the proficiency level. 
NLP for HSK is a Natural Language Processing for chinese Mandarin based on 
HSK learning process.

## Main motivation
HSK has several levels, where the first 6 levels has a set vocabulary. 
Further levels are close to/at native-speaker level, thus there is no 
pre-defined pool of vocabulary to be learned as it depends on the learned 
him/her-self. Since "*Chinese characters do not constitute an alphabet or a 
compact syllabary. Rather, the writing system is roughly logosyllabic; 
that is, a character generally represents one syllable of spoken Chinese and 
may be a word on its own or a part of a polysyllabic word.*"
[wiki](https://en.wikipedia.org/wiki/Written_Chinese). The **main goal** of 
NLP_HSK is to provide a perspective over the chinese writing system, to
simplify the learning process.

The primarily way of providing perspective, is to curate a dataset, which:
    - is complete (no missing data, no duplicated data)
    - is easy to access (data are stored in python dictionary)
    - is consistent (back-to-back consistency among data structures)
    - is simple to correct when errors are found (data are in human-readable form)

## Dataset
This dataset is available in /nlp_hsk/dataset/  
&emsp; - [**symbol2level.py**](https://github.com/martin-garaj/nlp_hsk/blob/8541300685b24041b92ce28090f77d1b79c3da75/nlp_hsk/dataset/symbol2level.py)  
&emsp;&emsp; - *symbol2level* dictionary translating chinese symbol to the HSK level,
          where the learner can learn the symbol  
&emsp;&emsp; - example:  
&emsp;&emsp;&emsp; '你': [ 1],  
&emsp; - [**symbol2pinyin.py**](https://github.com/martin-garaj/nlp_hsk/blob/8541300685b24041b92ce28090f77d1b79c3da75/nlp_hsk/dataset/symbol2pinyin.py)  
&emsp;&emsp; - *symbol2pinyin* dictionary translating chinese symbol to its 
          pronounciation accompanied with one of the tones (1:ā, 2:á, 3:ǎ, 4:à)  
&emsp;&emsp; - example:  
&emsp;&emsp;&emsp; '你': [('ni', 3)],  
&emsp; - [**symbol2radical.py**](https://github.com/martin-garaj/nlp_hsk/blob/8541300685b24041b92ce28090f77d1b79c3da75/nlp_hsk/dataset/symbol2radical.py)  
&emsp;&emsp; - *symbol2pinyin* a nested dictionary which translates a chinese 
        symbol to its constituent parts  
&emsp;&emsp; - example:  
&emsp;&emsp;&emsp; '你': {'亻': None,  
&emsp;&emsp;&emsp;&emsp; '尔': {'小': None,  
&emsp;&emsp;&emsp;&emsp;&emsp; '𠂊': None}},  
&emsp; - [**symbol2stroke.py**](https://github.com/martin-garaj/nlp_hsk/blob/8541300685b24041b92ce28090f77d1b79c3da75/nlp_hsk/dataset/symbol2stroke.py)  
&emsp;&emsp; - *symbol2stroke* dictionary translating chinese symbol to its 
          constituent strokes  
&emsp;&emsp; - example:  
&emsp;&emsp;&emsp; '你': [ 'ノ', '丨', 'ノ', 'フ', '丨', 'ノ', '丶'],  
&emsp; - [**symbol2word.py**](https://github.com/martin-garaj/nlp_hsk/blob/8541300685b24041b92ce28090f77d1b79c3da75/nlp_hsk/dataset/symbol2word.py)  
&emsp;&emsp; - *symbol2word* dictionary connecting chinese symbol with words it is 
          part of  
&emsp;&emsp; - example:  
&emsp;&emsp;&emsp; '你': ['你',  
&emsp;&emsp;&emsp;&emsp; '你们'],  
&emsp; - [**word2meaning.py**](https://github.com/martin-garaj/nlp_hsk/blob/8541300685b24041b92ce28090f77d1b79c3da75/nlp_hsk/dataset/symbol2word.py)  
&emsp;&emsp; - *word2meaning* dictionary connecting words with their meaning  
&emsp;&emsp; - example:  
&emsp;&emsp;&emsp; '你': [  'you'],  
&emsp; - [**level2color.py**](https://github.com/martin-garaj/nlp_hsk/blob/8541300685b24041b92ce28090f77d1b79c3da75/nlp_hsk/dataset/level2color.py)  
&emsp;&emsp; - *level2color* dictionary provides a convenient way to obtain the 
          color of specific HSK level (1 to 6) to visually match the data to 
          the progress of the learning process   
            

## Natural Language Processing
Mandarin (symbols, pinyin and meaning) create a 3-layer system of networks, 
where the symbols are interconnect with other symbols through radicals, 
meaning and similarity in pronounciation. Current goal is to train a simple 
**Graph-Neural Network** (similar to auto-encoder) in order to perform 
dimension reduction and visualize the HSK dataset. This is useful for 
learners to visualize their progress and the extent of the vocabulary 
they are familiar with in the context of the whole vocabulary.

