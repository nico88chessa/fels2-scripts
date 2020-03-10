from PySide2.QtCore import QObject, Property, Signal

import json


registersWriteRequestSample = {
    "Request": "Registers write",
    "Total columns to be printed": 500,
    "Number of periods channel TEST": 200,
    "Depack scheme": 1,
    "Accelleration turns to be ignored": 10,
    "Encoder resolution": 5000,
    "Ignore pulses for offset y": 30,
    "Delay VES signal": 0,
    "Ton VES signal": 0,
    "Enable virtual encoder pulses": True,
    "Enable VES pulse": False,
    "Enable ZMV signal": False,
    "ZMV table 0": 0,
    "ZMV table 1": 0,
    "ZMV table 2": 0,
    "ZMV table 3": 0,
    "ZMV table 4": 0,
    "ZMV table 5": 0,
    "ZMV table 7": 0,
    "ZMV table 6": 0,
    "ZMV Ton": 0,
    "Enable quadrature counting": True,
    "Quadrature count direction": True,
    "Index ch A config": 1,
    "Index ch B config": 1,
    "Index ch 0 config": 1,
    "Image DDR block dimension": 64,
    "Encoder map": 1,
    "Multishot delay": 20
}

controlWriteRequestSample = {
    "Request": "Control write",
    "Modulator mode": "Grayscale 8 bit",
    "Start": True ,
    "Update register": True,
    "Resume from pause": False,
    "Pause": False,
    "Test internal encoder": False,
    "Enable irq PWM-MAX": False,
    "Enable irq PWM-NOT-FINISHED": False,
    "N laser manual": 5,
    "Manual": True,
    "Multishot": True,
    "N shot": 5
}

outputWriteRequestSample = {
    "Request": "Output enable",
    "Laser output enable 1": "0xFFFFFFFF",
    "Laser output enable 2": "0xFFFFFFFF",
}

class CoreBean(QObject):

    registersWriteRequestChanged = Signal()
    registersWriteResponseChanged = Signal()
    registersReadResponseChanged = Signal()
    controlWriteRequestChanged = Signal()
    controlWriteResponseChanged = Signal()
    controlReadResponseChanged = Signal()
    outputWriteRequestChanged = Signal()
    outputWriteResponseChanged = Signal()
    outputReadResponseChanged = Signal()
    statusResponseChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # registers
        self._registersWriteRequest = json.dumps(registersWriteRequestSample, indent=4)
        self._registersWriteResponse = ""
        self._registersReadResponse = ""

        # control
        self._controlWriteRequest = json.dumps(controlWriteRequestSample, indent=4)
        self._controlWriteResponse = ""
        self._controlReadResponse = ""

        # output
        self._outputWriteRequest = json.dumps(outputWriteRequestSample, indent=4)
        self._outputWriteResponse = ""
        self._outputReadResponse = ""

        # status
        self._statusResponse = ""

    def getRegistersWriteRequest(self):
        return self._registersWriteRequest
    def setRegistersWriteRequest(self, data):
        self._registersWriteRequest = data
        self.registersWriteRequestChanged.emit()

    def getRegistersWriteResponse(self):
        return self._registersWriteResponse
    def setRegistersWriteResponse(self, data):
        self._registersWriteResponse = data
        self.registersWriteResponseChanged.emit()

    def getRegistersReadResponse(self):
        return self._registersReadResponse
    def setRegistersReadResponse(self, data):
        self._registersReadResponse = data
        self.registersReadResponseChanged.emit()

    def getControlWriteRequest(self):
        return self._controlWriteRequest
    def setControlWriteRequest(self, data):
        self._controlWriteRequest = data
        self.controlWriteRequestChanged.emit()

    def getControlWriteResponse(self):
        return self._controlWriteResponse
    def setControlWriteResponse(self, data):
        self._controlWriteResponse = data
        self.controlWriteResponseChanged.emit()

    def getControlReadResponse(self):
        return self._controlReadResponse
    def setControlReadResponse(self, data):
        self._controlReadResponse = data
        self.controlReadResponseChanged.emit()

    def getOutputWriteRequest(self):
        return self._outputWriteRequest
    def setOutputWriteRequest(self, data):
        self._outputWriteRequest = data
        self.outputWriteRequestChanged.emit()

    def getOutputWriteResponse(self):
        return self._outputWriteResponse
    def setOutputWriteResponse(self, data):
        self._outputWriteResponse = data
        self.outputWriteResponseChanged.emit()

    def getOutputReadResponse(self):
        return self._outputReadResponse
    def setOutputReadResponse(self, data):
        self._outputReadResponse = data
        self.outputReadResponseChanged.emit()

    def getStatusResponse(self):
        return self._statusResponse
    def setStatusResponse(self, data):
        self._statusResponse = data
        self.statusResponseChanged.emit()

    pRegistersWriteRequest = Property(str, getRegistersWriteRequest, setRegistersWriteRequest, notify=registersWriteRequestChanged)
    pRegistersWriteResponse = Property(str, getRegistersWriteResponse, setRegistersWriteResponse, notify=registersWriteResponseChanged)
    pRegistersReadResponse = Property(str, getRegistersReadResponse, setRegistersReadResponse, notify=registersReadResponseChanged)
    pControlWriteRequest = Property(str, getControlWriteRequest, setControlWriteRequest, notify=controlWriteRequestChanged)
    pControlWriteResponse = Property(str, getControlWriteResponse, setControlWriteResponse, notify=controlWriteResponseChanged)
    pControlReadResponse = Property(str, getControlReadResponse, setControlReadResponse, notify=controlReadResponseChanged)
    pOutputWriteRequest = Property(str, getOutputWriteRequest, setOutputWriteRequest, notify=outputWriteRequestChanged)
    pOutputWriteResponse = Property(str, getOutputWriteResponse, setOutputWriteResponse, notify=outputWriteResponseChanged)
    pOutputReadResponse = Property(str, getOutputReadResponse, setOutputReadResponse, notify=outputReadResponseChanged)
    pStatusResponse = Property(str, getStatusResponse, setStatusResponse, notify=statusResponseChanged)
