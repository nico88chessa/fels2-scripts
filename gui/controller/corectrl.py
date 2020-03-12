from PySide2.QtCore import QObject, Property, Signal, Slot, QThread, QMetaObject, QEventLoop
from gui.core.logger import Logger
from gui.controller.corebean import CoreBean
from gui.core.fels2controller import Fels2Controller
from gui.core.fels2inspector import Fels2Inspector


class CoreController(QObject):

    beanChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__bean = None
        self.__fels2Watcher: QThread = None
        self.__fels2Inspector: Fels2Inspector = None
        self.startWatcher()

    def getBean(self):
        return self.ppval

    def setBean(self, d):
        self.__bean = d
        self.beanChanged.emit()

    @Slot()
    def stopProcess(self):
        QMetaObject.invokeMethod(self.__fels2Inspector, "stopTimer")
        # trick EventLoop: in questo modo viene effettivamente eseguito il metodo stopTimer
        # senza questo trick, l'applicazione andrebbe in stallo
        # invokeMethod viene eseguito infatti non appena l'applicazione ritorna nell'eventLoop
        # pero' se ci metto la wait, l'applicazione non VA MAI nell'eventloop perche' aspetta
        # che il thread si chiuda (ma non si chiude mai perche' lo stopTimer non viene mai chiamato)
        if self.__fels2Watcher != None:
            loop = QEventLoop()
            self.__fels2Watcher.finished.connect(loop.quit)
            loop.exec_()
            self.__fels2Watcher.wait()

    @Slot()
    def startWatcher(self):
        Logger().info("Avvio thread watcher")
        self.__fels2Watcher = QThread()
        self.__fels2Watcher.setObjectName("Fels2Inspector")
        self.__fels2Inspector = Fels2Inspector()

        self.__fels2Inspector.moveToThread(self.__fels2Watcher)

        self.__fels2Watcher.started.connect(self.__fels2Inspector.startTimer)
        self.__fels2Inspector.processStopped.connect(self.__fels2Watcher.quit)
        self.__fels2Watcher.finished.connect(self.__fels2Inspector.deleteLater)
        self.__fels2Watcher.finished.connect(self.__fels2Watcher.deleteLater)

        self.__fels2Inspector.fels2Updated.connect(lambda r,c,o,s: (
            self.__bean.setRegistersReadResponse(r),
            self.__bean.setControlReadResponse(c),
            self.__bean.setOutputReadResponse(o),
            self.__bean.setStatusResponse(s))
        )

        self.__fels2Watcher.start()
        Logger().info("Thread watcher avviato")

    @Slot()
    def writeRegisters(self):
        Logger().info("Write registers")
        f2Ctrl = Fels2Controller()
        if f2Ctrl.connect():
            request = self.__bean.getRegistersWriteRequest()
            Logger().debug("Request: "+request)
            res = f2Ctrl.sendRequest(request)
            self.__bean.setRegistersWriteResponse(res)
        else:
            self.__bean.setRegistersWriteResponse("Problema connessione socket")

    @Slot()
    def writeControl(self):
        f2Ctrl = Fels2Controller()
        if f2Ctrl.connect():
            request = self.__bean.getControlWriteRequest()
            Logger().debug("Request: " + request)
            res = f2Ctrl.sendRequest(request)
            self.__bean.setControlWriteResponse(res)
        else:
            self.__bean.setRegistersWriteResponse("Problema connessione socket")

    @Slot()
    def writeOutput(self):
        f2Ctrl = Fels2Controller()
        if f2Ctrl.connect():
            request = self.__bean.getOutputWriteRequest()
            Logger().debug("Request: " + request)
            res = f2Ctrl.sendRequest(request)
            self.__bean.setOutputWriteResponse(res)
        else:
            self.__bean.setRegistersWriteResponse("Problema connessione socket")

    pBean = Property(CoreBean, getBean, setBean, notify=beanChanged)
