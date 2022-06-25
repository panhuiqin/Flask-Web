# -*- coding: utf-8 -*-
from datetime import datetime
import logging
import time
import os
from sheen import ColoredHandler
# from project_utils import utils_io_folder


class LogFactory(object):

    def __init__(self, Logger=None):
        """
            指定保存日志的文件路径，日志级别，以及调用文件
            将日志存入到指定的文件中
        """
        global logPath, resultPath, proDir
        proDir = os.path.split(os.path.dirname(__file__))[0]
        resultPath = os.path.join(proDir, "result")
        # create result file if it doesn't exist
        if not os.path.exists(resultPath) :
            os.mkdir(resultPath)
        # defined test result file name by localtime
        logPath = os.path.join(resultPath, str(datetime.now().strftime("%Y%m%d")))
        # create test result file if it doesn't exist
        if not os.path.exists(logPath) :
            os.mkdir(logPath)
        # 创建一个logger
        self.logger = logging.getLogger(Logger)
        self.logger.addHandler(ColoredHandler())
        self.logger.setLevel(logging.DEBUG)
        # self.log_name = os.path.join(self.log_path, "{}-{}.log".format(phase, time.strftime("%Y_%m_%d_%H")))
        self.logger.addHandler(ColoredHandler())
        # create file handler which logs even debug messages
        print(logPath)
        file_handler = logging.FileHandler(os.path.join(logPath, "output.log"))
        file_handler.setLevel(logging.DEBUG)
        # create console handler with a higher log level
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        # # 再创建一个handler，用于输出到控制台
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def get_log(self):
        return self.logger



# def test():
#     global logger
#     logger = LogFactory(__name__).get_log()
#     for i in range(10):
#         logger.error("131464631313")
#
#
# test()
