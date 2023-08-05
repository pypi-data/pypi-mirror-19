from codesnip.models import Snippet
from codesnip.templatetags import codesnip
from django.template import Template, Context
from django.test import TestCase


class TestCodeNodeClass(TestCase):
    def setUp(self):
        snippet_args = {
            'slug': 'test',
            'pygmentized': '<div class="highlight">'
                           '<pre><span class="k">print</span> <span class="s">'
                           '&quot;Hello World&quot;</span></pre>'
                           '</div>'
        }
        self.snippet = Snippet.objects.create(**snippet_args)

    def test_render(self):
        template = Template('{% load codesnip %}'
                            '{% code %}!!snippet test!!{% endcode %}')
        rendered = template.render(Context({}))
        assert rendered == self.snippet.pygmentized

    def test_render_nonexistant_snippet(self):
        template = Template('{% load codesnip %}'
                            '{% code %}!!snippet doesNotExist!!{% endcode %}')
        rendered = template.render(Context({}))
        assert rendered == codesnip.ObjectDoesNotExistMessage
