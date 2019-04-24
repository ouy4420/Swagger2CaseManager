from httprunner import HttpRunner, report
import os
from datetime import datetime
from httprunner import logger
from jinja2 import Template
from httprunner.report import stringify_data


class MyHttpRunner(HttpRunner):
    def gen_html_report(self, **kwargs):
        return self.render_html_report(**kwargs)

    def render_html_report(self, **kwargs):
        summary = self.summary
        html_report_name = kwargs.get("report_name", None)
        dir_name = kwargs.get("dir_name", None)
        html_report_template = kwargs.get("html_report_template", None)
        if not html_report_template:
            html_report_template = os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                "templates",
                "report_template.html"
            )
            logger.log_debug("No html report template specified, use default.")
        else:
            logger.log_info("render with html report template: {}".format(html_report_template))

        logger.log_info("Start to render Html report ...")
        logger.log_debug("render data: {}".format(summary))

        report_dir_path = os.path.join(os.getcwd(), "reports")
        report_dir_path = os.path.join(report_dir_path, dir_name)
        if not os.path.isdir(report_dir_path):
            os.makedirs(report_dir_path)

        start_at_timestamp = int(summary["time"]["start_at"])
        start_at_datetime = datetime.fromtimestamp(start_at_timestamp).strftime('%Y_%m_%d_%H_%M_%S')
        summary["time"]["start_datetime"] = start_at_datetime

        if html_report_name:
            summary["html_report_name"] = html_report_name
            report_dir_path = os.path.join(report_dir_path, html_report_name)
            html_report_name += "-{}.html".format(start_at_datetime)
        else:
            summary["html_report_name"] = ""
            html_report_name = "{}.html".format(start_at_datetime)

        if not os.path.isdir(report_dir_path):
            os.makedirs(report_dir_path)

        for index, suite_summary in enumerate(summary["details"]):
            if not suite_summary.get("name"):
                suite_summary["name"] = "test suite {}".format(index)
            for record in suite_summary.get("records"):
                meta_data = record['meta_data']
                stringify_data(meta_data, 'request')
                stringify_data(meta_data, 'response')

        with open(html_report_template, "r", encoding='utf-8') as fp_r:
            template_content = fp_r.read()
            report_path = os.path.join(report_dir_path, html_report_name)

            with open(report_path, 'w', encoding='utf-8') as fp_w:
                rendered_content = Template(
                    template_content,
                    extensions=["jinja2.ext.loopcontrols"]
                ).render(summary)
                fp_w.write(rendered_content)

        logger.log_info("Generated Html report: {}".format(report_path))

        return report_path


runner = MyHttpRunner()


def run(testcases_dir, testcases):
    # 获取testcases完整路径
    project = 'TestProject'
    # 获取指定要执行的测试用例集
    # 执行测试用例
    testcases_dir = os.path.join(testcases_dir, 'testcases')
    for case in testcases:
        yml_json = os.path.join(testcases_dir, case)
        if os.path.isfile(yml_json) or os.path.isdir(yml_json):
            runner.run(yml_json)
            if "\\" in case:
                sub_dir, case = case.rsplit("\\", 1)
                dir_name = project + "\\" + sub_dir
            else:
                dir_name = project
            runner.gen_html_report(
                report_name=case.rsplit(".", 1)[0],
                dir_name=dir_name,
                html_report_template="report_template.html"
            )
