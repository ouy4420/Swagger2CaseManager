import traceback
import os


class DebugCode(object):

    def __init__(self, code, file_path):
        self.__code = code
        self.resp = ""
        self.file_path = file_path

    def run(self):
        """ dumps driver_code.py and run
        """
        try:
            with open(self.file_path, 'w', encoding='utf-8') as stream:
                stream.write(self.__code)
            ret = os.popen("python {}".format(self.file_path))
            for line in ret.readlines():
                self.resp += line
        except Exception as e:
            self.resp = traceback.format_exc()


if __name__ == '__main__':
    path = r'C:\Users\Administrator\PycharmProjects\Swagger2Case\SwaggerToCase\TestProject\debugtalk.py'
    a = DebugCode("print(13)", path)
    a.run()
    print(a.resp)

