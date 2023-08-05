from django import forms
from codesnip.models import Snippet


class SnippetForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SnippetForm, self).__init__(*args, **kwargs)
        self.fields['language'].choices = sorted(self.fields['language']
                                                 .choices, key=lambda x: x[1])

    class Meta:
        exclude = ['pygmentized']
        model = Snippet

    def save(self, commit=True):
        snippet = super(SnippetForm, self).save(commit=False)
        snippet.pygmentize()

        if commit:
            snippet.save()
        return snippet
