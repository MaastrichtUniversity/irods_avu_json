import re


def avu2json(avu, root):
    data = None
    idx = 0

    # Regular expression patterns
    blank_node_pattern = re.compile('^_b[0-9]+$')
    array_index_pattern = re.compile('^[a-zA-Z0-9_]+#([0-9]+)$')

    for item in avu:
        if not item['u'].startswith(root):
            continue

        if not isinstance(data, dict):
            data = dict()

        # Check for array in unit
        array_index = array_index_pattern.match(str(item['u']))
        if array_index:
            key = item['a']
            idx = int(array_index.group(1))

            # Build array if it doesn't exist yet
            if key not in data:
                data[key] = list()

        # Check for blank node in value
        if blank_node_pattern.match(str(item['v'])):
            # Blank node
            key = item['a']

            # Recursively check the unit/subject field for new AVUs with this new root
            value = avu2json(avu, item['v'])

            # This may not be a true blank node, then handle the value as a normal string
            if value is None:
                value = item['v']
        else:
            key = item['a']
            value = item['v']

        # Store item in data
        if key in data and isinstance(data[key], list):
            # It's a list item, place it back at correct index
            data[key].insert(idx, value)
        else:
            data[key] = value

    return data
