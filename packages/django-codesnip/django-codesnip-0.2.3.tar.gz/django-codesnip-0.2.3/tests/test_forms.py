from django.test import TestCase
from codesnip.forms import SnippetForm
from codesnip.models import Snippet
from . import utils


class TestSnippetForm(TestCase):
    def test_language_sort(self):
        form = SnippetForm()
        assert form.fields['language'].choices == sorted(form.fields
                                                         ['language'].choices,
                                                         key=lambda x: x[1])

    def test_valid_data_and_save(self):
        # This data should be valid\
        form = SnippetForm(data=utils.VALID_SNIPPET_ARGS)
        assert form.is_valid()

        snippet = form.save()
        for data in utils.VALID_SNIPPET_ARGS:
            assert getattr(snippet, data) == utils.VALID_SNIPPET_ARGS[data]
