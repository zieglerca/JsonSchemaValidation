# JSON Schema Validation
## About JSON Schema Validation
The code in [this repository](https://github.com/zieglerca/JsonSchemaValidation)
tests out some options to validate JSON files against a 
[JSON schema]( https://json-schema.org/). JSON schemas are an excellent 
tool to describe data structures. They are used in API and message 
payload descriptions such as in 
[OpenAPI](https://en.wikipedia.org/wiki/OpenAPI_Specification) and 
[AsyncAPI](https://www.asyncapi.com/) specifications. 
A component may provide JSON schemas also to a consumer so that 
JSON payloads or files for a service or API call can be tested 
beforehand. Conversion between JSON and YAML is easily possible 
making JSON schema also an option for YAML payloads and files.  

## Repository Structure
The repository consists of two directories and two files: 
1. Directory **schemas** contains json schema files with erm.json using project.json using types.json..
1. Directoy **testcases** contains two test cases, "ok" is valid and "err" is invalid.
1. File **demo.py** contains a simple code example.
1. File **tests.py** contains some unit tests using a local and a remote schema for 
the validation of the test cases.

## Quick Walk-Through
For a beginner it is best to start with demo.py.
Some imports are reuqired. The latest version of jsonschema can be installed 
from [Julian's Python Validator Repository](https://github.com/Julian/jsonschema).
    
    import json
    import urllib.request
    from os.path import join, dirname
    from jsonschema import RefResolver
    from jsonschema.validators import Draft4Validator
    
The schema file is loaed. In this case I use the raw format in the repository.
    
    schema_uri = "https://raw.githubusercontent.com/zieglerca/JsonSchemaValidation/master/schemas/erm.json"
    with urllib.request.urlopen(schema_uri) as url:
        schema = json.loads(url.read().decode())
    
Next a reference resolver is needed because the schema file includes references 
to other schema files. It is generally good practice to share schema definitions 
used in multiple files instead of repetition in those files. 
    
    resolver = RefResolver(base_uri=schema_uri, referrer=schema, cache_remote=True)
    
With the resolver a validator can be retrieved.
    
    validator = Draft4Validator(schema, resolver=resolver)

Preparation for the validation is completed. Files ok.json and err.json are 
loaded and tested with the validator. The validator may return multiple errors. 

    for tc in ['ok.json', 'err.json']:
        file = join('testcases', tc)
        with open(file) as df:
            data = json.load(df)
        errors = list(validator.iter_errors(data))
        
Output of errors from the validation.
        
        for idx, err in enumerate(errors):
            print(f"Error {idx}")
            print(f"  Message: {err.message}")
            print(f"  Path: {'>'.join(err.path)}")
            print(f"  Schema Path: {'>'.join(err.schema_path)}")
            
The test cases show how to validate using local schema files with a local reference 
Resolver. 

## Resources
1. [JSON Schema Project (incl. Docu)]( https://json-schema.org/)
1. [Python Validator](https://github.com/Julian/jsonschema)
1. [Python validator documentation](https://python-jsonschema.readthedocs.io/en/latest/#)
1. [Training](https://json-schema.org/understanding-json-schema/index.html)
1. [Online Validator](https://www.jsonschemavalidator.net/)


