import logging
from logging import handlers
import os


class LogHandler(object):
    def __init__(self, name, level="INFO"):
        self.name = name
        self.level = level
        self.LEVELS = {
            "NOSET": logging.NOTSET,
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }

    def logger_basic(self):
        logger = logging.getLogger(self.name)
        # 设置输出的等级

        # 创建文件目录
        logs_dir = f"{os.path.dirname(__file__)}/../log"
        if not os.path.exists(logs_dir) or not os.path.isdir(logs_dir):
            os.mkdir(logs_dir)
        # 修改log保存位置
        # timestamp = time.strftime("%Y-%m-%d", time.localtime())
        filename = f"{self.name}.log"
        filepath = os.path.join(logs_dir, filename)
        rotatingFileHandler = logging.handlers.TimedRotatingFileHandler(  # type: ignore
            filename=filepath, when="D", interval=7, backupCount=2, encoding="utf-8"
        )  # 按照时间进行切割.

        # 设置输出格式
        formatter = logging.Formatter(
            "%(asctime)s -%(filename)s -%(levelname)s[line:%(lineno)d]: -%(message)s",
            "%Y-%m-%d %H:%M:%S %p",
        )
        rotatingFileHandler.setFormatter(formatter)
        # 加这一行if判断最为重要，如果不加的话，会重复打印日志
        if not logger.handlers:
            self._extracted_from_logger(formatter, logger, rotatingFileHandler)
        return logger

    # TODO Rename this here and in `logger_basic`
    def _extracted_from_logger(self, formatter, logger, rotatingFileHandler):
        # 控制台句柄
        console = logging.StreamHandler()
        console.setLevel(logging.NOTSET)
        console.setFormatter(formatter)
        # 添加内容到日志句柄中
        logger.addHandler(rotatingFileHandler)
        logger.addHandler(console)
        logger.setLevel(self.LEVELS[self.level])
