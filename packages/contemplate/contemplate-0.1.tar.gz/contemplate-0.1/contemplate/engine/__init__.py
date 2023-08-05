from __future__ import absolute_import, print_function
from abc import ABCMeta, abstractmethod

class TemplateEngine(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def render(self, data):
        pass
