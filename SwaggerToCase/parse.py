import json


class ParsePostData(object):
    @staticmethod
    def parse_raw_type(testcase_dic, post_data):
        raw_data = json.loads(post_data)
        testcase_dic["request"]["data"] = raw_data
        testcase_dic["request"]["headers"].update({"Content-Type": "application/json"})

    @staticmethod
    def parse_urlencoded_type(testcase_dic, post_data):
        urlencoded_data = {}
        for param in post_data:
            data_key = param.get("key")
            data_value = param.get("value")
            urlencoded_data.update({data_key: data_value})
        testcase_dic["request"]["headers"].update({"Content-Type": "application/x-www-form-urlencoded"})
        testcase_dic["request"]["data"] = urlencoded_data

    @staticmethod
    def parse_formdata_type(testcase_dic, post_data):
        formdata = {}
        file_path = "请填写上传文件的绝对路径"
        file_type = "请填写上传文件的文件类型(如：text/html)"
        variables = testcase_dic["variables"] = []
        for param in post_data:
            data_key = param.get("key")
            data_type = param.get("type")
            data_value = param.get("value")
            if data_type == "file":
                data_value = [file_path, file_type]
            formdata.update({data_key: data_value})
        variables.append({"formdata": formdata})
        variables.append({"multipart_encoder": "${formdata_encoder($formdata)}"})
        testcase_dic["request"]["headers"].update({"Content-Type": "${multipart_content_type($multipart_encoder)}"})
        testcase_dic["request"]["data"] = "$multipart_encoder"

    @staticmethod
    def parse_file_type(testcase_dic, post_data):
        file_path = "请填写上传文件的绝对路径"
        file_type = "请填写上传文件的文件类型(如：text/html)"
        variables = testcase_dic["variables"] = []
        variables.append({"field_name": "file"})
        variables.append({"file_path": file_path})
        variables.append({"file_type": file_type})
        variables.append({"multipart_encoder": "${multipart_encoder($field_name, $file_path, $file_type)}"})
        testcase_dic["request"]["headers"].update(
            {"Content-Type": "${multipart_content_type($multipart_encoder)}"})
        testcase_dic["request"]["data"] = "$multipart_encoder"


class ParseParameters(object):
    def __init__(self, definitions, parameters):
        self.definitions = definitions
        self.parameters = parameters
        self.path_param = []
        self.query_param = []
        self.header_param = []
        self.body_param = []
        self.formdata_param = []

    def parse_in_path(self, param):
        '''
        {
            "name": "audit_id",
            "in": "path",
            "description": "audit_id",
            "required": true,
            "type": "integer",
            "format": "int64"
          }
        :param param:
        :return:
        '''
        return param

    def parse_in_query(self, param):
        '''
        {
            "name": "page",
            "in": "query",
            "description": "当前页",
            "required": false,
            "type": "integer",
            "format": "int32",
            "x-example": 10
          }
        :param param:
        :return:
        '''
        return param

    def parse_in_header(self, param):
        '''
        {
            "name": "uid",
            "in": "header",
            "description": "会员ID",
            "required": false,
            "type": "string"
          }
        :param param:
        :return:
        '''
        return param

    def parse_in_body(self, param):
        '''
        1、
        {
            "in": "body",
            "name": "params",
            "description": "params",
            "required": true,
            "schema": {
              "$ref": "#/definitions/WechatAuthParams"
            }
          }
        2、
        {
            "in": "body",
            "name": "cookieUuid",
            "description": "cookieUuid",
            "required": false,
            "schema": {
              "type": "string"
            }
        3、
        {
              "name": "user",
              "in": "body",
              "description": "user to add to the system",
              "required": true,
              "schema": {
                "type": "array",
                "items": {
                  "type": "string"
                }
              }
        }
        :param param:
        :return:
        {
          "type": "object",
          "properties": {
            "money": {
              "type": "number",
              "example": 21.3,
              "description": "提现金额"
            },
            "quota": {
              "type": "boolean",
              "example": true,
              "description": "是否超过限额,True超过,False未超过"
            },
            "status": {
              "type": "string",
              "example": "TOAUDIT",
              "description": "审核状态（待审核TOAUDIT，审核通过THROUGH）"
        }
        '''

        # paramters列表中，可能会存在多个
        schema = param["schema"]
        if "$ref" in schema:
            ref = schema["$ref"]
            schema = ref.split('/')[-1]
            definitons = self.definitions
            body_format = definitons[schema]["properties"]
            body = {}
            for key, value in body_format.items():
                # ToDO: definitions中properties可以让开发配合设置default值
                body.update({key: value["default"]})
        else:
            # ToDO: Schema Object可以让开发配合设置default值
            body = schema["default"]

        return body

    def parse_in_formdata(self, param):
        '''
        {
          "name": "name",
          "in": "formData",
          "description": "Updated name of the pet",
          "required": false,
          "type": "string"
        }
        :param param:
        :return:
        '''
        # TODO: 还没有遇到有Formdata的情况
        key = param["name"]
        value = param["default"]
        return {key: value}

    def parse_parameters(self):
        type_parse = {
            "path": self.parse_in_path,
            "query": self.parse_in_query,
            "header": self.parse_in_header,
            "body": self.parse_in_body,
            "formData": self.parse_in_formdata,
        }
        data_append = {
            "path": self.path_param,
            "query": self.query_param,
            "header": self.header_param,
            "body": self.body_param,
            "formData": self.formdata_param,
        }
        for param in self.parameters:
            param_type = param["in"]
            param_required = param["required"]
            if param_required:
                parse_data = type_parse[param_type](param)
                data_append[param_type].append(parse_data)


class ParseDefinitons(object):
    def __init__(self, definitons):
        self.defintions = definitons
        self.data_schemas = {}

    def parse_definitons(self):
        pass






