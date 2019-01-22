#!/usr/bin/python3

import json

# Fix to check for string type in both python 2 and python 3
try:
    # noinspection PyUnboundLocalVariable
    basestring
except NameError:
    basestring = str


def obj2avu(d, root, blank):
    out = list()

    # Loop through object
    for key, item in d.items():
        if key == "@context":
            continue

        if isinstance(item, basestring):
            out.append({
                "a": key,
                "v": item,
                "u": root
            })
        elif isinstance(item, int):
            out.append({
                "a": key,
                "v": item,
                "u": root
            })
        else:
            # Not a string, convert objects and lists recursively
            o, blank = json2avu_r(item, root, key, blank)
            out.extend(o)

    return out, blank


def array2avu(d, root, attribute, blank):
    out = list()

    # Loop through array
    for idx, item in enumerate(d):
        # Add the index of the array as part of the subject/unit
        u = root + "#" + str(idx)

        if isinstance(item, basestring):
            out.append({
                "a": attribute,
                "v": item,
                "u": u
            })
        elif isinstance(item, int):
            out.append({
                "a": attribute,
                "v": item,
                "u": u
            })
        else:
            # Not a string, convert objects and lists recursively
            o, blank = json2avu_r(item, u, attribute, blank)
            out.extend(o)

    return out, blank


def json2avu_r(d, root, attribute, blank):
    out = list()

    if isinstance(d, dict):
        # Create blank node
        out.append({
            "a": attribute,
            "v": "_b" + str(blank),
            "u": root
        })

        # Set new root
        root = "_b" + str(blank)

        # Increase blank node
        blank = blank + 1

        o, blank = obj2avu(d, root, blank)
        out.extend(o)
    elif isinstance(d, list):
        o, blank = array2avu(d, root, attribute, blank)
        out.extend(o)

    return out, blank


def json2avu(d, root):
    # List of dictionaries to hold AVUs
    out = list()

    # Start at blank node 0
    blank = 0

    if isinstance(d, basestring):
        # Handle special case where there is only a string
        out = [{
            "a": d,
            "v": d,
            "u": root
        }]
    elif isinstance(d, dict):
        out, _ = obj2avu(d, root, blank)
    elif isinstance(d, list):
        out, _ = array2avu(d, root, root, blank)

    return out


with open('inputs/basic.json') as f:
    data = json.load(f)

avu = json2avu(data, "root")

print(json.dumps(data, indent=4))

# Find out max V length and use that for formatting
max_v_len = len(max(avu, key=lambda k: len(str(k["v"])))["v"])
out_format = "%30s %" + str(max_v_len + 5) + "s %10s"

print(out_format % ("A", "V", "U"))
print(out_format % ("P", "O", "S"))
for i in avu:
    print(out_format % (i["a"], i["v"], i["u"]))
