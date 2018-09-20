# https://spacetelescope.github.io/understanding-json-schema/index.html
# https://stackoverflow.com/questions/8595832/does-json-schema-validation-in-common-js-utils-support-references/9083630#9083630
# https://python-jsonschema.readthedocs.io/en/latest/

# see also https://github.com/Julian/jsonschema/issues/343 for references
# !!! https://medium.com/grammofy/handling-complex-json-schemas-in-python-9eacc04a60cf !!!


from os.path import join, dirname, sep, realpath
from jsonschema import validate, RefResolver
import json
import sys
import jsonref

with open('erm.json') as sf:
    schema = json.load(sf)

schemas_dir = dirname(realpath('erm.json'))
resolver = RefResolver(referrer=schema, base_uri='file://' + schemas_dir)

with open('testcase1.json') as df:
    data = json.load(df)

try:
    validate(data, schema, resolver=resolver)
except Exception as e:
    print(e)
print("done case 1")


with open('testcase2.json') as df:
    data = json.load(df)

try:
    validate(data, schema, resolver=resolver)
except Exception as e:
    print(e)
print("done case 2")


'''relative_path = join('schemas', 'erm.json')
absolute_path = join(dirname(__file__), relative_path)

base_path = dirname(absolute_path)
base_uri = f'file://{base_path}{sep}'


with open(absolute_path) as sf:
    schema = json.load(sf)

with open('testcase1.json') as df:
    data = json.load(df)

try:
    validate(data, schema, resolver=resolver)
except Exception as e:
    print(e)
print("done")


with open(absolute_path) as sf:
    schema = jsonref.loads(sf.read(), base_uri=base_uri, jsonschema=True)

with open('testcase1.json') as df:
    data = json.load(df)

try:
    validate(data, schema)
except Exception as e:
    print(e)
print("done")
'''

# also tried "project.json#/definitions/Project"} and other options as described in the web sties above
# no success