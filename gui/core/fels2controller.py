from gui.core.logger import Logger
from gui.core.singleton import Singleton
from threading import Lock
import socket
import json


IP_ADDRESS = "192.168.1.100"
DIAGNOSTIC_PORT = 8000
DATA_PORT = 8001
BUFFER_RECEIVE_SIZE = 1024
SOCKET_TIMEOUT_SEC = 1

readRegisterMap = {
    "Request": "Registers read"
}

readControlMap = {
    "Request": "Control read",
}

readStatusMap = {
    "Request": "Status read"
}

readOutputMap = {
    "Request": "Output enable read"
}

encoderMapTransferRequest = {
    "Request": "Data transfer",
    "Region": "Encoder map1"
}

imageTransferRequest = {
    "Request": "Data transfer",
    "Region": "Image"
}

modulationTableTransferRequest = {
    "Request": "Data transfer",
    "Region": "Modulation table"
}

readTransferRequest = {
    "Request": "Data transfer read"
}


class Fels2Controller(metaclass=Singleton):

    def __init__(self):
        self.__lock = Lock()
        self.__dataLock = Lock()
        self.__diagnosticSocket : socket.socket
        self.__dataSocket : socket.socket
        self.__isConnected = False

    def connect(self, forceConnection = False) -> bool:

        res = 0
        Logger().debug("Connect socket")
        if self.__isConnected and not forceConnection:
            Logger().info("FELS 2 gia' connessa")
            return True

        with self.__lock:
            try:
                Logger().info("Creazione diagnostic socket")
                self.__diagnosticSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.__diagnosticSocket.settimeout(SOCKET_TIMEOUT_SEC)
                self.__diagnosticSocket.connect((IP_ADDRESS, DIAGNOSTIC_PORT))
            except OSError as msg:
                Logger().error("Errore connessione diagnostica: " + str(msg))
                self.__diagnosticSocket.close()
                res = 1

            try:
                Logger().info("Creazione data socket")
                self.__dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.__dataSocket.settimeout(SOCKET_TIMEOUT_SEC)
                self.__dataSocket.connect((IP_ADDRESS, DATA_PORT))
            except OSError as msg:
                Logger().error("Errore connessione dati: " + str(msg))
                self.__dataSocket.close()
                res = 2

        self.__isConnected = res==0
        return self.__isConnected

    def disconnect(self):
        with self.__lock:
            self.__disconnectInternal()

    def __disconnectInternal(self):
            Logger().info("Richiesta disconnessione")
            if self.__diagnosticSocket != None:
                self.__diagnosticSocket.close()
                Logger().info("Disconnessione diagnostic socket OK")
            if self.__dataSocket != None:
                self.__dataSocket.close()
                Logger().info("Disconnessione data socket OK")
            self.__isConnected = False
            Logger().info("Disconnessione completata")

    def sendCommand(self, str):
        pass

    def readRegisters(self):
        registers = b""
        with self.__lock:
            Logger().info("Invio comando read registers")
            strCommand = json.dumps(readRegisterMap, indent=4)
            Logger().debug("Str: "+strCommand)
            try:
                len = self.__diagnosticSocket.sendall(strCommand.encode())
                Logger().debug("Ricevuto bytes: " + str(len))
                registers = self.__diagnosticSocket.recv(BUFFER_RECEIVE_SIZE)
            except OSError as msg:
                Logger().error("Errore read registers")
                Logger().error("Err: " + str(msg))
                self.__disconnectInternal()
                return "Errore read registers"
            outputDataJson = json.loads(registers.decode())
            prettyOutput = json.dumps(outputDataJson, indent=4, sort_keys=True)

        return prettyOutput

    def readControl(self):
        controlData = b""
        with self.__lock:
            Logger().info("Invio comando read control")
            strCommand = json.dumps(readControlMap, indent=4)
            Logger().debug("Str: " + strCommand)
            try:
                len = self.__diagnosticSocket.sendall(strCommand.encode())
                Logger().debug("Ricevuto bytes: " + str(len))
                controlData = self.__diagnosticSocket.recv(BUFFER_RECEIVE_SIZE)
            except OSError as msg:
                Logger().error("Errore read control")
                Logger().error("Err: " + str(msg))
                self.__disconnectInternal()
                return "Errore read control"
            outputDataJson = json.loads(controlData.decode())
            prettyOutput = json.dumps(outputDataJson, indent=4, sort_keys=True)

        return prettyOutput

    def readStatus(self):
        statusData = b""
        with self.__lock:
            Logger().info("Invio comando read status")
            strCommand = json.dumps(readStatusMap, indent=4)
            Logger().debug("Str: " + strCommand)
            try:
                len = self.__diagnosticSocket.sendall(strCommand.encode())
                Logger().debug("Ricevuto bytes: " + str(len))
                statusData = self.__diagnosticSocket.recv(BUFFER_RECEIVE_SIZE)
            except OSError as msg:
                Logger().error("Errore read status")
                Logger().error("Err: " + str(msg))
                self.__disconnectInternal()
                return "Errore read status"
            outputDataJson = json.loads(statusData.decode())
            prettyOutput = json.dumps(outputDataJson, indent=4, sort_keys=True)

        return prettyOutput

    def readOutput(self):
        outputData = b""
        with self.__lock:
            Logger().info("Invio comando read output")
            strCommand = json.dumps(readOutputMap, indent=4)
            Logger().debug("Str: " + strCommand)
            try:
                len = self.__diagnosticSocket.sendall(strCommand.encode())
                Logger().debug("Ricevuto bytes: " + str(len))
                outputData = self.__diagnosticSocket.recv(BUFFER_RECEIVE_SIZE)
            except OSError as msg:
                Logger().error("Errore read output")
                Logger().error("Err: " + str(msg))
                self.__disconnectInternal()
                return "Errore read output"
            outputDataJson = json.loads(outputData.decode())
            prettyOutput = json.dumps(outputDataJson, indent=4, sort_keys=True)

        return prettyOutput

    def sendRequest(self, request: str) -> str:
        outputData = b""
        with self.__lock:
            Logger().info("Invio request")
            Logger().debug("Str: " + request)
            data = json.loads(request)
            bytes2Send = json.dumps(data).encode()
            try:
                len = self.__diagnosticSocket.sendall(bytes2Send)
                Logger().debug("Ricevuto bytes: " + str(len))
                resultByte = self.__diagnosticSocket.recv(BUFFER_RECEIVE_SIZE)
            except OSError as msg:
                Logger().error("Errore invio request")
                Logger().error("Err: " + str(msg))
                self.__disconnectInternal()
                return "Errore request"

            outputDataJson = json.loads(resultByte.decode())
            prettyOutput = json.dumps(outputDataJson, indent=4, sort_keys=True)

        return prettyOutput

    def sendData(self, data):

        Logger().info("Invio dati")
        with self.__dataLock:
            res = self.__dataSocket.sendall(data)

        Logger().info("Dati inviati")