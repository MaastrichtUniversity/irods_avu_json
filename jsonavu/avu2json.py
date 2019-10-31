import re
import sys

RE_UNIT = '^[a-zA-Z0-9_]+_([0-9]+)_([osbanze])((?<=o)[0-9]+)?((?:#[0-9]+?)*)'
RE_INDICES = '#([0-9]+)'


def avu2json(avu, prefix, parent=0):
    data = None

    # Regular expression pattern for unit field
    pattern = re.compile(RE_UNIT)
    # Group 1: parent, group 2: var type, group 3: object id, group 4: array indices

    # Matching the array indices separately
    indices_pattern = re.compile(RE_INDICES)

    for item in avu:
        if not item['u'].startswith(prefix + "_" + str(parent) + "_"):
            continue

        # Match unit to extract all info
        unit = pattern.match(str(item['u']))

        # This AVU may be unrelated to the JSON
        if not unit:
            continue

        # Extract var type and object ID from regex
        var_type = unit.group(2)
        object_id = int(unit.group(3)) if unit.group(3) else None

        # Extract array indices
        array_indices = None
        if unit.group(4):
            array_indices = indices_pattern.findall(unit.group(4))

            # Convert to integers
            array_indices = list(map(int, array_indices))

        if not isinstance(data, dict):
            data = dict()

        # Check for new object in value
        if var_type == "o":
            key = item['a']

            # Recursively check the unit/subject field for new AVUs with this new namespace
            value = avu2json(avu, prefix, object_id)

            # If the object exists but is empty, return an empty object as well
            if value is None:
                value = {}
        else:
            key = item['a']
            value = def2type(item['v'], var_type)

        # Build array if it doesn't exist yet
        if array_indices is not None and key not in data:
            data[key] = list()

        # Store item in data
        if key in data and isinstance(data[key], list):
            # It's a list item, place it back at correct index of the potential multidimensional list
            multi_dim_list_insert(data[key], array_indices, value)
        else:
            data[key] = value

    return data


def multi_dim_list_insert(data, array_indices, value):
    # Get first element from list and remove that
    idx = array_indices.pop(0)

    if len(array_indices) > 0:
        # Check if we need to make new list
        try:
            data[idx]
        except IndexError:
            data.insert(idx, list())

        # Recursively handle multi dimensional list
        return multi_dim_list_insert(data[idx], array_indices, value)
    else:
        return data.insert(idx, value)


def def2type(v, t):
    if t == 's':
        if (sys.version_info < (3, 0)):
            return v.encode('utf-8')
        else:
            return str(v)
    elif t == 'e':
        return ""
    elif t == 'b':
        if v == 'True':
            return True
        elif v == 'False':
            return False
        else:
            raise Exception("Invalid boolean value")
    elif t == 'n':
        try:
            return int(v)
        except ValueError:
            return float(v)
    elif t == 'z':
        return None
    elif t == 'a':
        return []
    else:
        raise Exception("Type does not exist")
