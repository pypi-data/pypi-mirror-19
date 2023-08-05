from __future__ import absolute_import, print_function
from .__init__ import Parser
import os


class EnvParser(Parser):

    def __init__(self, source):
        pass

    def data(self):
        return os.environ

