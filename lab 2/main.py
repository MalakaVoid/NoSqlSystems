import json

from jsonschema import validate

f = open("example.json")
data = json.load(f)
f = open("json-schema.json")
schema = json.load(f)

validate(data, schema)