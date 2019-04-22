from httprunner import HttpRunner, report
import os
from datetime import datetime
from httprunner import logger
from jinja2 import Template


class MyHttpRunner(HttpRunner):
    def gen_html_report(self, **kwargs):
        return self.render_html_report(**kwargs)

    def render_html_report(self, **kwargs):
        """ render html report with specified report name and template
            if html_report_name is not specified, use current datetime
            if html_report_template is not specified, use default report template
        """
        # 获取所需参数 -------------------------------------------------------------------------------------------------
        summary = self.summary
        report_name = kwargs.get("report_name", None)
        file_name = kwargs.get("file_name", None)
        dir_name = kwargs.get("dir_name", None)
        html_report_template = kwargs.get("html_report_template", None)

        # 选择模板------------------------------------------------------------------------------------------------------
        if not html_report_template:
            html_report_template = os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                "templates",
                "default_report_template.html"
            )
            logger.log_debug("No html report template specified, use default.")
        else:
            logger.log_info("render with html report template: {}".format(html_report_template))

        logger.log_info("Start to render Html report ...")
        logger.log_debug("render data: {}".format(summary))

        # 在reports文件夹下建立dir_name文件夹，如果没有就创建 ----------------------------------------------------------
        report_dir_path = os.path.join(os.getcwd(), "reports")
        report_dir_path = os.path.join(report_dir_path, dir_name)
        if not os.path.isdir(report_dir_path):
            os.makedirs(report_dir_path)

        #  在dir_name文件夹下建立file_name报告 -------------------------------------------------------------------------
        start_at_timestamp = int(summary["time"]["start_at"])
        summary["time"]["start_datetime"] = datetime.fromtimestamp(start_at_timestamp).strftime('%Y-%m-%d %H_%M_%S')
        start_time = summary["time"]["start_datetime"]
        if file_name:
            summary["html_report_name"] = report_name
            file_name += "-{}.html".format(start_time)
        else:
            summary["html_report_name"] = ""
            file_name = "{}.html".format(start_time)

        # 准备报告的Details部分数据 ------------------------------------------------------------------------------------
        for index, suite_summary in enumerate(summary["details"]):
            if not suite_summary.get("name"):
                suite_summary["name"] = "test suite {}".format(index)
            for record in suite_summary.get("records"):
                meta_data = record['meta_data']
                report.stringify_data(meta_data, 'request')
                report.stringify_data(meta_data, 'response')

        # 模板渲染 -----------------------------------------------------------------------------------------------------
        print(os.getcwd())
        with open(html_report_template, "r", encoding='utf-8') as fp_r:
            template_content = fp_r.read()
            report_path = os.path.join(report_dir_path, file_name)  # 报告完整路径
            with open(report_path, 'w', encoding='utf-8') as fp_w:
                rendered_content = Template(template_content).render(summary)  # 模板渲染
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
                file_name=case,
                dir_name=dir_name,
                html_report_template="default_report_template.html"
            )

