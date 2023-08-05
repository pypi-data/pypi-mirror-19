"""
Settings for codesnip are namespaced in the CODESNIP setting.
For exmaple your project's `settings.py` file might looks like this:

CODESNIP = {
    'FORMATTER_ARGS': {
        'linenos': True,
        'anchorlinenos': True,
        'lineanchors': 'line',
    },
}
"""

from django.conf import settings as project_settings

DEFAULTS = {
    'FORMATTER_ARGS': {
        'cssclass': 'codesnip',
    },
}

# Check if a setting is applied in the Django project settings.py,
#   if not use the default.
SETTINGS = {}
for setting_name, setting_default in DEFAULTS.items():
    try:
        SETTINGS[setting_name] = project_settings.CODESNIP[setting_name]
    except (AttributeError, KeyError):
        SETTINGS[setting_name] = DEFAULTS[setting_name]
