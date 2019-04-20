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
