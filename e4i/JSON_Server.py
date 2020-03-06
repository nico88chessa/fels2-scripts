#import sys
#import logging

import socketserver
import socket
import threading
import time

import json
import devmem_pkg

import mmap
import os
import math
from threading import Thread
import devmem




address_encoder_map1 = 0x1C000000
address_encoder_map2 = 0x1C100000
address_encoder_map3 = 0x1C200000
address_mod_tab = 0x1D000000
address_reg_img1 = 0x1E000000
address_reg_img2 = 0x29000000
address_reg_img3 = 0x34000000


registers_dict = {
       "Number of periods channel TEST": 0,
       "Depack scheme": 0,
       "Total columns to be printed": 1,
       "Accelleration turns to be ignored": 0,
       "Encoder resolution": 0,
       "Ignore pulses for offset y": 0,
       "Delay VES signal": 0,
       "Ton VES signal": 0,
       "Enable VES pulse": False,
       "Enable ZMV signal": False,
       "ZMV table 0": 0,
       "ZMV table 1": 0,
       "ZMV table 2": 0,
       "ZMV table 3": 0,
       "ZMV table 4": 0,
       "ZMV table 5": 0,
       "ZMV table 6": 0,
       "ZMV table 7": 0,
       "ZMV Ton": 0,
       "Index ch A config": 1,
       "Index ch B config": 1,
       "Index ch 0 config": 1,
       "Image DDR block dimension" : 0,
       "Encoder map": 1,
       "Multishot delay": 0
    }

status_dict = {
    "Print finished": False,
    "Print paused": False,
    "Fifo empty": False,
    "Printed columns": 0,
    "Total turns": 0,
    "FPGA Revision date": "01 01 2019",
    "PWM-MAX": False,
    "PWM-NOT-FINISHED": False,
    "Quadrature decoder error": False,
    "Image region ready": False
    }

output_dict = {
    "Laser output enable 1": "0x00000000",
    "Laser output enable 2": "0x00000000",
}

control_dict = {
    "Modulator mode": "Grayscale 8 bit",
    "Start": False,
    "Resume from pause": False,
    "Update register": True,
    "Pause": False,
    "Test internal encoder": False,
    "Enable irq PWM-MAX": True,
    "Enable irq PWM-NOT-FINISHED": True,
    "N laser manual": 1,
    "Manual": False,
    "Multishot": False,
    "N shot": 0
}

region_dict = {
    "Region":"Encoder map1",
    "Image": 1
}

region_wrote = True

