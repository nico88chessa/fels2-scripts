from PySide2.QtCore import QObject, Property, Signal, Slot, QTimer
from gui.core.fels2controller import Fels2Controller


FELS2_POLLING_TIME_MS = 1000


class Fels2Inspector(QObject):

    fels2Updated = Signal(str, str, str, str)
    processStarted = Signal()
    processStopped = Signal()

    def __init__(self, parent = None):
        super().__init__(parent)
        self.__timer = QTimer(self)
        self.__timer.setInterval(FELS2_POLLING_TIME_MS)
        self.__timer.timeout.connect(self.checkStatus)

    @Slot()
    def startTimer(self):
        self.__timer.start()
        self.processStarted.emit()

    @Slot()
    def stopTimer(self):
        print("TIMER STOPPATO")
        self.__timer.stop()
        self.processStopped.emit()

    @Slot()
    def checkStatus(self):
        f2Ctrl = Fels2Controller()
        if f2Ctrl.connect():
            register = f2Ctrl.readRegisters()
            control = f2Ctrl.readControl()
            output = f2Ctrl.readOutput()
            status = f2Ctrl.readStatus()

            self.fels2Updated.emit(register, control, output, status)
        else:
            socketProblem = "Errore connessione socket"
            self.fels2Updated.emit(socketProblem, socketProblem, socketProblem, socketProblem)