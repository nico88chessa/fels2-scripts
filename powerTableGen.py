from array import array

FELS2_CLOCK_INTERVAL_NS = 10
FELS2_MAX_NUM_LASERS = 64
GS8_SIZE = 2**8
GS16_SIZE = 2**16
GS8_MAX_VALUE = GS8_SIZE - 1
GS16_MAX_VALUE = GS16_SIZE - 1


if __name__ == "__main__":

    print("Creazione tabella potenza\n\n"
          "1. 1B\n"
          "2. GS8\n"
          "3. GS16")

    choice = int(input("Scelta: "))

    if choice == 1:
        powerTable1b : array #("H", (0,)*FELS2_MAX_NUM_LASERS*2)

        laserNum = int(input("Numero laser (1/2): "))
        tonLaser1Ns = round(float(input("Selezionare Ton laser 1 [us]: "))*1000)
        tonLaser1Ticks = int(tonLaser1Ns / FELS2_CLOCK_INTERVAL_NS)

        if laserNum == 1:
            powerTable1b = array("H", (0,) * FELS2_MAX_NUM_LASERS * 2)
            powerTable1b[1] = tonLaser1Ticks
        else:
            tonLaser2Ns = round(float(input("Selezionare Ton laser 2 [us]: "))*1000)
            tonLaser2Ticks = int(tonLaser2Ns / FELS2_CLOCK_INTERVAL_NS)
            powerTable1b = array("H", (0, tonLaser1Ticks, 0, tonLaser2Ticks)*int(FELS2_MAX_NUM_LASERS/2))

        with open("./powerTable1b.pot", "wb") as fp:
            fp.write(powerTable1b.tobytes())

    elif choice == 2:
        tonMaxNs = round(float(input("Selezionare Ton massimo (valore "+str(GS8_MAX_VALUE)+") [us]: "))*1000)
        powerTableGS8 = array("H", (0,) * GS8_SIZE)
        step = tonMaxNs / GS8_MAX_VALUE
        for i in range(GS8_SIZE):
            powerTableGS8[i] = round(step * i)

        with open("./powerTableGS8.pot", "wb") as fp:
            fp.write(powerTableGS8.tobytes())

    elif choice == 3:
        tonMaxNs = round(float(input("Selezionare Ton massimo (valore "+str(GS16_MAX_VALUE)+") [us]: "))*1000)
        powerTableGS16 = array("H", (0,) * GS16_SIZE)
        step = tonMaxNs / GS16_MAX_VALUE

        for i in range(GS16_SIZE):
            powerTableGS16[i] = round(step * i)

        with open("./powerTableGS16.pot", "wb") as fp:
            fp.write(powerTableGS16.tobytes())
