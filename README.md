# Bidirectional conversion between JSON(-LD) and iRODS AVUs

## Rationale

JSON is a flexible and easy to use format for storing (nested) data. At the same time 
it can remain human readable. It can therefor be an ideal method for 
storing metadata in iRODS. However, iRODS uses Attribute, Value, Unit triples. Its 
largest drawback being the lack of nesting. 

This script describes a method for converting JSON to AVU triples and back again 
(bidirectional).

## Design goals

* Lean JSON -> AVU conversion. Don't explode the JSON unnecessarily in AVUs
* Being able to maintain order in JSON arrays
* Should not place any restrictions on the JSON input (i.e limit the characters used in an attribute)
* Keep Attribute->Value pairs the same in JSON and AVUs (for both arrays and objects). So they remain easily accessible in default rule language and genquery.
* Compatible with existing or additional AVUs already present on an object
* Validatable by JSON-schema files
* Compatible/aware of JSON-LD


## Implementation
Took ideas from RDF.

## How to run

Compatible with Python 2 and 3.

```bash
python conversion.py
```

## Example output
```
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

         A          V          U
         P          O          S
        k1         v1       root
        k2        _b0       root
        k3         v2        _b0
        k4         v3        _b0
        k5         v4     root#0
        k5         v5     root#1
        k6        _b1     root#0
        k7         v6        _b1
        k8         v7        _b1
```

## Limits

* If two AVUs have the same attribute but different values 