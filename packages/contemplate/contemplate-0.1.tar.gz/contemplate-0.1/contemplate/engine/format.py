from __future__ import absolute_import, print_function
from .__init__ import TemplateEngine

class FormatEngine(TemplateEngine):

    def render(self, template, **kwargs):
        return template.format(**kwargs)

