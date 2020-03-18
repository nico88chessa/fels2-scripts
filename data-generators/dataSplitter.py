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
              "1. dimensione > 64*10 elementi\n"
              "2. dimensione > 2 colonne intere (tutti i bit del VE a 1)\n"
              "3. dimensione % (element*BURST = 256 bytes) == 0\n")
        dataSize = int(input("Dimensione chunk dati [byte]: "))
    except ValueError as ve:
        print("Errore conversione: "+str(ve))
        exit(-1)

    try:
        fullpath = os.path.abspath(filepath)
        path, filename = os.path.split(fullpath)
        name, extension = os.path.splitext(filename)

        with open(filepath, "rb") as f:
            iterate = True
            iteration = 0
            while iterate:
                dataChunk = f.read(dataSize)
                f.seek(dataSize*(iteration+1))
                iterate = dataChunk != b""
                if not iterate:
                    continue

                newFilename = path + "/" + name + "-" + str(iteration) + extension
                with open(newFilename, "wb") as fw:
                    fw.write(dataChunk)
                iteration += 1

    except OSError as err:
        print("Err: "+str(err))
        exit(-1)

    exit(0)