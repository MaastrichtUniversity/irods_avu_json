#!/usr/bin/python3

import json

# Fix to make code compatible in python 3 and python 3
try:
    # noinspection PyUnboundLocalVariable
    basestring
except NameError:
    basestring = str


def obj2avu(d, root, blank):
    out = list()

    # Loop through object
    for key, item in d.items():
        if isinstance(item, basestring):
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
        if isinstance(item, basestring):
            out.append({
                "a": attribute,
                "v": item,
                "u": root + "#" + str(idx)
            })
        else:
            # Not a string, convert objects and lists recursively
            o, blank = json2avu_r(item, root, attribute, blank)
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

    if isinstance(d, str):
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

print("%10s %10s %10s" % ("a", "v", "u"))
print("%10s %10s %10s" % ("p", "o", "s"))
for i in avu:
    print("%10s %10s %10s" % (i["a"], i["v"], i["u"]))
