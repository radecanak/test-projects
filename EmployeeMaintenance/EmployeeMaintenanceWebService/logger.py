'''
Logger class
'''
import logging
import sys
from logging.handlers import RotatingFileHandler

class Log(object):
    __logger = None
    __handler = None

    @classmethod
    def debug(cls, message):
        """
        Set debug type of message
        """
        cls.__set_message(logging.DEBUG, message)

    @classmethod
    def info(cls, message):
        """
        Set info type of message
        """
        cls.__set_message(logging.INFO, message)

    @classmethod
    def error(cls, message):
        """
        Set error type of message
        """
        cls.__set_message(logging.ERROR, message)
    
    @classmethod
    def warning(cls, message):
        """
        Set warning type of message
        """
        cls.__set_message(logging.WARNING, message)

    @classmethod
    def critical(cls, message):
        """
        Set critical type of message
        """
        cls.__set_message(logging.CRITICAL, message)

    @classmethod
    def exception(cls, message):
        """
        Set exception type of message
        """
        cls.__set_message(logging.ERROR, message, True)

    @classmethod
    def __set_message(cls, log_level, message, is_exception=False):
        if cls.__handler is None:
            cls.__handler = RotatingFileHandler("employee_maintenance_web_service.log", maxBytes=20000000,\
            backupCount=5)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            cls.__handler.setFormatter(formatter)
            cls.__handler.createLock()
        cls.__handler.acquire()
        cls.__logger = logging.getLogger()
        cls.__logger.setLevel(log_level)
        cls.__logger.addHandler(cls.__handler)
        if is_exception:
            cls.__logger.exception(message)
        elif log_level == logging.DEBUG:
            cls.__logger.debug(message)
        elif log_level == logging.INFO:
            cls.__logger.info(message)
        elif log_level == logging.ERROR:
            cls.__logger.error(message)
        elif log_level == logging.WARNING:
            cls.__logger.warning(message)
        elif log_level == logging.CRITICAL:
            cls.__logger.critical(message)
        cls.__logger.removeHandler(cls.__handler)
        cls.__handler.release()
        cls.__handler.close()


