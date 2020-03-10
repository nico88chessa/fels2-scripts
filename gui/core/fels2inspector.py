from PySide2.QtCore import QObject, Property, Signal, Slot, QTimer
from gui.core.fels2controller import Fels2Controller


FELS2_POLLING_TIME_MS = 1000


class Fels2Inspector(QObject):

    fels2Updated = Signal(str, str, str, str)

    def __init__(self, parent = None):
        super().__init__(parent)
        self.timer = QTimer(self)
        self.timer.setInterval(FELS2_POLLING_TIME_MS)
        self.timer.timeout.connect(self.checkStatus)

    @Slot()
    def startTimer(self):
        self.timer.start()

    @Slot()
    def stopTimer(self):
        self.timer.stop()

    @Slot()
    def checkStatus(self):
        f2Ctrl = Fels2Controller()
        f2Ctrl.connect()
        register = f2Ctrl.readRegisters()
        control = f2Ctrl.readControl()
        outupt = f2Ctrl.readOutput()
        status = f2Ctrl.readStatus()

        self.fels2Updated.emit(register, control, outupt, status)