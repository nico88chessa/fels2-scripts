import logging
import os
from logging.handlers import RotatingFileHandler
from gui.core.singleton import Singleton


class Logger(metaclass=Singleton):

    def __init__(self):

        # folder = QStandardPaths.writableLocation(QStandardPaths.AppLocalDataLocation)
        # folder += "/" + Constants.LOG_FILE_PATH
        # folder += "/" + Settings().getLoggingPath().LOG_FILE_PATH

        logFolder = ""
        logFolder = os.getenv("HOME", "")
        logFolder += "/.var/fels-2/logs/"

        if not os.path.exists(logFolder):
            os.makedirs(logFolder)

        logFilename = "gui.log"

        logFolder += logFilename

        handler = RotatingFileHandler(filename=logFolder, maxBytes=0, backupCount=6, delay=True)
        formatter = logging.Formatter("${asctime} ${levelname} ${message}", style='$')
        handler.setFormatter(formatter)

        needRollover = os.path.exists(logFolder)
        if needRollover:
            handler.doRollover()

        self.__logger = logging.getLogger("logger")
        self.__logger.addHandler(handler)
        self.__logger.setLevel(logging.INFO)

    def debug(self, msg):
        self.__logger.debug(msg)

    def info(self, msg):
        self.__logger.info(msg)

    def warning(self, msg):
        self.__logger.warning(msg)

    def error(self, msg):
        self.__logger.error(msg)

    def critical(self, msg):
        self.__logger.critical(msg)
