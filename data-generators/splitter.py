import os.path


if __name__ == "__main__":

    print("Splitter area dati")

    try:
        filepath = input("Inserire file da suddividere: ")
        with open(filepath, "rb") as f:
            pass
    except OSError as err:
        print("File non trovato")
        exit(-1)

    try:
        print("Size constraints (1 elemento = 4 byte, BURST=64):\n"
              "1. dimensione > 64*10 elementi = 2560 byte\n"
              "2. dimensione > 2 colonne intere (tutti i bit del VE a 1)\n"
              "3. dimensione % (element*BURST = 256 byte) == 0\n"
              "4. Max dimensione DDR per dati =~ 550 MB = 550*1024*1024 byte")
        dataSize = int(input("Dimensione chunk dati [MB]: "))
    except ValueError as ve:
        print("Errore conversione: "+str(ve))
        exit(-1)

    dataSize = dataSize * 1024 * 1024
    print("Dimensione in byte: "+str(dataSize))

    try:
        path, filename = os.path.split(os.path.abspath(filepath))
        name, extension = os.path.splitext(filename)

        destpath = os.path.dirname(os.path.abspath(__file__)) + "/./output"

        with open(filepath, "rb") as f:
            iterate = True
            iteration = 0
            while iterate:
                print("Iteration: "+str(iteration))
                print("Lettura dati")
                dataChunk = f.read(dataSize)
                f.seek(dataSize*(iteration+1))
                iterate = dataChunk != b""
                if not iterate:
                    continue

                newFilename = destpath + "/" + name + "-" + str(iteration) + extension
                print("Scrittura dati: "+newFilename)
                with open(newFilename, "wb") as fw:
                    fw.write(dataChunk)
                iteration += 1

    except OSError as err:
        print("Err: "+str(err))
        exit(-1)

    exit(0)