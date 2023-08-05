from django.db import models
from pygments.lexers import LEXERS
from codesnip.settings import SETTINGS
from pygments import highlight
from pygments import lexers
from pygments.formatters import HtmlFormatter


class Snippet(models.Model):
    LANGUAGE_CHOICES = [(lexer, LEXERS[lexer][1]) for lexer in LEXERS]

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    language = models.CharField(max_length=255, choices=LANGUAGE_CHOICES)
    code = models.TextField()
    pygmentized = models.TextField(blank=True)

    def __str__(self):
        return '%s' % self.slug

    def pygmentize(self):
        language_lexer = getattr(lexers, self.language)
        formatter = HtmlFormatter(**SETTINGS['FORMATTER_ARGS'])
        self.pygmentized = highlight(self.code, language_lexer(), formatter)
