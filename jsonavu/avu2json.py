import re


def avu2json(avu, prefix, parent=0):
    data = None

    # Regular expression pattern for unit field
    pattern = re.compile('^[a-zA-Z0-9_]+_([0-9]+)_([osbnze])((?<=o)[0-9]+)?#?([0-9]+)?')
    # Group 1: parent, group 2: var type, group 3: object id, group 4: array index

    for item in avu:
        if not item['u'].startswith(prefix + "_" + str(parent)):
            continue

        # Match unit to extract all info
        unit = pattern.match(str(item['u']))

        # This AVU may be unrelated to the JSON
        if not unit:
            continue

        # Extract info from regex
        var_type = unit.group(2)
        object_id = int(unit.group(3)) if unit.group(3) else None
        array_idx = int(unit.group(4)) if unit.group(4) else None

        if not isinstance(data, dict):
            data = dict()

        # Check for new object in value
        if var_type == "o":
            key = item['a']

            # Recursively check the unit/subject field for new AVUs with this new root
            value = avu2json(avu, prefix, object_id)
        else:
            key = item['a']
            value = def2type(item['v'], var_type)

        # Build array if it doesn't exist yet
        if array_idx is not None and key not in data:
            data[key] = list()

        # Store item in data
        if key in data and isinstance(data[key], list):
            # It's a list item, place it back at correct index
            data[key].insert(array_idx, value)
        else:
            data[key] = value

    return data


def def2type(v, t):
    if t == 's':
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
    else:
        raise Exception("Type does not exist")
