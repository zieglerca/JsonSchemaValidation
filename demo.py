import json
import urllib.request
from os.path import join, dirname
from jsonschema import RefResolver
from jsonschema.validators import Draft4Validator

schema_uri = "https://raw.githubusercontent.com/zieglerca/JsonSchemaValidation/master/schemas/erm.json"
with urllib.request.urlopen(schema_uri) as url:
    schema = json.loads(url.read().decode())

resolver = RefResolver(base_uri=schema_uri, referrer=schema, cache_remote=True)
validator = Draft4Validator(schema, resolver=resolver)
for tc in ['ok.json', 'err.json']:
    file = join('testcases', tc)
    with open(file) as df:
        data = json.load(df)
    errors = list(validator.iter_errors(data))
    for idx, err in enumerate(errors):
        print(f"Error {idx}")
        print(f"  Message: {err.message}")
        print(f"  Path: {'>'.join(err.path)}")
        print(f"  Schema Path: {'>'.join(err.schema_path)}")