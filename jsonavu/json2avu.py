import json

# Workaround to check for string type in both python 2 and python 3
try:
    # noinspection PyUnboundLocalVariable,PyUnresolvedReferences
    basestring
except NameError:
    basestring = str


def obj2avu(d, prefix, parent, new_parent):
    out = list()

    # Loop through object
    for key, item in d.items():
        if isinstance(item, dict) or isinstance(item, list):
            # Convert objects and lists recursively
            o, new_parent = json2avu_r(item, prefix, parent, new_parent, key)
            out.extend(o)
        else:
            out.append({
                "a": key,
                "v": type2str(item),
                "u": prefix + "_" + str(parent) + "_" + type2def(item)
            })

    return out, new_parent


def array2avu(d, prefix, parent, new_parent, attribute):
    out = list()

    # Loop through array
    for idx, item in enumerate(d):
        if isinstance(item, dict) or isinstance(item, list):
            # Not a string or int, convert objects and lists recursively
            o, new_parent = json2avu_r(item, prefix, parent, new_parent, attribute)

            # Append the index to the first element returned
            o[0]['u'] = o[0]['u'] + "#" + str(idx)

            out.extend(o)
        else:
            out.append({
                "a": attribute,
                "v": type2str(item),
                "u": prefix + "_" + str(parent) + "_" + type2def(item) + "#" + str(idx)
            })

    return out, new_parent


def json2avu_r(d, prefix, parent, new_parent, attribute):
    out = list()

    if isinstance(d, dict):
        # Increase parent counter
        new_parent = new_parent + 1

        # Create a new parent
        out.append({
            "a": attribute,
            "v": ".",
            "u": prefix + "_" + str(parent) + "_" + "o" + str(new_parent)
        })

        o, parent = obj2avu(d, prefix, new_parent, new_parent)
        out.extend(o)
    elif isinstance(d, list):
        o, parent = array2avu(d, prefix, parent, new_parent, attribute)
        out.extend(o)

    return out, parent


def json2avu(d, prefix):
    # List of dictionaries to hold AVUs
    out = list()

    # Start at parent 0
    parent = 0

    if isinstance(d, basestring) or isinstance(d, int):
        # Handle special case where there is only a string or integer
        out = [{
            "a": prefix,
            "v": d,
            "u": prefix
        }]
    elif isinstance(d, dict):
        out, _ = obj2avu(d, prefix, parent, parent)
    elif isinstance(d, list):
        out, _ = array2avu(d, prefix, parent, parent, prefix)

    return out


def type2def(var):
    if isinstance(var, basestring):
        return 's'
    elif isinstance(var, bool):
        return 'b'
    elif isinstance(var, int):
        return 'n'
    elif isinstance(var, float):
        return 'n'
    elif var is None:
        return 'z'


def type2str(var):
    if isinstance(var, basestring):
        return var
    elif isinstance(var, bool):
        return str(var)
    elif isinstance(var, int):
        return str(var)
    elif isinstance(var, float):
        return str(var)
    elif var is None:
        return '.'
