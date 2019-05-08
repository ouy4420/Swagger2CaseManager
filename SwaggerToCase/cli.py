import argparse
import logging
import os
from SwaggerToCase.run import gen_api_case
from SwaggerToCase.inherit import run
# from .run import gen_api_case
# from .inherit import run


def main():
    """ Collection v2.1 converter: parse command line options and run commands.
    """
    parser = argparse.ArgumentParser(description='Convert Swagger  file to YAML/JSON testcases for HttpRunner.')
    parser.add_argument("-v", "--version", help="show version")
    parser.add_argument('-path',
                        '--test_pro_path',
                        action="store_true",
                        default=r'C:\Users\Administrator\PycharmProjects\Swagger2Case\SwaggerToCase\TestProject',
                        help="测试工作目录")
    log_level = getattr(logging, 'debug'.upper())
    logging.basicConfig(level=log_level)
    parser.add_argument(
        '-l',
        '--log_level',
        help="Specify logging level, default is DEBUG.")
    #
    # cwd = os.getcwd()
    # # test_pro_path = os.path.join(cwd, 'TestProject')
    # parser.add_argument('test_pro_path',
    #                     default='',
    #                     help="测试工作目录")
    #
    # url_or_file = r'C:\Users\Administrator\PycharmProjects\Swagger2Case\json_files\aa.json'
    # # url_or_file = 'http://192.168.1.107:5000/swagger.json'
    parser.add_argument('-i',
                        '--url_or_file',
                        help="加载swagger文件的url或file")
    #
    # swagger_name = 'Mytest'
    parser.add_argument('-name',
                        '--swagger_name',
                        help="swagger name")
    #
    # file_type = "YAML"
    parser.add_argument('-f',
                        '--file_type',
                        help="json or yaml file type")
    #
    args = parser.parse_args()
    print(args)
    # if args.version:
    #     print("{}".format('1.0'))
    #     exit(0)
    #
    gen_api_case(args.test_pro_path, args.url_or_file, args.swagger_name, args.file_type)
    run(args.test_pro_path, [args.swagger_name])
    #
    # return 0


if __name__ == '__main__':
    main()
