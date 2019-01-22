# iRODS bidirectional conversion of JSON to AVU and back

## Running

Compatible with Python 2 and 3.

```bash
python conversion.py
```

## Output
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

