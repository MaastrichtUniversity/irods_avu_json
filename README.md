# Bidirectional conversion between JSON(-LD) and iRODS AVUs

## Rationale

JSON is a flexible and easy to use format for storing (nested) data. At the same time 
it can remain human readable. It can therefore be an ideal method for
storing metadata in iRODS. However, iRODS uses Attribute, Value, Unit triples. Its 
largest drawback being the lack of nesting. 

This Python module describes a method for converting JSON to AVU triples and back again 
(bidirectional).

## Design goals

* Bijection between JSON <-> AVU
  * i.e no limit on the characters used in an attribute
  * i.e being able to maintain order in arrays
* Lean JSON -> AVU conversion. 
  * Don't explode the JSON unnecessarily in AVUs
* Keep Attribute->Value pairs the same in JSON and AVUs. So values remain easily accessible from within iRODS
* Compatible with existing or additional AVUs 
* Compatible/aware of JSON-LD
* Unicode-safe

## Implementation
The unit is field is being used for the following purposes:

1. The JSON-AVU namespace
2. The parent object (0 by default)
3. The object type (o, s, b, a, n, z, e)
4. The array index

AVUs only allow a string value. The types are converted as follows:

* s: string 
* o: object ("o" + object_id)
* b: boolean ("True" or "False")
* n: number (String value of float or int)
* z: null (".")
* e: empty string (".") (special case as AVUs don't allow empty values)
* a: empty array (".")

## Installation
Either clone the git repository, or use pip to install the module into your Python (virtual) environment:
```bash
pip install irods_avu_json
```

### From within iRODS
This Python module, by itself, has no interaction or awareness of iRODS.

There is a companion repository [irods_avu_json-ruleset](https://github.com/MaastrichtUniversity/irods_avu_json-ruleset) that contains
all the iRODS rules, policies, and microservices to make the conversion code operational in iRODS.

### Docker
A description of a docker container running the ruleset, its microservices, and python dependencies exists in the
[irods_avu_json-docker](https://github.com/MaastrichtUniversity/irods_avu_json-docker) repository. You can use this
to quickly try out this module and test its functionality.

## Example output
```
Source:
{
    "k1": "v1",
    "k2": {
        "k3": "v2",
        "k4": "v3"
    },
    "k5": [
        "v4",
        "v5"
    ],
    "k6": [
        {
            "k7": "v6",
            "k8": "v7"
        }
    ]
}
AVUs:
      A       V               U
     k1      v1        root_0_s
     k2      o1       root_0_o1
     k3      v2        root_1_s
     k4      v3        root_1_s
     k5      v4      root_0_s#0
     k5      v5      root_0_s#1
     k6      o2     root_0_o2#0
     k7      v6        root_2_s
     k8      v7        root_2_s
JSON:
{
    "k1": "v1",
    "k2": {
        "k3": "v2",
        "k4": "v3"
    },
    "k5": [
        "v4",
        "v5"
    ],
    "k6": [
        {
            "k7": "v6",
            "k8": "v7"
        }
    ]
}
```
## Development helpers

Use the `conversion.py` script for easy development. Compatible with Python 2 and 3.

```bash
python conversion.py inputs/basic.json
```

## Testing
Tests can be run from the top-level directory (requires Python3).

```bash
python3 -m unittest test
```

## Limits

On the AVU side
* If two AVUs have the same attribute and unit but different values only the last one ends up in the JSON

## Authors
Paul van Schayck (p.vanschayck@maastrichtuniversity.nl), Ton Smeele, Daniel Theunissen and Lazlo Westerhof 

## Copyright and license

(c) Maastricht University
(c) Utrecht University

Apache License 2.0

