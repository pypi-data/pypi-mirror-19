# -*- coding: utf-8 -*-
import io
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
            for item in source:
                yield item


class JsonFieldSource(object):

    def __init__(self, json_source, key):
        self.json = json_source
        self.key = key

    def __iter__(self):
        for json_entry in self.json:
            yield json_entry[self.key]


class FilteringSource(object):

    def __init__(self, source, condition):
        self.source = source
        self.condition = condition

    def __iter__(self):
        for entry in self.source:
            if self.condition(entry):
                yield entry


class MappingSource(object):

    def __init__(self, source, function):
        self.source = source
        self.function = function

    def __iter__(self):
        for entry in self.source:
            yield self.function(entry)


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


class FileLineSource(object):

    def __init__(self, text_file_path, encoding='utf8'):
        self.source_file = text_file_path
        self.encoding = encoding

    def __iter__(self):
        with io.open(self.source_file, mode='rt', encoding=self.encoding) as in_file:
            for line in in_file:
                line = line.strip()
                if len(line) <= 0:
                    continue
                yield line


class OpensubtitlesSentenceSource(object):

    DEFAULT_SENTENCE_TAG = '<s>'

    def __init__(self, line_source, sentence_tag=None):
        self.source = line_source
        if sentence_tag:
            self.sentence_tag = sentence_tag
        else:
            self.sentence_tag = OpensubtitlesSentenceSource.DEFAULT_SENTENCE_TAG

    def __iter__(self):
        for line in self.source:
            for sentence in line.split(self.sentence_tag):
                yield sentence.strip()


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
