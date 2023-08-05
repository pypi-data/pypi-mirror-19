from django.test import TestCase
from codesnip.models import Snippet
from . import utils


class TestSnippetModel(TestCase):
    def test_string_representation(self):
        snippet_args = {
            'slug': 'test_slug'
        }
        snippet = Snippet(**snippet_args)
        snippet.save()
        snippet_obj = Snippet.objects.get(slug=snippet_args['slug'])

        assert '{}'.format(snippet_obj) == snippet_args['slug']

    def test_pygmentize(self):
        snippet = Snippet(**utils.VALID_SNIPPET_ARGS)
        pygmentized = snippet.pygmentize()
        assert snippet.pygmentized == utils.CORRENT_SNIPET_PYGMENTIZED
