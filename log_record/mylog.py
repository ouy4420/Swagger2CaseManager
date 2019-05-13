import logging


# log日志信息配置
def log_config(filename, logger_name, level=logging.ERROR):
    mylogger = logging.getLogger(logger_name)
    mylogger.setLevel(level)  # 设定总的消息显示等级
    # 输出到屏幕
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)  # 设定“输出到屏幕”这部分的消息显示等级
    # 输出到文件
    fh = logging.FileHandler("{}.log".format(filename))
    fh.setLevel(level)  # 设定“输出到文件”这部分的消息显示等级
    # 设置日志格式
    fomatter = logging.Formatter('%(asctime)s -%(name)s-%(levelname)s-%(module)s:%(message)s')
    ch.setFormatter(fomatter)
    fh.setFormatter(fomatter)
    mylogger.addHandler(ch)
    mylogger.addHandler(fh)


if __name__ == '__main__':
    # logger名
    logger_name = 'Swagger2Case'
    # 导入logger
    log_config("swagger_log_record", logger_name)
