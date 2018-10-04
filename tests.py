import json
import urllib.request
import unittest
import os, sys
from jsonschema.validators import Draft4Validator
from jsonschema import RefResolver


class SchemaValidationTests(unittest.TestCase):

    def printErrors(self, errors):
        for idx, err in enumerate(errors):
            print(f"Error {idx}")
            print(f"  Message: {err.message}")
            print(f"  Path: {'>'.join(err.path)}")
            print(f"  Schema Path: {'>'.join(err.schema_path)}")

    def loadTestCase(self, name):
        file = os.path.join('testcases', name)
        with open(file) as df:
            return json.load(df)

    def loadSchema(self, file=None, uri=None):
        if uri:
            url = uri
        elif file:
            with open(os.path.join('schemas', file)) as sf:
                return json.load(sf)
        else:
            url = "https://raw.githubusercontent.com/zieglerca/JsonSchemaValidation/master/schemas/erm.json"
        with urllib.request.urlopen(url) as sf:
            return json.loads(sf.read().decode())

    def getRefResolver(self, file=None, uri=None):
        if file:
            schema_path = os.path.dirname(os.path.abspath(__file__))
            if sys.platform == "win32":
                schema_path = schema_path.replace('\\', '/')
                fn = f"file:///{schema_path}/schemas/"      # three /
            else:
                fn = f"file://{schema_path}/schemas/"       # two /
            schema_file = self.loadSchema(file=file)
            return RefResolver(base_uri=fn, referrer=schema_file)
        else:
            schema_file = self.loadSchema(uri=uri)
            return RefResolver(base_uri=uri, referrer=schema_file, cache_remote=True)

    def runTestCase(self, testcase, schema_file=None, schema_uri=None, errors=False):
        if schema_file:
            resolver = self.getRefResolver(file=schema_file)
            schema = self.loadSchema(file=schema_file)
        else:
            resolver = self.getRefResolver(uri=schema_uri)
            schema = self.loadSchema(uri=schema_uri)
        validator = Draft4Validator(schema, resolver=resolver)
        tc = self.loadTestCase(testcase)
        err = list(validator.iter_errors(tc))
        self.printErrors(err)
        if errors:
            self.assertTrue(err)
        else:
            self.assertFalse(err)

    def test_ok_file(self):
        print("\nTest Case: Validation using local schema with no errors")
        self.runTestCase(testcase='ok.json', schema_file='erm.json', errors=False)

    def test_err_file(self):
        print("\nTest Case: Validation using local schema with errors")
        self.runTestCase(testcase='err.json', schema_file='erm.json', errors=True)

    def test_ok_url(self):
        print("\nTest Case: Validation using remote schema with no errors")
        url = "https://raw.githubusercontent.com/zieglerca/JsonSchemaValidation/master/schemas/erm.json"
        self.runTestCase(testcase='ok.json', schema_uri=url, errors=False)

    def test_err_url(self):
        print("\nTest Case: Validation using remote schema with errors")
        url = "https://raw.githubusercontent.com/zieglerca/JsonSchemaValidation/master/schemas/erm.json"
        self.runTestCase(testcase='err.json', schema_uri=url, errors=True)