from codesnip.models import Snippet
from django import template
from django.core.exceptions import ObjectDoesNotExist
import re

register = template.Library()

ObjectDoesNotExistMessage = "<div class='alert alert-warning' "\
    "role='alert'>Code snippet missing!</div>"


# Parse text for snippet shortcode: !!snippet slug!!
def do_code(parser, token):
    nodelist = parser.parse(('endcode',))
    parser.delete_first_token()
    return CodeNode(nodelist)


class CodeNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist
        self.ObjectDoesNotExistMessage = "<div class='alert alert-warning' "\
            "role='alert'>Code snippet missing!</div>"

    def render(self, context):
        output = self.nodelist.render(context)
        output_list = output.split("!!")

        regex_str = 'snippet (.*)'
        for i in range(len(output_list)):
            match = re.search(regex_str, output_list[i])
            if match:
                try:
                    snippet = Snippet.objects.get(slug=match.group(1))
                    output_list[i] = snippet.pygmentized
                except ObjectDoesNotExist:
                    output_list[i] = ObjectDoesNotExistMessage

        output = ''.join(output_list)
        return output

register.tag('code', do_code)
