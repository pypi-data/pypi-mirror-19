# -*- coding: utf-8 -*-
import io
import json
import requests

from elasticsearch import Elasticsearch
from pynlple.exceptions import DataSourceException


class ElasticJsonDataSource(object):

    def __init__(self, url_address, port, index, query, keys=None, fill_na_map=None, authentication=None):
        self.url = url_address
        self.port = port
        self.index = index
        self.query = query
        self.keys = keys
        self.na_map = fill_na_map
        self.auth = authentication
        self.es = Elasticsearch([{'host': self.url, 'port': self.port}])

    def get_data(self):
        try:
            response = self.es.search(index=self.index, body=self.query)
        except Exception as e:
            raise DataSourceException(e.__str__())

        if self.keys and self.na_map:
            results = [self.__fill_na_values(self.__pick_fields(entry['_source'])) for entry in response['hits']['hits']]
        elif self.keys and not self.na_map:
            results = [self.__pick_fields(entry['_source']) for entry in response['hits']['hits']]
        elif not self.keys and self.na_map:
            results = [self.__fill_na_values(entry['_source']) for entry in response['hits']['hits']]
        else:
            results = [entry['_source'] for entry in response['hits']['hits']]
        print('Server had {0} total elements. Query yielded {1} elements.'
              .format(str(response['hits']['total']), str(len(results))))
        return results

    def __pick_fields(self, entry):
        for key in list(entry.keys()):
            if key not in self.keys:
                entry.pop(key, None)
        return entry

    def __fill_na_values(self, entry):
        for key, value in self.na_map.items():
            if key not in entry:
                entry[key] = value
        return entry


class ServerJsonDataSource(object):
    """Class for providing json data from json files."""

    def __init__(self, url_address, query, authentication=None):
        self.url_address = url_address
        self.query = query
        self.authentication = authentication

    def get_data(self):
        request = requests.post(self.url_address, auth=self.authentication, params=self.query)
        if request.status_code is not 200:
            raise DataSourceException('Could not reach the datasource. HTTP response code: ' + str(request.status_code))
        else:
            return request.json()


class FileJsonDataSource(object):
    """Class for providing json data from json files."""

    FILE_OPEN_METHOD = 'rt'
    FILE_WRITE_METHOD = 'wt'
    DEFAULT_ENCODING = 'utf8'

    def __init__(self, file_path, encoding_str=DEFAULT_ENCODING):
        self.file_path = file_path
        self.encoding_str = encoding_str

    def get_data(self):
        with io.open(self.file_path, FileJsonDataSource.FILE_OPEN_METHOD, encoding=self.encoding_str) as data_file:
            return json.load(data_file)

    def set_data(self, json_data):
        with io.open(self.file_path, FileJsonDataSource.FILE_WRITE_METHOD, encoding=self.encoding_str) as data_file:
            json.dump(json_data, data_file, ensure_ascii=False, indent=2)

    def __iter__(self):
        for entry in self.get_data():
            yield entry
