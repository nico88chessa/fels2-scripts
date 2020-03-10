from gui.core.logger import Logger
from gui.core.singleton import Singleton
from threading import Lock
import socket
import json



IP_ADDRESS = "192.168.1.100"
DIAGNOSTIC_PORT = 8000
DATA_PORT = 8001
BUFFER_RECEIVE_SIZE = 1024

readRegisterMap = {
    "Request": "Registers read"
}

readControlMap = {
    "Request": "Control read"
}

readStatusMap = {
    "Request": "Status read"
}

readOutputMap = {
    "Request": "Output enable read"
}


class Fels2Controller(metaclass=Singleton):

    def __init__(self):
        self.__lock = Lock()
        self.__dataLock = Lock()
        self.__diagnosticSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__isConnected = False

    def connect(self, forceConnection = False) -> int:

        res = 0
        Logger().debug("Connect socket")
        if self.__isConnected and not forceConnection:
            Logger().info("FELS 2 gia' connessa")
            return 0

        with self.__lock:
            try:
                self.__diagnosticSocket.connect((IP_ADDRESS, DIAGNOSTIC_PORT))
            except OSError as msg:
                Logger().error("Errore connessione diagnostica: " + str(msg))
                self.__diagnosticSocket.close()
                res = 1

            try:
                self.__dataSocket.connect((IP_ADDRESS, DATA_PORT))
            except OSError as msg:
                Logger().error("Errore connessione dati: " + str(msg))
                self.__dataSocket.close()
                res = 2

        self.__isConnected = res==0
        return res

    def disconnect(self):
        with self.__lock:
            self.__dataSocket.close()
            self.__diagnosticSocket.close()

    def sendCommand(self, str):
        pass

    def readRegisters(self):
        registers = b""
        with self.__lock:
            Logger().info("Invio comando read registers")
            strCommand = json.dumps(readRegisterMap, indent=4)
            Logger().debug("Str: "+strCommand)
            len = self.__diagnosticSocket.sendall(strCommand.encode())
            Logger().debug("Ricevuto bytes: " + str(len))
            registers = self.__diagnosticSocket.recv(BUFFER_RECEIVE_SIZE)
            outputDataJson = json.loads(registers.decode())
            prettyOutput = json.dumps(outputDataJson, indent=4)

        return prettyOutput

    def readControl(self):
        controlData = b""
        with self.__lock:
            Logger().info("Invio comando read control")
            strCommand = json.dumps(readControlMap, indent=4)
            Logger().debug("Str: " + strCommand)
            len = self.__diagnosticSocket.sendall(strCommand.encode())
            Logger().debug("Ricevuto bytes: " + str(len))
            controlData = self.__diagnosticSocket.recv(BUFFER_RECEIVE_SIZE)
            outputDataJson = json.loads(controlData.decode())
            prettyOutput = json.dumps(outputDataJson, indent=4)

        return prettyOutput

    def readStatus(self):
        statusData = b""
        with self.__lock:
            Logger().info("Invio comando read status")
            strCommand = json.dumps(readStatusMap, indent=4)
            Logger().debug("Str: " + strCommand)
            len = self.__diagnosticSocket.sendall(strCommand.encode())
            Logger().debug("Ricevuto bytes: " + str(len))
            statusData = self.__diagnosticSocket.recv(BUFFER_RECEIVE_SIZE)
            outputDataJson = json.loads(statusData.decode())
            prettyOutput = json.dumps(outputDataJson, indent=4)

        return prettyOutput

    def readOutput(self):
        outputData = b""
        with self.__lock:
            Logger().info("Invio comando read output")
            strCommand = json.dumps(readOutputMap, indent=4)
            Logger().debug("Str: " + strCommand)
            len = self.__diagnosticSocket.sendall(strCommand.encode())
            Logger().debug("Ricevuto bytes: " + str(len))
            outputData = self.__diagnosticSocket.recv(BUFFER_RECEIVE_SIZE)
            outputDataJson = json.loads(outputData.decode())
            prettyOutput = json.dumps(outputDataJson, indent=4)

        return prettyOutput

    def sendRequest(self, request: str) -> str:
        outputData = b""
        with self.__lock:
            Logger().info("Invio request")
            Logger().debug("Str: " + request)
            data = json.loads(request)
            bytes2Send = json.dumps(data).encode()
            len = self.__diagnosticSocket.sendall(bytes2Send)
            Logger().debug("Ricevuto bytes: " + str(len))
            resultByte = self.__diagnosticSocket.recv(BUFFER_RECEIVE_SIZE)
            outputDataJson = json.loads(resultByte.decode())
            prettyOutput = json.dumps(outputDataJson, indent=4)

        return prettyOutput