class RequestHandler(socketserver.BaseRequestHandler):

    def print_registers(self):
        mem = devmem.DevMem(0x40000000,44)
        print("*** PRINT REGISTERS ***")
        print(mem.read(0x0, 44).hexdump(4))


    def handle_Registers_write(self,dict):
        mem = devmem.DevMem(0x40000000,44)
        mem.debug_set(False)
        a = mem.read(0xAC,1)[0x0]; #WALKAROUND
        if "Number of periods channel TEST" in dict:
            if (dict["Number of periods channel TEST"] != registers_dict["Number of periods channel TEST"]):
                registers_dict["Number of periods channel TEST"] = dict["Number of periods channel TEST"]
        mem.write(0x18,[registers_dict["Number of periods channel TEST"]])
        if "Depack scheme" in dict:
            if (dict["Depack scheme"] != registers_dict["Depack scheme"]):
                registers_dict["Depack scheme"] = dict["Depack scheme"]
        mem.write(0x1C,[registers_dict["Depack scheme"]])
        if "Total columns to be printed" in dict:
            if (dict["Total columns to be printed"] != registers_dict["Total columns to be printed"]):
                registers_dict["Total columns to be printed"] = dict["Total columns to be printed"]
        a = mem.read(0xAC,1)[0x0]; #WALKAROUND
        mem.write(0x24,[registers_dict["Total columns to be printed"]])
        if "Accelleration turns to be ignored" in dict:
            if (dict["Accelleration turns to be ignored"] != registers_dict["Accelleration turns to be ignored"]):
                registers_dict["Accelleration turns to be ignored"] = dict["Accelleration turns to be ignored"]
        mem.write(0x28,[registers_dict["Accelleration turns to be ignored"]])
        if "Encoder resolution" in dict:
            if (dict["Encoder resolution"] != registers_dict["Encoder resolution"]):
                registers_dict["Encoder resolution"] = dict["Encoder resolution"]
        mem.write(0x2C,[registers_dict["Encoder resolution"]])
        if "Ignore pulses for offset y" in dict:
            if (dict["Ignore pulses for offset y"] != registers_dict["Ignore pulses for offset y"]):
                registers_dict["Ignore pulses for offset y"] = dict["Ignore pulses for offset y"]
        mem.write(0x30,[registers_dict["Ignore pulses for offset y"]])
        if "Delay VES signal" in dict:
            if (dict["Delay VES signal"] != registers_dict["Delay VES signal"]):
                registers_dict["Delay VES signal"] = dict["Delay VES signal"]
        mem.write(0x34,[registers_dict["Delay VES signal"]])
        if "Ton VES signal" in dict:
            if (dict["Ton VES signal"] != registers_dict["Ton VES signal"]):
                registers_dict["Ton VES signal"] = dict["Ton VES signal"]
        mem.write(0x38,[registers_dict["Ton VES signal"]])
        if "Enable VES pulse" in dict:
            if (dict["Enable VES pulse"] != registers_dict["Enable VES pulse"]):
                registers_dict["Enable VES pulse"] = dict["Enable VES pulse"]
        if "Enable ZMV signal" in dict:
            if (dict["Enable ZMV signal"] != registers_dict["Enable ZMV signal"]):
                registers_dict["Enable ZMV signal"] = dict["Enable ZMV signal"]
        reg=1;
        if registers_dict["Enable VES pulse"]:
            reg=reg+2;
        if registers_dict["Enable ZMV signal"]:
            reg=reg+4;
        mem.write(0x3C,[reg])
        if "ZMV table 0" in dict:
            if (dict["ZMV table 0"] != registers_dict["ZMV table 0"]):
                registers_dict["ZMV table 0"] = dict["ZMV table 0"]
        mem.write(0x40,[registers_dict["ZMV table 0"]])
        if "ZMV table 1" in dict:
            if (dict["ZMV table 1"] != registers_dict["ZMV table 1"]):
                registers_dict["ZMV table 1"] = dict["ZMV table 1"]
        mem.write(0x44,[registers_dict["ZMV table 1"]])
        if "ZMV table 2" in dict:
            if (dict["ZMV table 2"] != registers_dict["ZMV table 2"]):
                registers_dict["ZMV table 2"] = dict["ZMV table 2"]
        mem.write(0x48,[registers_dict["ZMV table 2"]])
        if "ZMV table 3" in dict:
            if (dict["ZMV table 3"] != registers_dict["ZMV table 3"]):
                registers_dict["ZMV table 3"] = dict["ZMV table 3"]
        mem.write(0x4C,[registers_dict["ZMV table 3"]])
        if "ZMV table 4" in dict:
            if (dict["ZMV table 4"] != registers_dict["ZMV table 4"]):
                registers_dict["ZMV table 4"] = dict["ZMV table 4"]
        mem.write(0x50,[registers_dict["ZMV table 4"]])
        if "ZMV table 5" in dict:
            if (dict["ZMV table 5"] != registers_dict["ZMV table 5"]):
                registers_dict["ZMV table 5"] = dict["ZMV table 5"]
        mem.write(0x54,[registers_dict["ZMV table 5"]])
        if "ZMV table 6" in dict:
            if (dict["ZMV table 6"] != registers_dict["ZMV table 6"]):
                registers_dict["ZMV table 6"] = dict["ZMV table 6"]
        mem.write(0x58,[registers_dict["ZMV table 6"]])
        if "ZMV table 7" in dict:
            if (dict["ZMV table 7"] != registers_dict["ZMV table 7"]):
                registers_dict["ZMV table 7"] = dict["ZMV table 7"]
        mem.write(0x5C,[registers_dict["ZMV table 7"]])
        if "ZMV Ton" in dict:
            if (dict["ZMV Ton"] != registers_dict["ZMV Ton"]):
                registers_dict["ZMV Ton"] = dict["ZMV Ton"]
        mem.write(0x60,[registers_dict["ZMV Ton"]])
        if "Index ch A config" in dict:
            if (dict["Index ch A config"] != registers_dict["Index ch A config"]):
                registers_dict["Index ch A config"] = dict["Index ch A config"]
        if "Index ch B config" in dict:
            if (dict["Index ch B config"] != registers_dict["Index ch B config"]):
                registers_dict["Index ch B config"] = dict["Index ch B config"]
        if "Index ch 0 config" in dict:
            if (dict["Index ch 0 config"] != registers_dict["Index ch 0 config"]):
                registers_dict["Index ch 0 config"] = dict["Index ch 0 config"]
        reg = 0x11CD
        if registers_dict["Index ch A config"]:
            reg=reg+0x200;
        if registers_dict["Index ch B config"]:
            reg=reg+0x400;
        if registers_dict["Index ch 0 config"]:
            reg=reg+0x800;
        mem.write(0x64,[reg])
        if "Image DDR block dimension" in dict:
            if (dict["Image DDR block dimension"] != registers_dict["Image DDR block dimension"]):
                registers_dict["Image DDR block dimension"] = dict["Image DDR block dimension"]
        a = mem.read(0xAC,1)[0x0]; #WALKAROUND
        mem.write(0x80,[registers_dict["Image DDR block dimension"]])
        if "Encoder map" in dict:
            if (dict["Encoder map"] != registers_dict["Encoder map"]):
                registers_dict["Encoder map"] = dict["Encoder map"]
        if registers_dict["Encoder map"] == 1:
            mem.write(0x84,[address_encoder_map1])
        elif registers_dict["Encoder map"] == 2:
            mem.write(0x84,[address_encoder_map2])
            #devmem_pkg.mmap_write_word(0x40000084, address_encoder_map2)
        elif registers_dict["Encoder map"] == 3:
            mem.write(0x84,[address_encoder_map3])
        if "Multishot delay" in dict:
            if (dict["Multishot delay"] != registers_dict["Multishot delay"]):
                registers_dict["Multishot delay"] = dict["Multishot delay"]
        mem.write(0x88,[registers_dict["Multishot delay"]])
        #registri impostati dalla PS
        #read_addr 0xA8
        a = mem.read(0xAC,1)[0x0]; #WALKAROUND
        mem.write(0xA8,[address_mod_tab])
        #control_irq_reg 0x0C
        a = mem.read(0xAC,1)[0x0]; #WALKAROUND
        mem.write(0x0C,[0x1E])
        #tot_dim_enc_reg 0x70
        a = mem.read(0xAC,1)[0x0]; #WALKAROUND
        dim_enc_map = math.ceil(registers_dict["Encoder resolution"]/32)
        mem.write(0x70,[dim_enc_map])
        #addr_ddr_image1_reg 0x74
        mem.write(0x74,[address_reg_img1])
        #addr_ddr_image2_reg 0x78
        mem.write(0x78,[address_reg_img2])
        #addr_ddr_image3_reg 0x7C
        mem.write(0x7C,[address_reg_img3])
        #read_addr 0xA8
        print("*** PRINT REGISTERS ***")
        print(mem.read(0x0, 44).hexdump(4))
        return {"Response code": 0}

    def handle_Registers_read(self,dict):
        dall = {"Response code": 0}
        dall.update(registers_dict)
        return dall

    def handle_Control_write(self,dict):
        mem = devmem.DevMem(0x40000000,44)
        reg = 0
        a = mem.read(0xAC,1)[0x0]; #WALKAROUND
        if "Modulator mode" in dict:
            if (dict["Modulator mode"] != control_dict["Modulator mode"]):
                control_dict["Modulator mode"] = dict["Modulator mode"]
        if control_dict["Modulator mode"] == "Grayscale 8 bit":
            reg = reg + 0x100000
            #size 0xAC
            mem.write(0xAC,[128])
        elif control_dict["Modulator mode"] == "Grayscale 16 bit":
            reg = reg + 0x200000
            #size 0xAC
            mem.write(0xAC,[32768])
        elif control_dict["Modulator mode"] == "Bitmap":
            reg = reg + 0
            #size 0xAC
            mem.write(0xAC,[64])
        else:
            control_dict["Modulator mode"] = "Grayscale 8 bit"
            return {"Response code": 1}
        if "Start" in dict:
            control_dict["Start"] = dict["Start"]
            if dict["Start"] == True:
                reg = reg + 1
                status_dict["Print finished"] = False
                status_dict["Print paused"] = False
        if "Update register" in dict:
            control_dict["Update register"] = dict["Update register"]
            if dict["Update register"] == True:
                reg = reg + 0x80000000
                print("update reg")
        if "Pause" in dict:
            control_dict["Pause"] = dict["Pause"]
            if dict["Pause"] == True:
                reg = reg + 0x4
        if "Test internal encoder" in dict:
            control_dict["Test internal encoder"] = dict["Test internal encoder"]
        if control_dict["Test internal encoder"] == True:
            reg = reg + 0x20
        if "Enable irq PWM-MAX" in dict:
            control_dict["Enable irq PWM-MAX"] = dict["Enable irq PWM-MAX"]
        if control_dict["Enable irq PWM-MAX"] == True:
            reg = reg + 0x400
        if "Enable irq PWM-NOT-FINISHED" in dict:
            control_dict["Enable irq PWM-NOT-FINISHED"] = dict["Enable irq PWM-NOT-FINISHED"]
        if control_dict["Enable irq PWM-NOT-FINISHED"] == True:
            reg = reg + 0x800
        if "N laser manual" in dict:
            control_dict["N laser manual"] = dict["N laser manual"]
        reg = reg + control_dict["N laser manual"] * 0x1000
        if "Manual" in dict:
            control_dict["Manual"] = dict["Manual"]
        if control_dict["Manual"] == True:
            reg = reg + 0x400000
        if "Multishot" in dict:
            control_dict["Multishot"] = dict["Multishot"]
        if control_dict["Multishot"] == True:
            reg = reg + 0x1000000
        if "N shot" in dict:
            control_dict["N shot"] = dict["N shot"]
        reg = reg + control_dict["N shot"] * 0x2000000
        a = mem.read(0xAC,1)[0x0]; #WALKAROUND
        print(hex(reg))
        mem.write(0x00,[reg])
        if "Resume from pause" in dict:
            control_dict["Resume from pause"] = dict["Resume from pause"]
            if dict["Resume from pause"] == True:
                status_dict["Print paused"] = False
                a = mem.read(0xAC,1)[0x0]; #WALKAROUND
                mem.write(0xA4,[(4+2048)])
                print("Here")
        return {"Response code": 0}

    def handle_Control_read(self,dict):
        dall = {"Response code": 0}
        dall.update(control_dict)
        return dall

    def handle_Output_enable(self,dict):
        mem = devmem.DevMem(0x40000000,44)
        if "Laser output enable 1" in dict:
            if (dict["Laser output enable 1"] != output_dict["Laser output enable 1"]):
                output_dict["Laser output enable 1"] = dict["Laser output enable 1"]
        a = mem.read(0xAC,1)[0x0]; #WALKAROUND
        mem.write(0x10,[int(output_dict["Laser output enable 1"],0)])
        a = mem.read(0xAC,1)[0x0]; #WALKAROUND
        mem.write(0x8C,[int(output_dict["Laser output enable 1"],0)])
        if "Laser output enable 2" in dict:
            if (dict["Laser output enable 2"] != output_dict["Laser output enable 2"]):
                output_dict["Laser output enable 2"] = dict["Laser output enable 2"]
        a = mem.read(0xAC,1)[0x0]; #WALKAROUND
        mem.write(0x14,[int(output_dict["Laser output enable 2"],0)])
        a = mem.read(0xAC,1)[0x0]; #WALKAROUND
        mem.write(0x90,[int(output_dict["Laser output enable 2"],0)])
        return {"Response code": 0}

    def handle_Data_write(self,dict):
        if "Region" in dict:
            if (dict["Region"] != region_dict["Region"]):
                region_dict["Region"] = dict["Region"]
        return {"Response code": 0}

    def handle_Output_enable_read(self,dict):
        dall = {"Response code": 0}
        dall.update(output_dict)
        return dall

    def handle_Data_read(self,dict):
        dall = {"Response code": 0}
        dall.update(region_dict)
        return dall

    def handle_Status_read(self,dict):
        mem = devmem.DevMem(0x40000000,44)
        a = mem.read(0x20,1)[0x0];
        status_dict["Printed columns"] = a;
        a = mem.read(0x6C,1)[0x0];
        status_dict["Total turns"] = a;
        a = mem.read(0x08,1)[0x0];
        status_dict["FPGA Revision date"] = a;
        dall = {"Response code": 0}
        dall.update(status_dict)
        return dall

    def handle(self):
        global shared_string
        data = self.request.recv(1024)
        data_string = data.decode("utf-8")
        data_dict = json.loads(data_string)
        if data_dict["Request"] != "Status read":
            print("serving JSON")
            print(data_dict)
        try:
            if data_dict["Request"] == "Registers write":
                response_dict = self.handle_Registers_write(data_dict)
            elif data_dict["Request"] == "Registers read":
                response_dict = self.handle_Registers_read(data_dict)
            elif data_dict["Request"] == "Output enable":
                response_dict = self.handle_Output_enable(data_dict)
            elif data_dict["Request"] == "Output enable read":
                response_dict = self.handle_Output_enable_read(data_dict)
            elif data_dict["Request"] == "Control write":
                response_dict = self.handle_Control_write(data_dict)
            elif data_dict["Request"] == "Control read":
                response_dict = self.handle_Control_read(data_dict)
            elif data_dict["Request"] == "Status read":
                response_dict = self.handle_Status_read(data_dict)
            elif data_dict["Request"] == "Data transfer":
                response_dict = self.handle_Data_write(data_dict)
            elif data_dict["Request"] == "Data transfer read":
                response_dict = self.handle_Data_read(data_dict)
            else:
                print("REQUEST NOT RECOGNIZED")
                response_dict = {"Response code" : 1}
        except:
            print("BAD REQUEST")
            response_dict = {"Response code" : 1}
        response = json.dumps(response_dict).encode()
        self.request.send(response)
        return

