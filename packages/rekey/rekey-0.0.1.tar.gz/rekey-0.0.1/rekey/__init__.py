__author__ = 'dpepper'
__version__ = '0.0.1'


import __builtin__
import forbiddenfruit
import sys


def rekey(obj, key_handle = None, value_handle = None):
    if type(obj) not in [list, dict]:
        raise ValueError

    if not (key_handle or value_handle):
        raise ValueError

    if key_handle:
        res = {}
    else:
        res = []

    for value in obj:
        new_key = pull(value, key_handle) if key_handle else None
        new_value = pull(value, value_handle) if value_handle else None

        if new_key:
            res[new_key] = new_value if value_handle else value
        else:
            res.append(new_value)

    return res


def pull(obj, handle):
    print obj

    if hasattr(obj, handle):
        attr = getattr(obj, handle)
        if callable(attr):
            return attr()

        return attr
            # if attr.func_code.co_argcount == 0:
            #     return attr()
            # return attr(obj)

    # dict key
    if hasattr(obj, 'has_key') and obj.has_key(handle):
        return obj[handle]

    # function pointer...pass in value
    if callable(handle):
        return handle(obj)

    # regular old function
    if globals().has_key(handle):
        return globals()[handle](obj)

    # built in function
    if hasattr(__builtin__, handle):
        return getattr(__builtin__, handle)(obj)

    return None


def install():
    forbiddenfruit.curse(list, 'rekey', rekey)


def uninstall():
    forbiddenfruit.reverse(list, 'rekey')


# wire it up
install()
