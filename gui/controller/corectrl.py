import json

from PySide2.QtCore import QObject, Property, Signal, Slot, QThread, QMetaObject, QEventLoop
from gui.core.logger import Logger
from gui.controller.corebean import CoreBean
from gui.core.fels2controller import Fels2Controller
import gui.core.fels2controller as F2CTRL
from gui.core.fels2inspector import Fels2Inspector

FELS2_PERIOD_TIME = 5120


class CoreController(QObject):

    beanChanged = Signal()
    updateTransferConsole = Signal(str)

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
        self.__bean.encoderPulsesChanged.connect(self.updateUtilsValues)
        self.__bean.fileChunkSizeChanged.connect(self.updateUtilsValues)

    @Slot()
    def stopProcess(self):
        QMetaObject.invokeMethod(self.__fels2Inspector, "stopTimer")
        # trick EventLoop: in questo modo viene effettivamente eseguito il metodo stopTimer
        # senza questo trick, l'applicazione andrebbe in deadlock
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

    @Slot()
    def sendEncoderMap(self):

        Logger().info("Sending encoder map")
        encoderPath = self.__bean.getMapFilepath()
        Logger().info("Apertura file: "+encoderPath)
        try:
            with open(encoderPath, "rb") as f:
                encoderMap = f.read()
        except OSError as err:
            self.updateTransferConsole.emit("File: "+encoderPath+" non trovato")
            return


        Logger().info("Encoder map letta correttamente")

        f2Ctrl = Fels2Controller()
        if f2Ctrl.connect():
            # preparo la scheda a ricevere la mappa encoder
            request = F2CTRL.encoderMapTransferRequest
            strCommand = json.dumps(request, indent=4)
            self.updateTransferConsole.emit(request)
            requestResult = f2Ctrl.sendRequest(strCommand)
            self.updateTransferConsole.emit(requestResult)

            # invio la mappa encoder
            f2Ctrl.sendData(encoderMap)

            # verifico che mappa encoder e' settata nella scheda
            request = F2CTRL.readTransferRequest
            strCommand = json.dumps(request, indent=4)
            self.updateTransferConsole.emit(request)
            requestResult = f2Ctrl.sendRequest(strCommand)
            self.updateTransferConsole.emit(requestResult)

        else:
            self.updateTransferConsole.emit("Invio encoder map KO")

    @Slot()
    def sendModulationTableMap(self):
        Logger().info("Sending modulation table map")
        modulationTablePath = self.__bean.getModulationTableFilepath()
        Logger().info("Apertura file: " + modulationTablePath)
        try:
            with open(modulationTablePath, "rb") as f:
                modulationTable = f.read()
        except OSError as err:
            self.updateTransferConsole.emit("File: " + modulationTablePath + " non trovato")
            return

        Logger().info("Modulation table map letta correttamente")

        f2Ctrl = Fels2Controller()
        if f2Ctrl.connect():
            # preparo la scheda a ricevere la modulation table
            request = F2CTRL.modulationTableTransferRequest
            strCommand = json.dumps(request, indent=4)
            self.updateTransferConsole.emit(request)
            requestResult = f2Ctrl.sendRequest(strCommand)
            self.updateTransferConsole.emit(requestResult)

            # invio la modulation table
            f2Ctrl.sendData(modulationTable)

            # verifico che mappa encoder e' settata nella scheda
            request = F2CTRL.readTransferRequest
            strCommand = json.dumps(request, indent=4)
            self.updateTransferConsole.emit(request)
            requestResult = f2Ctrl.sendRequest(strCommand)
            self.updateTransferConsole.emit(requestResult)

        else:
            self.updateTransferConsole.emit("Invio modulation table map KO")

    @Slot()
    def sendImage(self):
        Logger().info("Sending image")
        imagePath = self.__bean.getImageFilepath()
        Logger().info("Apertura file: " + imagePath)
        try:
            with open(imagePath, "rb") as f:
                image = f.read()
        except OSError as err:
            self.updateTransferConsole.emit("File: " + imagePath + " non trovato")
            return

        Logger().info("Immagine letta correttamente")

        f2Ctrl = Fels2Controller()
        if f2Ctrl.connect():
            # preparo la scheda a ricevere l'immagine
            request = F2CTRL.imageTransferRequest
            strCommand = json.dumps(request, indent=4)
            self.updateTransferConsole.emit(request)
            requestResult = f2Ctrl.sendRequest(strCommand)
            self.updateTransferConsole.emit(requestResult)

            # invio dati immagine
            f2Ctrl.sendData(image)

            # verifico che l'immagine e' settata nella scheda
            request = F2CTRL.readTransferRequest
            strCommand = json.dumps(request, indent=4)
            self.updateTransferConsole.emit(request)
            requestResult = f2Ctrl.sendRequest(strCommand)
            self.updateTransferConsole.emit(requestResult)

        else:
            self.updateTransferConsole.emit("Invio image KO")

    @Slot()
    def updateUtilsValues(self):
        encoderPulses = int(self.__bean.getEncoderPulses())
        fileChunk = int(self.__bean.getFileChunkSize())
        self.__bean.setPeriodTestTime(FELS2_PERIOD_TIME)
        self.__bean.setNumPeriodChannel(encoderPulses/4)
        self.__bean.setRotationTestTime(encoderPulses/4*FELS2_PERIOD_TIME)
        self.__bean.setDDRBlockSize(fileChunk*1024**2/4)

    pBean = Property(CoreBean, getBean, setBean, notify=beanChanged)
