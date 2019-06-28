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
            o, new_parent = json2avu_r(item, prefix, parent, new_parent, key, "")
            out.extend(o)
        else:
            out.append({
                "a": key,
                "v": type2str(item),
                "u": prefix + "_" + str(parent) + "_" + type2def(item)
            })

    return out, new_parent


def array2avu(d, prefix, parent, new_parent, attribute, index):
    out = list()

    # Empty list
    if not d:
        out.append({
            "a": attribute,
            "v": ".",
            "u": prefix + "_" + str(parent) + "_a" + index
        })
        return out, new_parent

    # Loop through array
    for idx, item in enumerate(d):
        # Append the index to any existing index
        new_index = index + "#" + str(idx)

        if isinstance(item, dict) or isinstance(item, list):
            # Not a string or int, convert objects and lists recursively
            o, new_parent = json2avu_r(item, prefix, parent, new_parent, attribute, new_index)

            out.extend(o)
        else:
            out.append({
                "a": attribute,
                "v": type2str(item),
                "u": prefix + "_" + str(parent) + "_" + type2def(item) + new_index
            })

    return out, new_parent


def json2avu_r(d, prefix, parent, new_parent, attribute, index):
    out = list()

    if isinstance(d, dict):
        # Increase parent counter
        new_parent = new_parent + 1

        # Create a new parent
        out.append({
            "a": attribute,
            "v": "o" + str(new_parent),
            "u": prefix + "_" + str(parent) + "_" + "o" + str(new_parent) + index
        })

        o, parent = obj2avu(d, prefix, new_parent, new_parent)
        out.extend(o)
    elif isinstance(d, list):
        o, parent = array2avu(d, prefix, parent, new_parent, attribute, index)
        out.extend(o)

    return out, parent


def json2avu(d, prefix):
    # Start at parent 0
    parent = 0

    # Start without an array index
    index = ""

    if isinstance(d, dict):
        out, _ = obj2avu(d, prefix, parent, parent)
    elif isinstance(d, list):
        out, _ = array2avu(d, prefix, parent, parent, prefix, index)
    else:
        # Handle special case where there is only a primitive
        out = [{
            "a": prefix,
            "v": type2str(d),
            "u": prefix + "_" + str(parent) + "_" + type2def(d)
        }]

    return out


def type2def(var):
    if isinstance(var, basestring):
        if var == "":
            return 'e'
        else:
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
        if var == "":
            return '.'
        else:
            return var
    elif isinstance(var, bool):
        return str(var)
    elif isinstance(var, int):
        return str(var)
    elif isinstance(var, float):
        return str(var)
    elif var is None:
        return '.'
