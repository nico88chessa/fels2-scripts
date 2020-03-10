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

        self._logger = logging.getLogger("logger")
        self._logger.addHandler(handler)
        self._logger.setLevel(logging.DEBUG)

    def debug(self, msg):
        self._logger.debug(msg)

    def info(self, msg):
        self._logger.info(msg)

    def warning(self, msg):
        self._logger.warning(msg)

    def error(self, msg):
        self._logger.error(msg)

    def critical(self, msg):
        self._logger.critical(msg)
