import requests
import logging
import sys
import json


def load_by_url(swagger_josn_url=None):
    '''
    :param swagger_josn_url: json swagger url地址
    :return: swagger dict 对象
    '''
    try:
        swagger_josn_url = swagger_josn_url or 'http://192.168.1.107:5000/swagger.json'
        content_json = requests.get(swagger_josn_url).json()
        return content_json
    except Exception:
        logging.error("swagger file content error: {}".format(swagger_josn_url))
        sys.exit(1)


def load_by_file(file_path):
    with open(file_path, "r", encoding="utf-8-sig") as f:
        try:
            content = json.loads(f.read())
            return content
        except (KeyError, TypeError):
            logging.error("swagger file content error: {}".format(file_path))
            sys.exit(1)