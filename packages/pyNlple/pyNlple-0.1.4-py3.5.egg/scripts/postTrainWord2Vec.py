# -*- coding: utf-8 -*-
import logging

from pynlple.datasource.corpus import DFTaggedDocumentSource
from pynlple.datasource.datasource import JsonDataframeSource as datasource, DataframeSource
from pynlple.datasource.jsonsource import FileJsonDataSource as jsonsource
from pynlple.processing.preprocessor import DefaultPreprocessorStack
from pynlple.processing.stopwords import PunctuationFilter

from pynlple.module import abs_path, append_paths

from gensim.models import Word2Vec

filter_ = PunctuationFilter()


def tokenize(text):
    return text.split()


def filter_stopwords(tokens):
    return filter_.filter(tokens)

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

replacers_stack = DefaultPreprocessorStack()

folder_path = 'E:/Projects/YouScan/pyNlple/data/'
data_path = abs_path(folder_path, '83389_2016.12.01_dump_lang.json') # LOOK FOR IT ON HDD
json_source = jsonsource(data_path)
data = datasource(json_source,
                  'id text tags sourceId postType resourceType lang published'.split(),
                  fill_na_map={'text': '', 'postType': -1}).get_dataframe()
data = data[data['postType'] == 1] # Use only original posts (not comments, replies, etc.)
data = data[data['lang'].isin(['rus', 'unc'])]

data.sort_values(['published'], ascending=False, inplace=True)

preprocessor = DefaultPreprocessorStack()
data['text'] = data['text'].apply(preprocessor.preprocess)
print('Posts, russian: ' + str(data.shape))
data.drop_duplicates(subset=['text'], keep='last', inplace=True)

print('Posts, russian, deduplicated: ' + str(data.shape))

data['tokens'] = data['text'].apply(lambda s: tokenize(s))
data['filtered_tokens'] = data['tokens'].apply(lambda t: filter_stopwords(t))
data['len'] = data['filtered_tokens'].apply(lambda x: len(x))
data['filtered_text'] = data['filtered_tokens'].apply(lambda tokens: ' '.join(tokens))

data = data[data['len'] > 3]
data = data[data['len'] < 90]

model = Word2Vec.load(abs_path(data_path, 'word2vec/YS5-c.w2v'))
w2v = {w: vec for w, vec in zip(model.index2word, model.syn0)}

new_data = DFTaggedDocumentSource(DataframeSource(data), text_column='filtered_text')
model.build_vocab(new_data, update=True)
model.train(new_data)

model.save(abs_path(data_path, 'word2vec/YS5-c_updated.w2v'))