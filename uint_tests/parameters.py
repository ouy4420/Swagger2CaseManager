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
        self.assertEqual(parse.path_param, [{'name': 'audit_id', 'in': 'path', 'description': 'audit_id', 'required': True, 'type': 'integer', 'format': 'int64'}])
        self.assertEqual(parse.query_param, [{'name': 'page', 'in': 'query', 'description': '当前页', 'required': True, 'type': 'integer', 'format': 'int32', 'x-example': 10}])
        self.assertEqual(parse.header_param, [{'name': 'uid', 'in': 'header', 'description': '会员ID', 'required': True, 'type': 'string'}])
        self.assertEqual(parse.body_param, [{'money': 21.3, 'quota': True, 'status': 'TOAUDIT'}, '123', [1, 2, 3]])
        self.assertEqual(parse.formdata_param, [{'name': '{1: 1,2: 2}'}])



