''' Decorators '''

from .logger import LOGGER

def _object_as_dict(obj):
    if obj:
        return obj.__dict__
    else:
        return {}


def patch_method(obj, log_original=False):
    ''' Decorator for swapping original function with a new implementation on given obj
        Usage: @patch_mehod(Device) function_name_to_replace
    '''
    def decorator(func):
        _orig = None
        _fn_name = func.__name__
        try:
            _orig = getattr(obj, _fn_name)
        except AttributeError as err:
            LOGGER.error(str(err))
            return None

        def wrapper(*args, **kwargs):
            result = None

            try:
                result = func(*args, **kwargs)
            except Exception as err: # pylint: disable=broad-except
                LOGGER.error(str(err))

            if result:
                return result

            if _orig:
                result = _orig(*args, **kwargs) if _orig else None
                if log_original:
                    if type(result) == tuple:
                        for obj in result[1]:
                            LOGGER.info(_object_as_dict(obj[0]))

                    LOGGER.info("Method {} returned: ".format(_fn_name))
                    LOGGER.info(result)
                return result

            LOGGER.info("Method {} not found on origin object".format(_fn_name))
            return None

        # Swap function
        setattr(obj, _fn_name, wrapper)

        return func
    return decorator
