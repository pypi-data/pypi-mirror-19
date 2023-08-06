import ast
import logging
import os

from pkg_resources import working_set

logger = logging.getLogger(__name__)

ENTRY_POINT_APP = 'powerplug.apps'


def add_apps(installed_apps):
    for entry in working_set.iter_entry_points(ENTRY_POINT_APP):
        if entry.module_name not in installed_apps:
            installed_apps += (entry.module_name,)
    return installed_apps


def environ(key, default=None):
    """
        Searches os.environ. If a key is found try evaluating its type else;
        return the string.
        returns: k->value (type as defined by ast.literal_eval)
    """
    # Taken from
    # https://github.com/mattseymour/python-env/blob/master/dotenv/__init__.py
    try:
        # Attempt to evaluate into python literal
        return ast.literal_eval(os.environ.get(key.upper(), default))
    except (ValueError, SyntaxError):
        return os.environ.get(key.upper(), default)
