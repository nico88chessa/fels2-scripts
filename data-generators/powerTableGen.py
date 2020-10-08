import os
from array import array


FELS2_CLOCK_INTERVAL_NS = 10
FELS2_MAX_NUM_LASERS = 64
GS8_SIZE = 2**8
GS16_SIZE = 2**16
GS8_MAX_VALUE = GS8_SIZE - 1
GS16_MAX_VALUE = GS16_SIZE - 1


if __name__ == "__main__":

    currentPath = os.path.dirname(os.path.abspath(__file__))
    print("Cc:"+str(currentPath))
    destPath = currentPath + "/./output/"
    print("Cc:" + str(destPath))

    print("Creazione tabella potenza\n\n"
          "1. 1B\n"
          "2. GS8\n"
          "3. GS16")

    choice = int(input("Scelta: "))

    if choice == 1:
        # powerTable1b : array #("H", (0,)*FELS2_MAX_NUM_LASERS*2)

        laserNum = int(input("Numero laser (da 1 a 8): "))
        powerTable1b8Laser = array("H", (0,0,)*8)

        for i in range(laserNum):
            tonLaser = round(float(input("Selezionare Ton laser " + str(i) + " [us]: ")) * 1000)
            tonLaserTicks = int(tonLaser / FELS2_CLOCK_INTERVAL_NS)
            toffLaser = round(float(input("Selezionare Toff laser "+ str(i) + " [us]: "))*1000)
            toffLaserTicks = int(toffLaser / FELS2_CLOCK_INTERVAL_NS)

            powerTable1b8Laser[2*i:2*(i+1)] = array("H", [toffLaserTicks, tonLaserTicks])
        powerTable1b = array("H", powerTable1b8Laser * 8)

        filename = "powerTable1b.pot"
        destFullpath = destPath+filename
        print("Scrittura mappa in: " + destFullpath)
        with open(destFullpath, "wb") as fp:
            fp.write(powerTable1b.tobytes())
            print("OK")


        # tonLaser1Ns = round(float(input("Selezionare Ton laser 1 [us]: "))*1000)
        # tonLaser1Ticks = int(tonLaser1Ns / FELS2_CLOCK_INTERVAL_NS)
        #
        # if laserNum == 1:
        #     powerTable1b = array("H", (0,) * FELS2_MAX_NUM_LASERS * 2)
        #     powerTable1b[1] = tonLaser1Ticks
        #     filename = "powerTable1b.pot"
        #     destFullpath = destPath+filename
        #     print("Scrittura mappa in: " + destFullpath)
        #     with open(destFullpath, "wb") as fp:
        #         fp.write(powerTable1b.tobytes())
        #         print("OK")
        # else:
        #     tonLaser2Ns = round(float(input("Selezionare Ton laser 2 [us]: "))*1000)
        #     tonLaser2Ticks = int(tonLaser2Ns / FELS2_CLOCK_INTERVAL_NS)
        #     powerTable1b = array("H", (0, tonLaser1Ticks, 0, tonLaser2Ticks)*int(FELS2_MAX_NUM_LASERS/2))
        #     filename = "powerTable1b.pot"
        #     destFullpath = destPath + filename
        #     print("Scrittura mappa in: "+destFullpath)
        #     with open(destFullpath, "wb") as fp:
        #         fp.write(powerTable1b.tobytes())
        #         print("OK")

    elif choice == 2:
        tonMaxNs = round(float(input("Selezionare Ton massimo (valore "+str(GS8_MAX_VALUE)+") [us]: "))*1000)
        tonMaxNsTicks = int(tonMaxNs / FELS2_CLOCK_INTERVAL_NS)
        powerTableGS8 = array("H", (0,) * GS8_SIZE)
        step = tonMaxNsTicks / GS8_MAX_VALUE
        for i in range(GS8_SIZE):
            powerTableGS8[i] = round(step * i)

        filename = "powerTableGS8.pot"
        destFullpath = destPath + filename
        print("Scrittura mappa in: " + destFullpath)
        with open(destFullpath, "wb") as fp:
            fp.write(powerTableGS8.tobytes())
            print("OK")

    elif choice == 3:
        tonMaxNs = round(float(input("Selezionare Ton massimo (valore "+str(GS16_MAX_VALUE)+") [us]: "))*1000)
        tonMaxNsTicks = int(tonMaxNs / FELS2_CLOCK_INTERVAL_NS)
        powerTableGS16 = array("H", (0,) * GS16_SIZE)
        step = tonMaxNsTicks / GS16_MAX_VALUE

        for i in range(GS16_SIZE):
            powerTableGS16[i] = round(step * i)

        filename = "powerTableGS16.pot"
        destFullpath = destPath + filename
        print("Scrittura mappa in: " + destFullpath)
        with open(destFullpath, "wb") as fp:
            fp.write(powerTableGS16.tobytes())
            print("OK")

    exit(0)
