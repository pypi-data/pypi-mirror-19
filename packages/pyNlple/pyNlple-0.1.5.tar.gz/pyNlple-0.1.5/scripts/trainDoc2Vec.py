# -*- coding: utf-8 -*-
import logging

import itertools
from gensim.models.doc2vec import TaggedDocument

from pynlple.datasource.corpus import StackingSource, FilteringSource, JsonFieldSource, MappingSource
from pynlple.datasource.filesource import FilePathSource
from pynlple.datasource.jsonsource import FileJsonDataSource
from pynlple.processing.preprocessor import DefaultPreprocessorStack
from pynlple.module import abs_path, append_paths
from gensim import models

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


path1 = 'F:/text_lang/facebook-text-1.txt'
path2 = 'F:/text_lang/facebook-text-2.txt'
json_source1 = FileJsonDataSource(path1)
json_source2 = FileJsonDataSource(path2)

json_source = StackingSource([json_source1, json_source2])

language_filtered_source = FilteringSource(json_source, lambda j: j['lang'] in ['rus', 'unc'])
text_source = JsonFieldSource(language_filtered_source, 'Text')

replacers_stack = DefaultPreprocessorStack()
token_source = MappingSource(text_source, lambda t: replacers_stack.preprocess(t).split())

n = 3
long_sentences_source = FilteringSource(token_source, lambda s: len(s) >= n)

# counter = itertools.count()
# source = MappingSource(long_sentences_source, lambda s: TaggedDocument(s, (next(counter),)))
source = MappingSource(long_sentences_source, lambda s: TaggedDocument(s, (str(hash(tuple(s))),)))
key = 'facebook' + '_min_tokens=' + str(n)
pars = dict(
    size=400,
    window=8,
    dm=1,
    dbow_words=1,
    dm_mean=1,
    negative=5,
    seed=13,
    min_count=2,
    iter=10,
    workers=3
)
params = '_'.join(repr(key) + '=' + repr(pars[key]) for key in sorted(pars.keys()))
model_name = 'gensim_doc2vec_' + key + '_' + params + '.tst'
model_path = append_paths(abs_path('model/'), model_name)

model = models.Doc2Vec(None, **pars)
model.build_vocab(source)
model.train(source)
model.save(model_path)
print('First training step finished.')

# model.save_word2vec_format(path('data\\' + str(id_) + '_word2vec.tsv'))

# model = models.Doc2Vec.load(model_path)
# print ('Model ' + model_name + ' was successfully loaded.')