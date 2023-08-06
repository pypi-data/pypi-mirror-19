__author__ = 'dpepper'
__version__ = '0.1.0'


import __builtin__
import forbiddenfruit
import sys
import types


def rekey(obj, key_handle = None, value_handle = None):
    if type(obj) not in [list, dict]:
        raise ValueError

    if key_handle == None and value_handle == None:
        raise ValueError

    # determine return type
    if key_handle or type(obj) == dict:
        res = {}
    else:
        res = []

    # figure out how to iterate
    if hasattr(obj, 'items'):
        _iter = obj.items()
    else:
        _iter = obj


    for items in _iter:
        # unpack potential key / value tuple
        if type(items) == tuple:
            key, value = items
        else:
            key, value = None, items

        # set default result values
        new_key, new_value = key, value

        # grab new key / value
        if key_handle != None:
            new_key = pull(value, key_handle)

        if value_handle != None:
            new_value = pull(value, value_handle)

        # store results
        if type(res) == list:
            res.append(new_value)
        else:
            res[new_key] = new_value

    return res


def pull(obj, handle):
    # function pointer...pass in value
    if callable(handle):
        return handle(obj)

    # dict key
    if hasattr(obj, 'has_key') and obj.has_key(handle):
        return obj[handle]

    # list index
    if type(obj) == list and type(handle) == int:
        return obj[handle]

    # object attribute or instance method
    if hasattr(obj, handle):
        attr = getattr(obj, handle)
        if callable(attr):
            return attr()

        return attr

    # regular old function
    if globals().has_key(handle):
        return globals()[handle](obj)

    # built in function
    if hasattr(__builtin__, handle):
        return getattr(__builtin__, handle)(obj)

    raise TypeError('invalid handle: ' + handle)


def install():
    forbiddenfruit.curse(dict, 'rekey', rekey)
    forbiddenfruit.curse(list, 'rekey', rekey)


def uninstall():
    forbiddenfruit.reverse(dict, 'rekey')
    forbiddenfruit.reverse(list, 'rekey')


# wire it up
install()
