# Inspired by Django Markdown Shortcodes
#   https://github.com/defbyte/django-markdown-shortcodes
from django.conf import settings
from django.utils.module_loading import module_has_submodule
from importlib import import_module
from os.path import dirname, basename, isfile
from codetalker.settings import SETTINGS
from sys import modules
import glob
import inspect
import re


class Shortcode_Parser:
    def __init__(self):
        # Shortcodes have the form @@command param param param@@
        # The regex also strips whitespace at the beginning and end of the text
        # wrapped in '@@', e.g. "@@   command param  @@" = "@@command param@@".
        # "@@" is the default shortcode delimeter.
        self._SHORTCODE_REGEX = re \
            .compile('{0}\s*?([([a-z-]+)(.*?)\s*?{0}'.
                     format(SETTINGS['SHORTCODE_DELIMETER']))
        self._shortcodes_dict = {}
        self._find_shortcodes()

    def _find_shortcodes(self):
        for app in settings.INSTALLED_APPS:
            if app not in modules:
                raise ImportError("`%s` not found in sys.modules but set in "
                                  "INSTALLED_APPS" % app)

            if module_has_submodule(modules[app], 'shortcodes'):
                self.load_shortcode(modules[app])

    def load_shortcode(self, module):
        shortcodes = import_module("%s.shortcodes" % module.__name__)
        # If __path__ is not a list, we can assume there was a problem
        #   importing. This came up during development when __init__.py was
        #   missing.
        if not isinstance(shortcodes.__path__, list):
            raise ImportError("`{}.shortcodes` had an error being imported, Is"
                              " there an __init__.py?"
                              .format(module.__name__))

        py_files = []
        for path in shortcodes.__path__:
            py_files += glob.glob("{}/*.py".format(path))

        submodules = [basename(f)[:-3] for f in py_files if isfile(f) and
                      not basename(f).startswith('_')]
        for submod in submodules:
            submod = import_module("%s.shortcodes.%s" % (module.__name__,
                                                         submod))
            submod_functions = inspect.getmembers(submod, inspect.isfunction)
            for submod_function in submod_functions:
                if submod_function[0] in self._shortcodes_dict:
                    raise ValueError("{} already exists in `shortcodes_dict`."
                                     .format(submod_function[0]))
                self._shortcodes_dict[submod_function[0]] = submod_function[1]

    def expand_shortcodes(self, document):
        matches = re.finditer(self._SHORTCODE_REGEX, document)
        for result in matches:
            sequence = result.group()
            command = result.group(1).replace("-", "_").strip()
            method_name = "shortcode_%s" % command
            params = result.group(2).split(' ')
            # Remove empty items in params list
            params = [param for param in params if not param.isspace() and
                      param != '']

            shortcode_method = self._shortcodes_dict.get(method_name)
            if shortcode_method:
                print("Rendering shortcode '%s' with parameters '%s'."
                      % (command, params))
                html = shortcode_method(*params)
                document = document.replace(sequence, html)
            else:
                print("Shortcode `%s` not found." % command)

        return document
