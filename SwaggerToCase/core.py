from SwaggerToCase.loader import LoadSwagger
from SwaggerToCase.parser import ParseSwagger
from SwaggerToCase.maker import MakeAPI, MakeTestcase
from SwaggerToCase.dumper import DumpFile


class Swagger2Case(object):
    def __init__(self, config):
        self.config = config
        self.item = {}
        self.parsed_swagger = {}
        self.definitoins = {}
        self.apis = []
        self.testcases = []

    def execute(self):
        # 加载swagger文件
        self.load()
        # 解析文件数据
        self.parse()
        # 组装api合testcase数据
        self.make()
        # 将api和testcase写入文件
        self.dump()

    def load(self):
        file_or_url = self.config["file_or_url"]
        loader = LoadSwagger(file_or_url)
        self.item = loader.load_swagger()

    def parse(self):
        parsed_swagger = ParseSwagger(self.item)
        parsed_swagger.parse_swagger()
        self.parsed_swagger = parsed_swagger.swagger
        self.definitoins = self.parsed_swagger["definitions"]

    def make(self):
        interfaces = self.parsed_swagger["interfaces"]
        make_api = MakeAPI()
        make_api.make_testapis(self.apis, interfaces)
        make_case = MakeTestcase()
        make_case.make_testcases(self.apis, self.testcases, interfaces)

    def dump(self):
        dumper = DumpFile(self.config, self.apis, self.testcases)
        dumper.dump_api_file()  # 写入api文件
        dumper.dump_testcases_files()  # 写入testcase文件

