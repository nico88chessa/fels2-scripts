from bitarray import bitarray
from array import array
import struct
import math

SLOT_SIZE_BYTE = 4

if __name__ == "__main__":

    pulsesEncoder = int (input("Numero impulsi encoder: "))

    # multiplo del byte, altrimenti bitarray
    # ha problemi nella conversione con endianess
    pulsesEncoderBytes = math.ceil(pulsesEncoder / 8)
    pulsesEncoderInts = math.ceil(pulsesEncoder / (8*SLOT_SIZE_BYTE)) # long int in python e' 4 byte
    encoderMap = bitarray(pulsesEncoderBytes * 8)
    encoderMap.setall(False)
    encodeUIntMap = array("I", [0]*pulsesEncoderInts)

    print("single item size: "+str(encodeUIntMap.itemsize))

    print("Scegliere modalita' generazione mappa encoder\n"
          "1. impulsi virtuali equispaziati\n"
          "2. suddivisione lineare")

    choice = int(input("Scelta: "))

    countVirtualPulses = 0
    if choice == 1:
        pulseDistance = int (input("Inserire spaziatura impulsi encoder virtuale: "))
        pulseDistance += 1
        for i in range(0, pulsesEncoder, pulseDistance):
            encoderMap[i] = True
            intPos = int (i / (SLOT_SIZE_BYTE*8))
            bitOffset = int (i % (SLOT_SIZE_BYTE*8))
            encodeUIntMap[intPos] |= 0x01 << bitOffset
            countVirtualPulses += 1

    elif choice == 2:
        pulsesVirtualEncoder = int (input("Numero impulsi encoder virtuale: "))
        step = float(pulsesEncoder / pulsesVirtualEncoder)
        for i in range(pulsesVirtualEncoder):
            position = round(step * i)
            encoderMap[position] = True
            intPos = int(i / (SLOT_SIZE_BYTE*8))
            bitOffset = int(i % (SLOT_SIZE_BYTE*8))
            encodeUIntMap[intPos] |= 0x01 << bitOffset
            countVirtualPulses += 1
    else:
        exit(0)

    print("Numero impulsi encoder virtuale: "+str(countVirtualPulses))
    '''
    print("Selezionare endianess:\n"
          "1. little\n"
          "2. big\n"
          "3. 4byte-mode")

    outputMode = int(input("Endianess: "))

    with open("./workfile.map", "wb") as f:
        if outputMode == 1:
            encMapEndianess = bitarray(encoderMap, endian="little")
        elif outputMode == 2:
            encMapEndianess = encoderMap
        elif outputMode == 3:
            encMapEndianess = encodeUIntMap
    '''
    with open("./virtualEncoder.map", "wb") as f:
        encMapEndianess = encodeUIntMap
        f.write(encMapEndianess.tobytes())

    exit(0)