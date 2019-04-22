import unittest
from SwaggerToCase.parser import ParseParameters
from SwaggerToCase.loader import load_by_file


class TestDefinitions(unittest.TestCase):
    def setUp(self):
        item = {"definitions": {
            "WechatAuthParams": {
                "type": "object",
                "properties": {
                    "money": {
                        "type": "number",
                        "default": 21.3,
                        "description": "提现金额"
                    },
                    "quota": {
                        "type": "boolean",
                        "default": True,
                        "description": "是否超过限额,True超过,False未超过"
                    },
                    "status": {
                        "default": "TOAUDIT",
                        "items": {
                            "$ref": "#/definitions/haha"
                        }
                    },
                    "order": {
                        "type": "array",
                        "example": [
                            {
                                "order_id": "13",
                                "gold": 1.2
                            },
                            {
                                "order_id": "14",
                                "gold": 1.4
                            }
                        ],
                        "description": "订单使用金币信息",
                        "items": {
                            "$ref": "#/definitions/haha"
                        }
                    }
                }},
            "haha": {
                "type": "object",
                "properties": {
                    "haha1": {
                        "type": "number",
                        "default": 21.3,
                        "description": "提现金额"
                    },
                    "haha2": {
                        "type": "boolean",
                        "default": True,
                        "description": "是否超过限额,True超过,False未超过"
                    }

                }
            }
        }}
        self.definitions = item["definitions"]
        self.parameters = load_by_file(r'C:\Users\Administrator\PycharmProjects\Swagger2Case\json_files\parameters.json')

    def test_common(self):
        parse = ParseParameters(self.definitions, self.parameters)
        data = parse.parse_from_definitons("#/definitions/WechatAuthParams")
        self.assertEqual(data['money'], 123)
        self.assertEqual(data['quota'], True)

    def test_object(self):
        parse = ParseParameters(self.definitions, self.parameters)
        data = parse.parse_from_definitons("#/definitions/WechatAuthParams")
        self.assertEqual(data['status'], {'haha1': 123, 'haha2': True})

    def test_array(self):
        parse = ParseParameters(self.definitions, self.parameters)
        data = parse.parse_from_definitons("#/definitions/WechatAuthParams")
        self.assertEqual(data['order'], [{'haha1': 123, 'haha2': True}, {'haha1': 123, 'haha2': True}])


if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestDefinitions)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
