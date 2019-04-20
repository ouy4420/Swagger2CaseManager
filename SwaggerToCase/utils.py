import requests

try:
    from json.decoder import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError


def load_item(file_path=None):
    # with open(file_path, "r", encoding="utf-8-sig") as f:
    #     try:
    #         content_json = json.loads(f.read())
    #         return content_json
    #     except (KeyError, TypeError):
    #         logging.error("swagger file content error: {}".format(file_path))
    #         sys.exit(1)
    url_json = 'http://192.168.1.107:5000/swagger.json'  # json swagger url地址
    content_json = requests.get(url_json).json()
    return content_json

