#!/usr/bin/python3

import json
import sys

import jsonavu

with open(sys.argv[1]) as f:
    data = json.load(f)

avu = jsonavu.json2avu(data, "root")

print("Source:")
if (sys.version_info < (3, 0)):
    print(json.dumps(data, indent=4, ensure_ascii=False, encoding='utf8'))
else:
    print(json.dumps(data, indent=4, ensure_ascii=False).encode('utf8').decode())

# Find out max V length and use that for formatting
max_a_len = len(max(avu, key=lambda k: len(k["a"].encode('utf-8')))["a"])
max_v_len = len(max(avu, key=lambda k: len(k["v"].encode('utf-8')))["v"])
out_format = "%" + str(max_a_len + 5) + "s %" + str(max_v_len + 5) + "s %15s"

print("AVUs:")
print(out_format % ("A", "V", "U"))
for i in avu:
    print(out_format % (i["a"], i["v"], i["u"]))

print("JSON:")
data_back = jsonavu.avu2json(avu, "root")
if (sys.version_info < (3, 0)):
    print(json.dumps(data_back, indent=4, ensure_ascii=False, encoding='utf8'))
else:
    print(json.dumps(data_back, indent=4, ensure_ascii=False).encode('utf8').decode())
