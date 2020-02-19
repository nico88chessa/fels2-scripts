from bitarray import bitarray
import math

if __name__ == "__main__":

    pulsesEncoder = int (input("Numero impulsi encoder: "))

    # multiplo del byte, altrimenti bitarray
    # ha problemi nella conversione con endianess
    pulsesEncoderBytes = math.ceil(pulsesEncoder / 8)
    encoderMap = bitarray(pulsesEncoderBytes * 8)
    encoderMap.setall(False)

    print("Scegliere modalita' generazione mappa encoder\n"
          "1. impulsi virtuali equispaziati\n"
          "2. suddivisione lineare")

    choice = int(input("Scelta: "))

    if choice == 1:
        pulseDistance = int (input("Inserire spaziatura impulsi encoder virtuale: "))
        pulseDistance += 1
        for i in range(0, pulsesEncoder, pulseDistance):
            encoderMap[i] = True

    elif choice == 2:
        pulsesVirtualEncoder = int (input("Numero impulsi encoder virtuale: "))
        step = float(pulsesEncoder / pulsesVirtualEncoder)
        for i in range(pulsesVirtualEncoder):
            position = round(step * i)
            encoderMap[position] = True
    else:
        exit(0)

    print("Selezionare endianess:\n"
          "1. little\n"
          "2. big")

    endianess = int(input("Endianess: "))

    with open("./workfile.map", "wb") as f:
        if endianess == 1:
            encMapEndianess = bitarray(encoderMap, endian="little")
        elif endianess == 2:
            encMapEndianess = encoderMap

        f.write(encMapEndianess.tobytes())