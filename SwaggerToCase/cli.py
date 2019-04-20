import argparse
import logging
import os
import sys

from collection2case import __version__
from collection2case.core import PostmanParser


def main():
    """ Collection v2.1 converter: parse command line options and run commands.
    """
    parser = argparse.ArgumentParser(
        description='Convert collection v2.1 josn file to YAML/JSON testcases for HttpRunner.')
    parser.add_argument(
        '-V', '--version', dest='version', action='store_true',
        help="show version")
    parser.add_argument('har_source_file', nargs='?',
                        help="Specify collection v2.1 josn file source file")
    parser.add_argument('output_testset_file', nargs='?',
                        help="Optional. Specify converted YAML/JSON testset file.")
    parser.add_argument(
        '--filter', help="Specify filter keyword, only url include filter string will be converted.")
    parser.add_argument(
        '--exclude',
        help="Specify exclude keyword, url that includes exclude string will be ignored, multiple keywords can be joined with '|'")
    parser.add_argument(
        '--log-level', default='INFO',
        help="Specify logging level, default is INFO.")

    args = parser.parse_args()

    if args.version:
        print("{}".format(__version__))
        exit(0)

    log_level = getattr(logging, args.log_level.upper())
    logging.basicConfig(level=log_level)

    har_source_file = args.har_source_file
    output_testset_file = args.output_testset_file

    if not har_source_file or not har_source_file.endswith(".json"):
        logging.error("json file not specified.")
        sys.exit(1)

    output_file_type = "JSON"
    if not output_testset_file:
        harfile = os.path.splitext(har_source_file)[0]
        output_testset_file = "{}.{}".format(harfile, output_file_type.lower())
    else:
        output_file_suffix = os.path.splitext(output_testset_file)[1]
        if output_file_suffix in [".yml", ".yaml"]:
            output_file_type = "YAML"
        elif output_file_suffix in [".json"]:
            output_file_type = "JSON"
        else:
            logging.error("Converted file could only be in YAML or JSON format.")
            sys.exit(1)

    har_parser = PostmanParser(har_source_file)

    if output_file_type == "JSON":
        har_parser.gen_json(output_testset_file)
    else:
        har_parser.gen_yaml(output_testset_file)

    return 0


# def main1(args):
#     if args["version"]:
#         print("{}".format(__version__))
#         exit(0)
#
#     log_level = getattr(logging, args["log_level"].upper())
#     logging.basicConfig(level=log_level)
#     har_source_file = args["har_source_file"]
#     output_testset_file = args["output_testset_file"]
#
#     if not har_source_file or not har_source_file.endswith(".json"):
#         logging.error("json file not specified.")
#         sys.exit(1)
#
#     output_file_type = "JSON"
#     if not output_testset_file:
#         harfile = os.path.splitext(har_source_file)[0]
#         output_testset_file = "{}.{}".format(harfile, output_file_type.lower())
#     else:
#         temp = os.path.splitext(output_testset_file)
#         output_file_suffix = os.path.splitext(output_testset_file)[1]
#         if output_file_suffix in [".yml", ".yaml"]:
#             output_file_type = "YAML"
#         elif output_file_suffix in [".json"]:
#             output_file_type = "JSON"
#         else:
#             logging.error("Converted file could only be in YAML or JSON format.")
#             sys.exit(1)
#
#     har_parser = PostmanParser(har_source_file)
#
#     if output_file_type == "JSON":
#         har_parser.gen_json(output_testset_file)
#     else:
#         har_parser.gen_yaml(output_testset_file)
#
#     return 0
#
#
# if __name__ == "__main__":
#     args = {'exclude': None, 'filter': None,
#             'har_source_file': r'C:\Users\jlx\PycharmProjects\postman2case\postman_collection.json',
#             'log_level': 'DEBUG',
#             'output_testset_file': r'C:\Users\jlx\PycharmProjects\postman2case\temp\demo.yml', 'version': False}
#     main1(args)
