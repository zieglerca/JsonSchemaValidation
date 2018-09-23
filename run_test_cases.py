from os.path import join, dirname
from jsonschema import validate, RefResolver
import json
from jsonschema.validators import Draft4Validator
import urllib.request

def printErrors(errors):
    for idx, err in enumerate(errors):
        print(f"Error {idx}")
        print(f"  Message: {err.message}")
        print(f"  Path: {'>'.join(err.path)}")
        print(f"  Schema Path: {'>'.join(err.schema_path)}")

'''
# load ERM schema
relative_path = join('schemas', 'erm.json')
absolute_path = join(dirname(__file__), relative_path)
with open(absolute_path) as sf:
    schema = json.load(sf)
'''

schema_uri = "https://raw.githubusercontent.com/zieglerca/JsonSchemaValidation/master/schemas/erm.json"
# load ERM schema from Github
with urllib.request.urlopen(schema_uri) as url:
    schema = json.loads(url.read().decode())

'''
# this validator just returns the first error as an exception
for tc in ['testcase1.json', 'testcase2.json']:
    # load test case
    with open(tc) as df: data = json.load(df)
    # validate test case
    try:
        validate(data, schema)
    except Exception as e:
        print("completed with error: {tc}")
        print(e)
    else:
        print("completed successfully: {tc}")

# this validator returns all errors in a structured format (better)
validator = Draft4Validator(schema)
for tc in ['testcase1.json', 'testcase2.json']:
    # load test case
    with open(tc) as df: data = json.load(df)
    # validate test case
    errors = list(validator.iter_errors(data))
    printErrors(errors)
'''
# this validator returns all errors in a structured format (better) AND uses a resolver for remote references
resolver = RefResolver(base_uri=schema_uri, referrer=schema, cache_remote=True )
validator = Draft4Validator(schema, resolver=resolver)
for tc in ['testcase1.json', 'testcase2.json']:
    # load test case
    with open(tc) as df: data = json.load(df)
    # validate test case
    errors = list(validator.iter_errors(data))
    printErrors(errors)
