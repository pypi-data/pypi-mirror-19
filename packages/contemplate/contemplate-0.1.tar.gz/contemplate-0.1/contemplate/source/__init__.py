from __future__ import absolute_import, print_function
from abc import ABCMeta, abstractmethod

class Source(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def data(self):
        pass
