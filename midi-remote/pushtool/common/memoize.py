'''
This module provides decorators for managing memoization of functions.
See wiki for more info on memoization: https://en.wikipedia.org/wiki/Memoization
'''

from inspect import signature

_MEMOIZE_CACHE = {}

def _get_namespace(f, namespace=None):
    if namespace is not None:
        return namespace
    return f.__module__ + "." + f.__name__

def cached(*decorator_args, namespace=None):
    '''
    Cached decorator function will cache based on the keys used to call the decorated function.

    Args:
        *args (string[]): List of paremeters to use as a cache key in the decorated function.
        namespace (string): Namespace of the cached object.
                            Use braces (e.g '{variable}-x') to refer to
                            parameters from the decorated function.
    '''


    def decorator(f):
        args_name = signature(f).parameters.keys()
        nsp = _get_namespace(f, namespace)
        def wrapper(*args, **kwargs):
            args_dict = dict(zip(args_name, args))
            cache_container = _MEMOIZE_CACHE.setdefault(nsp.format(**args_dict), {})

            cache_key = ""
            for arg in decorator_args:
                cache_key += args_dict[arg]

            obj = cache_container.get(cache_key, None)
            if obj is not None:
                return obj

            result = f(*args, **kwargs)

            cache_container[cache_key] = result
            return result

        return wrapper
    return decorator




def clean_namespace(namespace=None):
    '''
    Decorator function to clean used namespaces upon completion of the decorated functionself.

    Args:
        namespace (string): Namespace to remove after completion of the function
    '''

    def decorator(fn):
        args_name = signature(fn).parameters.keys()
        nsp = _get_namespace(fn, namespace)
        def wrapper(*args, **kwargs):
            args_dict = dict(zip(args_name, args))
            container = nsp.format(**args_dict)

            result = fn(*args, **kwargs)

            if container in _MEMOIZE_CACHE:
                del _MEMOIZE_CACHE[container]

            return result

        return wrapper
    return decorator
