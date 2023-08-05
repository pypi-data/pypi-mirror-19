from __future__ import absolute_import, print_function
from abc import ABCMeta, abstractproperty, abstractmethod


class ParserException(Exception):
    pass


class Parser(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, source):
        pass

    @abstractmethod
    def data(self):
        pass