class RequestHandler1(socketserver.BaseRequestHandler):

    def handle(self):
        global region_wrote
        if region_dict["Region"] == "Image":
            if region_dict["Image"] == 1:
                addr = address_reg_img1
                region_dict["Image"] = 2
            elif region_dict["Image"] == 2:
                addr = address_reg_img2
                region_dict["Image"] = 3
            elif region_dict["Image"] == 3:
                addr = address_reg_img3
                region_dict["Image"] = 1
            status_dict["Image region ready"] = False
        elif region_dict["Region"] == "Encoder map1":
            addr = address_encoder_map1
        elif region_dict["Region"] == "Encoder map2":
            addr = address_encoder_map2
        elif region_dict["Region"] == "Encoder map3":
            addr = address_encoder_map3
        elif region_dict["Region"] == "Modulation table":
            addr = address_mod_tab
        total_byte = 0
        print("serving DATA")
        f = os.open("/dev/mem", os.O_RDWR | os.O_SYNC)
        base_addr = addr & ~(mmap.PAGESIZE - 1)
        offset = addr - base_addr
        size = 0xB000000
        mem = mmap.mmap(f, size, mmap.MAP_SHARED, mmap.PROT_READ | mmap.PROT_WRITE, offset=base_addr)
        mem.seek(offset)
        time_1 = time.time()
        while True:
            data = self.request.recv(131072)
            if (not data):
                mem.close()
                os.close(f)
                time_2 = time.time()
                dt1 = time_2 - time_1
                print ("time  :{0:.3f}".format(dt1*1000.0) + "[msec]")
                region_wrote = True
                break
            mem[total_byte:total_byte+len(data)]=data
            total_byte = total_byte + len(data)
        return

