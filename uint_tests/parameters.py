import unittest
from SwaggerToCase.parse import ParseParameters
from SwaggerToCase.utils import load_by_file


class TestParser(unittest.TestCase):

    # def setUp(self):
    #     self.postman_parser = PostmanParser("tests/data/test.json")

    def test_parameters(self):
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
                        "type": "string",
                        "default": "TOAUDIT",
                        "description": "审核状态（待审核TOAUDIT，审核通过THROUGH）"
                    }}}
        }
        }
        parameters = load_by_file(r'C:\Users\Administrator\PycharmProjects\Swagger2Case\json_files\parameters.json')
        parse = ParseParameters(item["definitions"], parameters)
        parse.parse_parameters()
        print(parse.path_param)
        print(parse.query_param)
        print(parse.header_param)
        print(parse.body_param)
        print(parse.formdata_param)
        self.assertEqual(parse.path_param, [{'audit_id': 123}])
        self.assertEqual(parse.query_param, [{'page': 123}])
        self.assertEqual(parse.header_param, [{'uid': '123'}])
        self.assertEqual(parse.body_param, [{'money': 123, 'quota': True, 'status': '123'}, '123', [1, 2, 3]])
        self.assertEqual(parse.formdata_param, [{'name': '{1: 1,2: 2}'}])



