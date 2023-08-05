from __future__ import print_function, absolute_import
from .__init__ import Parser, ParserException
import json


class JSONParser(Parser):

    def __init__(self, source):
        self.source = source

    def data(self):
        try:
            with open(self.source, 'r') as fd:
                return json.load(fd)
        except ValueError as err:
            raise DataSourceException(err)

