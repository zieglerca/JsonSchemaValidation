from os.path import join, dirname, sep, realpath
from jsonschema import validate, RefResolver
import json
import sys
import jsonref

# load ERM schema
relative_path = join('schemas', 'erm.json')
absolute_path = join(dirname(__file__), relative_path)
with open(absolute_path) as sf:
    schema = json.load(sf)

for tc in ['testcase1.json', 'testcase2.json']:
    # load test case
    with open(tc) as df:
        data = json.load(df)

    # validate test case
    try:
        validate(data, schema)
    except Exception as e:
        print("completed with error: {tc}")
        print(e)
    else:
        print("completed successfully: {tc}")