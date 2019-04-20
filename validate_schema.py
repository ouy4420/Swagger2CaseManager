from jsonschema import validate
from jsonschema.exceptions import ValidationError

schema = {
        "properties": {
            "language": {
                "type": "string",
                "default": "TheLanguage"
            },
            "id": {
                "type": "integer",
                "default": "ID"
            }
        },
        "type": "object"
    }
test_input = {'language': 'java', 'id': 1}
try:
    validate(test_input, schema)
except ValidationError:
    print('It is not a valid collection!')
else:
    print('It is a valid collection!')


