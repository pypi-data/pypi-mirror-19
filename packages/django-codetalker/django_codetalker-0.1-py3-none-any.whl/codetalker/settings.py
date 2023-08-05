"""
Settings for codetalker are namespaced in the CODETALKER setting.
For exmaple your project's `settings.py` file might looks like this:

CODETALKER = {
    'SHORTCODE_DELIMETER': '@@',
}
"""

from django.conf import settings as project_settings

DEFAULTS = {
    'SHORTCODE_DELIMETER': '@@',
    'SHORTCODE_PATH': 'shortcodes',
}

# Check if a setting is applied in the Django project settings.py,
#   if not use the default.
SETTINGS = {}
for setting_name, setting_default in DEFAULTS.items():
    try:
        SETTINGS[setting_name] = project_settings.CODETALKER[setting_name]
    except (AttributeError, KeyError):
        SETTINGS[setting_name] = DEFAULTS[setting_name]
