import os.path


if __name__ == "__main__":

    print("Raw aggregate")
    print("Questo script serve per unire piu file raw in uno solo piu grande")
    sourceFile = input("Inserire percorso file raw: ")

    if not os.path.exists(sourceFile):
        print("Path errata")
        exit(1)

    sourceFullpath = os.path.abspath(sourceFile)
    numCopies = int(input("Inserire il numero di volte che il file deve essere replicato: "))

    path, filename = os.path.split(sourceFullpath)
    name, extension = os.path.splitext(filename)
    destpath = os.path.dirname(os.path.abspath(__file__)) + "/./output"
    destFile = destpath + "/./" + name + "-BIG" + extension

    if os.path.exists(destFile):
        print("File gia trovato... sara' sovrascritto")

    with open(sourceFullpath, "rb") as fp:

        bytes = fp.read()
        with open(destFile, "w+b") as fpw:
            for i in range(0, numCopies):
                fpw.write(bytes)

