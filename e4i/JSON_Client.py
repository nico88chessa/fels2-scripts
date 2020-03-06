
import sys
import logging

import socketserver
import socket
import threading
import time
import json

if __name__ == "__main__":
    ip, port = ('192.168.1.100', 8000)
    print(ip,port)

    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('client')
    logger.info('Server on %s:%s', ip, port)

    ################################################################
    # Connect to the server
    logger.debug('creating socket')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logger.debug('connecting to server')
    s.connect((ip, port))

    # Send the data
    message_dict = {
        "Request": "Registers write",
        "Number of periods channel TEST": 0,
        "Depack scheme": 0,        
        "Total columns to be printed": 160,
        "Accelleration turns to be ignored": 4,
        "Encoder resolution": 200,
        "Ignore pulses for offset y": 20,
        "Index ch A config": 1,
        "Index ch B config": 1,
        "Index ch 0 config": 1,
        "Image DDR block dimension" : 0x2000,
        "Encoder map": 1
    }

    message = json.dumps(message_dict).encode()
    logger.debug('sending data: "%s"', message)
    len_sent = s.send(message)

    # Receive a response
    logger.debug('waiting for response')
    response = s.recv(1024)
    logger.debug('response from server: "%s"', response)

    # Clean up
    logger.debug('closing socket')
    s.close()
    logger.debug('done')

    proceed = ''
    while proceed != 'p':
        proceed = input('p to proceed: ')

    ################################################################
    # Connect to the server
    #logger.debug('creating socket')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logger.debug('connecting to server')
    s.connect((ip, port))

    # Send the data
    message_dict = {
        "Request": "Data transfer",
        "Region": "Encoder map1"
    }

    message = json.dumps(message_dict).encode()
    logger.debug('sending data: "%s"', message)
    len_sent = s.send(message)

    # Receive a response
    logger.debug('waiting for response')
    response = s.recv(1024)
    logger.debug('response from server: "%s"', response)

    # Clean up
    logger.debug('closing socket')
    s.close()
    logger.debug('done')

    proceed = ''
    while proceed != 'p':
        proceed = input('p to proceed: ')

    ###############################################################
    ip1, port1 = ('192.168.1.100',8001)
    print(ip1,port1)

    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('client1')
    logger.info('Server on %s:%s', ip1, port1)

    ################################################################
    # Connect to the server
    logger.debug('creating socket')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logger.debug('connecting to server')
    s.connect((ip1, port1))

    # Send the data
    message =  b'\x55' * 28
    logger.debug('sending data: "%s"', message)
    len_sent = s.sendall(message)

    # Clean up
    logger.debug('closing socket')
    s.close()
    logger.debug('done')

    proceed = ''
    while proceed != 'p':
        proceed = input('p to proceed: ')

    ################################################################
    # Connect to the server
    logger.debug('creating socket')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logger.debug('connecting to server')
    s.connect((ip, port))

    # Send the data
    message_dict = {
        "Request": "Data transfer",
        "Region": "Modulation table"
    }

    message = json.dumps(message_dict).encode()
    logger.debug('sending data: "%s"', message)
    len_sent = s.send(message)

    # Receive a response
    logger.debug('waiting for response')
    response = s.recv(1024)
    logger.debug('response from server: "%s"', response)

    # Clean up
    logger.debug('closing socket')
    s.close()
    logger.debug('done')

    proceed = ''
    while proceed != 'p':
        proceed = input('p to proceed: ')

    ################################################################
    # Connect to the server
    logger.debug('creating socket')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logger.debug('connecting to server')
    s.connect((ip1, port1))

    # Send the data
    message =  b'\x00\x00\x01\x00' * 64
    logger.debug('sending data: "%s"', message)
    len_sent = s.sendall(message)

    # Clean up
    logger.debug('closing socket')
    s.close()
    logger.debug('done')

    proceed = ''
    while proceed != 'p':
        proceed = input('p to proceed: ')

    ###############################################################
    # Connect to the server
    logger.debug('creating socket')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logger.debug('connecting to server')
    s.connect((ip, port))

    # Send the data
    message_dict = {
        "Request": "Data transfer",
        "Region": "Image"
    }

    message = json.dumps(message_dict).encode()
    logger.debug('sending data: "%s"', message)
    len_sent = s.send(message)

    # Receive a response
    logger.debug('waiting for response')
    response = s.recv(1024)
    logger.debug('response from server: "%s"', response)

    # Clean up
    logger.debug('closing socket')
    s.close()
    logger.debug('done')

    proceed = ''
    while proceed != 'p':
        proceed = input('p to proceed: ')

    ################################################################
    # Connect to the server
    logger.debug('creating socket')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logger.debug('connecting to server')
    s.connect((ip1, port1))

    # Send the data
    message =  b'\xFF' * 8192
    logger.debug('sending data: "%s"', message)
    len_sent = s.sendall(message)

    # Clean up
    logger.debug('closing socket')
    s.close()
    logger.debug('done')

    proceed = ''
    while proceed != 'p':
        proceed = input('p to proceed: ')

    ################################################################
    # Connect to the server
    logger.debug('creating socket')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logger.debug('connecting to server')
    s.connect((ip, port))

    # Send the data
    message_dict = {
        "Request": "Output enable",
        "Laser output enable 1": "0x00000001",
        "Laser output enable 2": "0x00000000"
    }

    message = json.dumps(message_dict).encode()
    logger.debug('sending data: "%s"', message)
    len_sent = s.send(message)

    # Receive a response
    logger.debug('waiting for response')
    response = s.recv(1024)
    logger.debug('response from server: "%s"', response)

    # Clean up
    logger.debug('closing socket')
    s.close()
    logger.debug('done')

    proceed = ''
    while proceed != 'p':
        proceed = input('p to proceed: ')

    ###############################################################
    # Connect to the server
    logger.debug('creating socket')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logger.debug('connecting to server')
    s.connect((ip, port))

    # Send the data
    message_dict = {
        "Request": "Control write",
        "Modulator_mode": "Bitmap",
        "Start": True,
        "Update register": True,
        "Pause": False,
        "Test internal encoder": True,
        "Enable irq PWM-MAX": False,
        "Enable irq PWM-NOT-FINISHED": False,
        "N laser manual": 1,
        "Manual": False,
        "Multishot": False,
        "N shot": 0
    }

    message = json.dumps(message_dict).encode()
    logger.debug('sending data: "%s"', message)
    len_sent = s.send(message)

    # Receive a response
    logger.debug('waiting for response')
    response = s.recv(1024)
    logger.debug('response from server: "%s"', response)

    # Clean up
    logger.debug('closing socket')
    s.close()
    logger.debug('done')

    iteration = 0
    while False:#True:
        time_1 = time.time()
        iteration += 1
        if iteration == 20:
            break
        print("Iteration : " + str(iteration))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))

        # Send the data
        message_dict = {
            "Request": "Status read"
        }

        message = json.dumps(message_dict).encode()
        #logger.debug('sending data: "%s"', message)
        len_sent = s.send(message)

        # Receive a response
        #logger.debug('waiting for response')
        response = s.recv(1024)
        #logger.debug('response from server: "%s"', response)

        # Clean up
        #logger.debug('closing socket')
        s.close()
        #logger.debug('done')

        data_string = response.decode("utf-8")
        data_dict = json.loads(data_string)

        if data_dict["Print finished"] == True:
            break

        if data_dict["Print paused"] == True:
            break

        if data_dict["Image region ready"] == True:
            iteration = 0
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip1, port1))

            # Send the data
            message =  b'\xFF' * 8192
            #logger.debug('sending data: "%s"', message)
            len_sent = s.sendall(message)

            # Clean up
            #logger.debug('closing socket')
            s.close()
            #logger.debug('done')
            print ("Image wrote")

        time_2 = time.time()
        print ("time  :{0:.3f}".format((time_2-time_1)*1000.0) + "[msec]")


    proceed = ''
    while proceed != 'p':
        proceed = input('p to proceed: ')
