import imp
import inspect
import os
import six

__version__ = '0.1.0'

__all__ = [
    'Required',
    'inject',
]


class _Required(object):
    """Object that indicates that a variable must be defined externally."""
    pass
Required = _Required()


class VarNotDefined(Exception):
    """
    Raised if the external config fails to define a variable that the main
    config requires.
    """
    pass


class UnknownVarDefined(Exception):
    """
    Raised if the external config defines a variable that the main config
    hasn't defined.
    """
    pass


def _get(key, default=None):
    """Use it if a setting may not exist, and a default is necessary"""
    return globals().get(key, default)


def inject(path):
    """
    Injects the uppercase global variables in the Python module at the given
    filesystem path into the invoker's global variables.

    Args:
        path (str): The filesystem path to the Python module to import and
            inject into the invoker's global variables.
    """

    if os.path.exists(path):
        if six.PY2:
            loaded_conf = imp.load_source(
                'pyconfimporter.loaded', path)
        else:
            from importlib.machinery import SourceFileLoader
            loaded_conf = SourceFileLoader(
                'pyconfimporter.loaded', path).load_module()

        if six.PY2:
            env = inspect.stack()[1][0].f_globals
        else:
            env = inspect.stack()[1].frame.f_globals

        # copy all uppercase keys from service settings file to this file
        for key in dir(loaded_conf):
            if key.isupper():
                if key not in env:
                    raise UnknownVarDefined(
                        'Unknown variable defined: %s' % key)
                env[key] = getattr(loaded_conf, key)
    else:
        raise IOError('Could not find {}'.format(path))

    for key, val in env.items():
        if key.isupper() and env[key] == Required:
            raise VarNotDefined('Required variable not defined: %s' % key)

    env['get'] = _get
