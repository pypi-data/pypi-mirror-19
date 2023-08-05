from django.contrib import admin
from codesnip.forms import SnippetForm
from codesnip.models import Snippet


class SnippetAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    form = SnippetForm

admin.site.register(Snippet, SnippetAdmin)