class IRQThread (Thread):
    def __init__(self):
        Thread.__init__(self)
    def run(self):
        global region_wrote
        mem1 = devmem.DevMem(0x40000000,44)
        time_2 = time.time()
        while True:
            print ("Waiting IRQ")
            devmem_pkg.wait_irq('/dev/uio0')
            time_1 = time.time()
            print ("time to arrive irq  :{0:.3f}".format((time_1-time_2)*1000.0) + "[msec]")
            sts = mem1.read(0x04,1)[0x0]
            feed = sts & 4
            if (feed != 0):
                if region_wrote == True:
                    a = mem1.read(0xAC,1)[0x0] #WALKAROUND
                    mem1.write(0xA4,[(2+512)])
                    status_dict["Image region ready"] = True
                    region_wrote = False
                else:
                    print("region wrote was false")
            paused = sts & 16
            if (paused != 0):
                status_dict["Print paused"] = True
            finished = sts & 8
            if (finished != 0):
                status_dict["Print finished"] = True
                a = mem1.read(0xAC,1)[0x0] #WALKAROUND
                mem1.write(0xA4,[(1024)])
            time_2 = time.time()
            print(sts)
            print ("time to serve irq  :{0:.3f}".format((time_2-time_1)*1000.0) + "[msec]")

if __name__ == "__main__":
    address = ('', 8000)  # let the kernel assign a port
    server = socketserver.TCPServer(address, RequestHandler)
    ip, port = server.server_address  # what port was assigned?
    print(ip,port)

    t = threading.Thread(target=server.serve_forever)
    t.setDaemon(True)  # don't hang on exit
    t.start()

    address1 = ('', 8001)  # let the kernel assign a port
    server1 = socketserver.TCPServer(address1, RequestHandler1)
    ip1, port1 = server1.server_address  # what port was assigned?
    print(ip1,port1)

    t1 = threading.Thread(target=server1.serve_forever)
    t1.setDaemon(True)  # don't hang on exit
    t1.start()

    t2 = IRQThread()
    t2.setDaemon(True)  # don't hang on exit
    t2.start()

    quit = ''
    while quit != 'q':
	    quit = input('q to quit: ')


    print("Service stopped")
    # Clean up
    server.shutdown()
    server.socket.close()
    server1.shutdown()
    server1.socket.close()
