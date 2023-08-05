# -*- coding: utf-8 -*-
import codecs
import gzip
import re

import bz2
from gensim.corpora.textcorpus import TextCorpus
from gensim.models.doc2vec import TaggedDocument

from pynlple.datasource.jsonsource import FileJsonDataSource


class StackingSource(object):
    def __init__(self, list_sources):
        self.sources = list_sources

    def __iter__(self):
        for source in self.sources:
            return source.__iter__()


class GensimTextCorpus(TextCorpus):

    DEFAULT_TOKEN_DELIM_PATTERN = r'\s+'

    def get_texts(self):
        split_pattern = re.compile(self.DEFAULT_TOKEN_DELIM_PATTERN)

        with self.getstream() as lines:
            for lineno, line in enumerate(lines):
                line = line.strip()
                if self.metadata:
                    yield split_pattern.split(line), (lineno,)
                else:
                    yield split_pattern.split(line)


class GensimTextPreprocessingCorpus(TextCorpus):

    def __init__(self, input=None, token_delim_pattern=None, preprocessor=None):
        if not token_delim_pattern:
            self.delim = GensimTextPreprocessingCorpus.DEFAULT_TOKEN_DELIM_PATTERN
        else:
            self.delim = token_delim_pattern
        if preprocessor:
            self.preprocessor = preprocessor
        super(GensimTextPreprocessingCorpus, self).__init__(input)

    DEFAULT_TOKEN_DELIM_PATTERN = r'\s+'

    def get_texts(self):
        split_pattern = re.compile(self.DEFAULT_TOKEN_DELIM_PATTERN)

        with self.getstream() as lines:
            for lineno, line in enumerate(lines):
                if self.preprocessor:
                    line = self.preprocessor.preprocess(line)
                if self.metadata:
                    yield split_pattern.split(line), (lineno,)
                else:
                    yield split_pattern.split(line)


class JsonTextSource(object):

    def __init__(self, json_filepaths_source, text_key):
        self.json_paths = json_filepaths_source
        self.text_key = text_key

    def __iter__(self):
        for json_path in self.json_paths:
            for entry in FileJsonDataSource(json_path):
                yield entry[self.text_key]


class DFsTaggedDocumentSource(object):

    def __init__(self, dataframe_sources, text_column, tag_columns=None, text_preprocessor=None):
        self.sources = dataframe_sources
        self.text_column = text_column
        self.tag_columns = tag_columns
        self.text_preprocessor = text_preprocessor
        super().__init__()

    def __iter__(self):
        for source in self.sources:
            return DFTaggedDocumentSource(source, self.text_column, self.tag_columns, self.text_preprocessor)


class DFTaggedDocumentSource(object):

    def __init__(self, dataframe_source, text_column, tag_columns=None, text_preprocessor=None):
        self.source = dataframe_source
        self.text_column = text_column
        self.tag_columns = tag_columns
        self.text_preprocessor = text_preprocessor

    def __iter__(self):
        for row in self.source.get_dataframe().itertuples():
            text = getattr(row, self.text_column)
            if self.text_preprocessor:
                text = self.text_preprocessor.preprocess(text)
            tokens = text.split()
            if self.tag_columns:
                yield TaggedDocument(tokens, [getattr(row, tag_column) for tag_column in self.tag_columns])
            else:
                yield tokens


class PreprocessingLineSource(object):

    def __init__(self, line_source, preprocessor):
        self.source = line_source
        self.preprocessor = preprocessor

    def __iter__(self):
        for item in self.source:
            yield self.preprocessor.preprocess(item)


class FileLineSource(object):

    def __init__(self, text_file_path, encoding='utf8'):
        self.source_file = text_file_path
        self.encoding = encoding

    def __iter__(self):
        with codecs.open(self.source_file, 'rt', self.encoding) as in_file:
            for line in in_file:
                line = line.strip()
                if len(line) <= 0:
                    continue
                yield line


class OpensubtitlesSentenceSource(object):

    DEFAULT_SENTENCE_TAG = '<s>'

    def __init__(self, line_source, text_preprocessor=None, sentence_tag=None):
        self.source = line_source
        self.text_preprocessor = text_preprocessor
        if sentence_tag:
            self.sentence_tag = sentence_tag
        else:
            self.sentence_tag = OpensubtitlesSentenceSource.DEFAULT_SENTENCE_TAG

    def __iter__(self):
        for line in self.source:
            text = line
            if self.text_preprocessor:
                text = self.text_preprocessor.preprocess(text)
            for sentence in text.split(self.sentence_tag):
                yield sentence.strip().split()


class SentenceFilteringSource(object):

    def __init__(self, sentence_source, filter_rule):
        self.source = sentence_source
        self.rule = filter_rule

    def __iter__(self):
        for sentence in self.source:
            if self.rule(sentence):
                yield sentence


class BZipDocumentSource(object):

    def __init__(self, bzip_filepath, text_preprocessor=None):
        self.source_filepath = bzip_filepath
        self.text_preprocessor = text_preprocessor
        super().__init__()

    def __iter__(self):
        with bz2.BZ2File(self.source_filepath, 'rtU') as in_bz:
            for line in in_bz:
                text = line
                if self.text_preprocessor:
                    text = self.text_preprocessor.preprocess(text)
                tokens = text.split()
                yield tokens


class GZipDocumentSource(object):

    def __init__(self, gzip_filepath, text_preprocessor=None):
        self.source_filepath = gzip_filepath
        self.text_preprocessor = text_preprocessor
        super().__init__()

    def __iter__(self):
        with gzip.GzipFile(self.source_filepath, 'rU') as in_bz:
            for line in in_bz:
                text = line
                if self.text_preprocessor:
                    text = self.text_preprocessor.preprocess(text)
                tokens = text.split()
                yield tokens
