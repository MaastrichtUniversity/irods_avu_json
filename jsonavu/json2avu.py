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
        if isinstance(item, basestring) or isinstance(item, int):
            out.append({
                "a": key,
                "v": item,
                "u": prefix + "_" + str(parent) + "_" + "s"
            })
        else:
            # Not a string or int, convert objects and lists recursively
            o, new_parent = json2avu_r(item, prefix, parent, new_parent, key)
            out.extend(o)

    return out, new_parent


def array2avu(d, prefix, parent, new_parent, attribute):
    out = list()

    # Loop through array
    for idx, item in enumerate(d):
        if isinstance(item, basestring) or isinstance(item, int):
            out.append({
                "a": attribute,
                "v": item,
                "u": prefix + "_" + str(parent) + "_" + "s#" + str(idx)
            })
        else:
            # Not a string or int, convert objects and lists recursively
            o, new_parent = json2avu_r(item, prefix, parent, new_parent, attribute)

            # Append the index to the first element returned
            o[0]['u'] = o[0]['u'] + "#" + str(idx)

            out.extend(o)

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
