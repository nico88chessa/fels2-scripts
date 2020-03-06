import mmap
import os
import struct


def mmap_read_word(addr):
    '''
    :param addr: integer
    :return:
    '''
    f = os.open("/dev/mem", os.O_RDWR | os.O_SYNC)
    base_addr = addr & ~(mmap.PAGESIZE - 1)
    offset = addr - base_addr
    mem = mmap.mmap(f, offset + 4, mmap.MAP_SHARED, mmap.PROT_READ | mmap.PROT_WRITE, offset=base_addr)
    mem.seek(offset)
    val = struct.unpack("I", mem.read(4))[0]
    mem.close()
    os.close(f)
    return val


def mmap_write_word(addr, val):
    '''

    :param addr: integer
    :param val: integer
    :return:
    '''
    #print("inside " + hex(addr))
    #print("inside " + hex(val))
    f = os.open("/dev/mem", os.O_RDWR | os.O_SYNC)
    base_addr = addr & ~(mmap.PAGESIZE - 1)
    offset = addr - base_addr
    mem = mmap.mmap(f, offset + 4, mmap.MAP_SHARED, mmap.PROT_READ | mmap.PROT_WRITE, offset=base_addr)
    mem.seek(offset)
    mem.write(struct.pack('I', val))
    mem.close()
    os.close(f)
    #print("finished " + hex(addr))


def mmap_write_list(addr, val_list):
    #f = os.open("/dev/mem", os.O_RDWR | os.O_SYNC)
    f = os.open("./prova.txt", os.O_RDWR | os.O_SYNC | os.O_CREAT)
    base_addr = addr & ~(mmap.PAGESIZE - 1)
    offset = addr - base_addr
    size = mmap.PAGESIZE - offset
    mem = mmap.mmap(f, size, mmap.MAP_SHARED, mmap.PROT_READ | mmap.PROT_WRITE, offset=base_addr)
    for i, val in enumerate(val_list):
        mem.seek(offset)
        mem.write(struct.pack('I', int(val[2:], 16)))
        offset += 4
        if (offset == mmap.PAGESIZE):
            mem.close()
            offset = 0
            base_addr += mmap.PAGESIZE
            mem = mmap.mmap(f, mmap.PAGESIZE, mmap.MAP_SHARED, mmap.PROT_READ | mmap.PROT_WRITE, offset=base_addr)
    mem.close()
    os.close(f)

def mmap_read_list(addr, length):
    val_list = []
    f = os.open("/dev/mem", os.O_RDWR | os.O_SYNC)
    base_addr = addr & ~(mmap.PAGESIZE - 1)
    offset = addr - base_addr
    size = mmap.PAGESIZE - offset
    mem = mmap.mmap(f, size, mmap.MAP_SHARED, mmap.PROT_READ | mmap.PROT_WRITE, offset=base_addr)
    for i in range(length):
        mem.seek(offset)
        val_list.append(struct.unpack("I", mem.read(4))[0])
        offset += 4
        if (offset == mmap.PAGESIZE):
            mem.close()
            offset = 0
            base_addr += mmap.PAGESIZE
            mem = mmap.mmap(f, mmap.PAGESIZE, mmap.MAP_SHARED, mmap.PROT_READ | mmap.PROT_WRITE, offset=base_addr)
    mem.close()
    os.close(f)
    return val_list

def wait_irq(device_name):
    #device_name = '/dev/uio0'
    device_file = os.open(device_name, os.O_RDWR | os.O_SYNC)
    os.write(device_file, bytes([1, 0, 0, 0])) #leggi sotto
    os.read(device_file, 4)
    #os.write(device_file, bytes([1, 0, 0, 0])) # lasciare commentato
    #os.write(device_file, chr(1) + chr(0) + chr(0) + chr(0))
    os.close(device_file)

    # note: irq is disabled once received.  you need to reenable it
    #   - before handling it, if edge-triggered
    #   - after handling it, if level-triggered
