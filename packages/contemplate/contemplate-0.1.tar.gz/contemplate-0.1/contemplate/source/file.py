from __future__ import absolute_import, print_function
from .__init__ import Source

class FileSource(Source):

    def __init__(self, source):
        self.source = source

    def data(self):
        with open(self._source, 'r') as fd:
            # FIXME: temp-test-only, will fail if file too big
            return fd.read()
