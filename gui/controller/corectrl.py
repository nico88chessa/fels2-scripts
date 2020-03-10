from PySide2.QtCore import QObject, Property, Signal, Slot, QThread, Qt
from gui.core.logger import Logger
from gui.controller.corebean import CoreBean
from gui.core.fels2controller import Fels2Controller
from gui.core.fels2inspector import Fels2Inspector


class CoreController(QObject):

    @Signal
    def beanChanged(self): pass

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__bean = None
        self.__fels2Watcher : None
        self.__fels2Inspector : Fels2Inspector

    def getBean(self):
        return self.ppval

    def setBean(self, d):
        self.__bean = d
        self.beanChanged.emit()

    @Slot()
    def startWatcher(self):
        self.__fels2Watcher = QThread()
        self.__fels2Watcher.setObjectName("Fels2Inspector")
        self.__fels2Inspector = Fels2Inspector()

        self.__fels2Inspector.moveToThread(self.__fels2Watcher)
        self.__fels2Watcher.started.connect(self.__fels2Inspector.startTimer)
        self.__fels2Watcher.finished.connect(self.__fels2Inspector.stopTimer)
        self.__fels2Inspector.fels2Updated.connect(
            lambda r, c, o, s : (
                self.__bean.setRegistersReadResponse(s),
                self.__bean.setControlReadResponse(c),
                self.__bean.setOutputReadResponse(o),
                self.__bean.setStatusReadResponse(s)
            )
        )

        self.__fels2Watcher.start()

    @Slot()
    def fels2Update(self, r, c, o, s):
        self.__bean.setRegistersReadResponse(s)
        self.__bean.setControlReadResponse(c)
        self.__bean.setOutputReadResponse(o)
        self.__bean.setStatusReadResponse(s)

    @Slot()
    def writeRegisters(self):
        self.startWatcher()
        return
        f2Ctrl = Fels2Controller()
        f2Ctrl.connect()
        request = self.__bean.getRegistersWriteRequest()
        Logger().debug("Request: "+request)
        res = f2Ctrl.sendRequest(request)
        self.__bean.setRegistersWriteResponse(res)

    @Slot()
    def writeControl(self):
        f2Ctrl = Fels2Controller()
        f2Ctrl.connect()
        request = self.__bean.getControlWriteRequest()
        Logger().debug("Request: " + request)
        res = f2Ctrl.sendRequest(request)
        self.__bean.setControlWriteResponse(res)

    @Slot()
    def writeOutput(self):
        f2Ctrl = Fels2Controller()
        f2Ctrl.connect()
        request = self.__bean.getOutputWriteRequest()
        Logger().debug("Request: " + request)
        res = f2Ctrl.sendRequest(request)
        self.__bean.setOutputWriteResponse(res)

    pBean = Property(CoreBean, getBean, setBean, notify=beanChanged)
