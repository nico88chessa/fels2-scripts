from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine, qmlRegisterType

from gui.core.logger import Logger
from gui.controller.corectrl import CoreController, CoreBean

import sys


if __name__ == "__main__":

    Logger().info("Avvio applicazione FELS2")

    app = QGuiApplication(sys.argv)

    app.setOrganizationName("DV")
    app.setApplicationName("FELS2-GUI")
    app.setApplicationVersion("0.0.1")

    qmlRegisterType(CoreController, "com.dv.CoreController", 1, 0, "CoreController")
    qmlRegisterType(CoreBean, "com.dv.CoreBean", 1, 0, "CoreBean")

    engine = QQmlApplicationEngine("./qml/main.qml")

    res = app.exec_()
    sys.exit(res)