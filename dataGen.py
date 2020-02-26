from PIL import Image, TiffTags
from array import array
import math

#  ./images/BN-10col-W1000H1@2540dpi.tif
#  ./images/grayscale-0.5x1@2540dpi.tif

if __name__ == "__main__":

    # filePath = "./images/BN-0.5x1@2540dpi.tif"
    # filePath = "./images/triangolo-20x10@2540.tif"
    # filePath = "./images/grayscale-0.5x1@2540dpi.tif"
    filePath = input("Inserire nome file: ")
    print("Filepath: "+filePath)

    with Image.open(filePath) as image:

        width, height = image.size
        numPixels = width * height
        imageData = list(image.getdata())

        print("Image mode: "+str(image.mode))
        tiffTags = {TiffTags.lookup(k).name: v for k, v in image.tag_v2.items()}
        blackIsZero = (tiffTags["PhotometricInterpretation"]==1)

        '''
        Image open se ne frega dell'interpretazione del tif. 255 e' bianco e 0 e' nero SEMPRE.
        per cui devo sempre invertire
        
        if blackIsZero:
            imageData = [255-imageData[i] for i in range(len(imageData))]
        '''
        imageData = [255 - imageData[i] for i in range(len(imageData))]

        imageRows = [imageData[i*width : (i+1)*width] for i in range(height)]

        print("Immagine letta correttamente.")
        numPixelCircumference = int(input("Numero pixel della circonferenza (min: "+str(width)+"): "))

        if numPixelCircumference < width:
            print("Immagine piu' grande della circonferenza")
            exit(1)

        print("Modalita' di stampa: \n"
              "1. B/N\n"
              "2. GS8\n"
              "3. GS16\n")
        sc = int(input("Scelta: "))
        numLaser = int(input("Inserire il numero di laser: "))

        if sc==1:
            if numLaser == 1:
                chunk = math.ceil(height / numLaser)
                # cylinderRows = [[0] * numPixelCircumference for i in range(chunk)]

                bytesPerRow = math.ceil(numPixelCircumference / 8)
                bytesPerImage = bytesPerRow*height

                rawImage = array("B", [0]*bytesPerImage)

                for r in range(height):
                    # cylinderRows[r][0:width] = imageRows[r]
                    cylinderRow = [0] * numPixelCircumference
                    cylinderRow[0:width] = imageRows[r]
                    for c in range(width):
                        index = int((r*bytesPerRow)+math.floor(c/8))
                        offset = int(c%8)
                        value = 0x00 if (cylinderRow[c]==0) else (0x01 << offset)
                        rawImage[index] |= value

                with open("./1b-1laser.raw", "wb") as f:
                    f.write(rawImage.tobytes())

            elif numLaser <= 8:
                chunk = math.ceil(height / numLaser)
                # cylinderRows = [[0] * numPixelCircumference for i in range(chunk)]
                # bytesPerRow = math.ceil(numPixelCircumference)
                # byt8esPerImage = bytesPerRow * height
                # rawImage = array("B", [0] * bytesPerImage)
                rawImage = array("B", [0] * numPixels)

                for c in range(chunk):
                    cylinderRow = [0] * numPixelCircumference
                    for colChunk in range(width):
                        #cylinderRows[c][colChunk] |= (0x01 << 0) if numLaser > 0 and ((c*numLaser) + 0)<height and imageRows[(c*numLaser) + 0][colChunk]==255 else 0x00
                        #cylinderRows[c][colChunk] |= (0x01 << 1) if numLaser > 1 and ((c*numLaser) + 1)<height and imageRows[(c*numLaser) + 1][colChunk]==255 else 0x00
                        #cylinderRows[c][colChunk] |= (0x01 << 2) if numLaser > 2 and ((c*numLaser) + 2)<height and imageRows[(c*numLaser) + 2][colChunk]==255 else 0x00
                        #cylinderRows[c][colChunk] |= (0x01 << 3) if numLaser > 3 and ((c*numLaser) + 3)<height and imageRows[(c*numLaser) + 3][colChunk]==255 else 0x00
                        #cylinderRows[c][colChunk] |= (0x01 << 4) if numLaser > 4 and ((c*numLaser) + 4)<height and imageRows[(c*numLaser) + 4][colChunk]==255 else 0x00
                        #cylinderRows[c][colChunk] |= (0x01 << 5) if numLaser > 5 and ((c*numLaser) + 5)<height and imageRows[(c*numLaser) + 5][colChunk]==255 else 0x00
                        #cylinderRows[c][colChunk] |= (0x01 << 6) if numLaser > 6 and ((c*numLaser) + 6)<height and imageRows[(c*numLaser) + 6][colChunk]==255 else 0x00
                        #cylinderRows[c][colChunk] |= (0x01 << 7) if numLaser > 7 and ((c*numLaser) + 7)<height and imageRows[(c*numLaser) + 7][colChunk]==255 else 0x00

                        cylinderRow[colChunk] |= (0x01 << 0) if numLaser > 0 and ((c*numLaser) + 0)<height and imageRows[(c*numLaser) + 0][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 1) if numLaser > 1 and ((c*numLaser) + 1)<height and imageRows[(c*numLaser) + 1][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 2) if numLaser > 2 and ((c*numLaser) + 2)<height and imageRows[(c*numLaser) + 2][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 3) if numLaser > 3 and ((c*numLaser) + 3)<height and imageRows[(c*numLaser) + 3][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 4) if numLaser > 4 and ((c*numLaser) + 4)<height and imageRows[(c*numLaser) + 4][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 5) if numLaser > 5 and ((c*numLaser) + 5)<height and imageRows[(c*numLaser) + 5][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 6) if numLaser > 6 and ((c*numLaser) + 6)<height and imageRows[(c*numLaser) + 6][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 7) if numLaser > 7 and ((c*numLaser) + 7)<height and imageRows[(c*numLaser) + 7][colChunk]==255 else 0x00


                    # rawImage[c*bytesPerRow:] = array('B', cylinderRows[c])
                    rawImage[c * numPixelCircumference:] = array("B", cylinderRow)

                with open("./1b-8laser.raw", "wb") as f:
                    f.write(rawImage.tobytes())

            elif numLaser <= 16:
                chunk = math.ceil(height / numLaser)
                # bytesPerRow = math.ceil(numPixelCircumference)*2
                # bytesPerImage = bytesPerRow * height
                # rawImage = array("H", [0] * bytesPerImage)
                rawImage = array("H", [0] * numPixels)
                for c in range(chunk):
                    cylinderRow = [0] * numPixelCircumference
                    for colChunk in range(width):
                        cylinderRow[colChunk] |= (0x01 << 0) if numLaser > 0 and ((c*numLaser) + 0)<height and imageRows[(c*numLaser) + 0][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 1) if numLaser > 1 and ((c*numLaser) + 1)<height and imageRows[(c*numLaser) + 1][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 2) if numLaser > 2 and ((c*numLaser) + 2)<height and imageRows[(c*numLaser) + 2][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 3) if numLaser > 3 and ((c*numLaser) + 3)<height and imageRows[(c*numLaser) + 3][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 4) if numLaser > 4 and ((c*numLaser) + 4)<height and imageRows[(c*numLaser) + 4][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 5) if numLaser > 5 and ((c*numLaser) + 5)<height and imageRows[(c*numLaser) + 5][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 6) if numLaser > 6 and ((c*numLaser) + 6)<height and imageRows[(c*numLaser) + 6][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 7) if numLaser > 7 and ((c*numLaser) + 7)<height and imageRows[(c*numLaser) + 7][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 8) if numLaser > 8 and ((c*numLaser) + 8)<height and imageRows[(c*numLaser) + 8][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 9) if numLaser > 9 and ((c*numLaser) + 9)<height and imageRows[(c*numLaser) + 9][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 10) if numLaser > 10 and ((c*numLaser) + 10)<height and imageRows[(c*numLaser) + 10][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 11) if numLaser > 11 and ((c*numLaser) + 11)<height and imageRows[(c*numLaser) + 11][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 12) if numLaser > 12 and ((c*numLaser) + 12)<height and imageRows[(c*numLaser) + 12][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 13) if numLaser > 13 and ((c*numLaser) + 13)<height and imageRows[(c*numLaser) + 13][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 14) if numLaser > 14 and ((c*numLaser) + 14)<height and imageRows[(c*numLaser) + 14][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 15) if numLaser > 15 and ((c*numLaser) + 15)<height and imageRows[(c*numLaser) + 15][colChunk]==255 else 0x00
                    rawImage[c * numPixelCircumference:] = array("H", cylinderRow)
                with open("./1b-16laser.raw", "wb") as f:
                    f.write(rawImage.tobytes())

            elif numLaser <= 32:
                chunk = math.ceil(height / numLaser)
                # bytesPerRow = math.ceil(numPixelCircumference) * 4
                # bytesPerImage = bytesPerRow * height
                # rawImage = array("I", [0] * bytesPerImage)
                rawImage = array("I", [0] * numPixels)
                for c in range(chunk):
                    cylinderRow = [0] * numPixelCircumference
                    for colChunk in range(width):
                        cylinderRow[colChunk] |= (0x01 << 0) if numLaser > 0 and ((c*numLaser) + 0)<height and imageRows[(c*numLaser) + 0][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 1) if numLaser > 1 and ((c*numLaser) + 1)<height and imageRows[(c*numLaser) + 1][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 2) if numLaser > 2 and ((c*numLaser) + 2)<height and imageRows[(c*numLaser) + 2][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 3) if numLaser > 3 and ((c*numLaser) + 3)<height and imageRows[(c*numLaser) + 3][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 4) if numLaser > 4 and ((c*numLaser) + 4)<height and imageRows[(c*numLaser) + 4][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 5) if numLaser > 5 and ((c*numLaser) + 5)<height and imageRows[(c*numLaser) + 5][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 6) if numLaser > 6 and ((c*numLaser) + 6)<height and imageRows[(c*numLaser) + 6][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 7) if numLaser > 7 and ((c*numLaser) + 7)<height and imageRows[(c*numLaser) + 7][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 8) if numLaser > 8 and ((c*numLaser) + 8)<height and imageRows[(c*numLaser) + 8][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 9) if numLaser > 9 and ((c*numLaser) + 9)<height and imageRows[(c*numLaser) + 9][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 10) if numLaser > 10 and ((c*numLaser) + 10)<height and imageRows[(c*numLaser) + 10][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 11) if numLaser > 11 and ((c*numLaser) + 11)<height and imageRows[(c*numLaser) + 11][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 12) if numLaser > 12 and ((c*numLaser) + 12)<height and imageRows[(c*numLaser) + 12][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 13) if numLaser > 13 and ((c*numLaser) + 13)<height and imageRows[(c*numLaser) + 13][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 14) if numLaser > 14 and ((c*numLaser) + 14)<height and imageRows[(c*numLaser) + 14][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 15) if numLaser > 15 and ((c*numLaser) + 15)<height and imageRows[(c*numLaser) + 15][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 16) if numLaser > 16 and ((c*numLaser) + 16)<height and imageRows[(c*numLaser) + 16][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 17) if numLaser > 17 and ((c*numLaser) + 17)<height and imageRows[(c*numLaser) + 17][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 18) if numLaser > 18 and ((c*numLaser) + 18)<height and imageRows[(c*numLaser) + 18][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 19) if numLaser > 19 and ((c*numLaser) + 19)<height and imageRows[(c*numLaser) + 19][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 20) if numLaser > 20 and ((c*numLaser) + 20)<height and imageRows[(c*numLaser) + 20][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 21) if numLaser > 21 and ((c*numLaser) + 21)<height and imageRows[(c*numLaser) + 21][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 22) if numLaser > 22 and ((c*numLaser) + 22)<height and imageRows[(c*numLaser) + 22][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 23) if numLaser > 23 and ((c*numLaser) + 23)<height and imageRows[(c*numLaser) + 23][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 24) if numLaser > 24 and ((c*numLaser) + 24)<height and imageRows[(c*numLaser) + 24][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 25) if numLaser > 25 and ((c*numLaser) + 25)<height and imageRows[(c*numLaser) + 25][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 26) if numLaser > 26 and ((c*numLaser) + 26)<height and imageRows[(c*numLaser) + 26][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 27) if numLaser > 27 and ((c*numLaser) + 27)<height and imageRows[(c*numLaser) + 27][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 28) if numLaser > 28 and ((c*numLaser) + 28)<height and imageRows[(c*numLaser) + 28][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 29) if numLaser > 29 and ((c*numLaser) + 29)<height and imageRows[(c*numLaser) + 29][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 30) if numLaser > 30 and ((c*numLaser) + 30)<height and imageRows[(c*numLaser) + 30][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 31) if numLaser > 31 and ((c*numLaser) + 31)<height and imageRows[(c*numLaser) + 31][colChunk]==255 else 0x00
                    rawImage[c * numPixelCircumference:] = array("I", cylinderRow)
                with open("./1b-32laser.raw", "wb") as f:
                    f.write(rawImage.tobytes())

            elif numLaser <= 64:
                chunk = math.ceil(height / numLaser)
                # bytesPerRow = math.ceil(numPixelCircumference) * 8
                # bytesPerImage = bytesPerRow * height
                # rawImage = array("L", [0] * bytesPerImage)
                rawImage = array("L", [0] * numPixels)
                for c in range(chunk):
                    cylinderRow = [0] * numPixelCircumference
                    for colChunk in range(width):
                        cylinderRow[colChunk] |= (0x01 << 0) if numLaser > 0 and ((c*numLaser) + 0)<height and imageRows[(c*numLaser) + 0][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 1) if numLaser > 1 and ((c*numLaser) + 1)<height and imageRows[(c*numLaser) + 1][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 2) if numLaser > 2 and ((c*numLaser) + 2)<height and imageRows[(c*numLaser) + 2][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 3) if numLaser > 3 and ((c*numLaser) + 3)<height and imageRows[(c*numLaser) + 3][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 4) if numLaser > 4 and ((c*numLaser) + 4)<height and imageRows[(c*numLaser) + 4][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 5) if numLaser > 5 and ((c*numLaser) + 5)<height and imageRows[(c*numLaser) + 5][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 6) if numLaser > 6 and ((c*numLaser) + 6)<height and imageRows[(c*numLaser) + 6][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 7) if numLaser > 7 and ((c*numLaser) + 7)<height and imageRows[(c*numLaser) + 7][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 8) if numLaser > 8 and ((c*numLaser) + 8)<height and imageRows[(c*numLaser) + 8][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 9) if numLaser > 9 and ((c*numLaser) + 9)<height and imageRows[(c*numLaser) + 9][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 10) if numLaser > 10 and ((c*numLaser) + 10)<height and imageRows[(c*numLaser) + 10][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 11) if numLaser > 11 and ((c*numLaser) + 11)<height and imageRows[(c*numLaser) + 11][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 12) if numLaser > 12 and ((c*numLaser) + 12)<height and imageRows[(c*numLaser) + 12][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 13) if numLaser > 13 and ((c*numLaser) + 13)<height and imageRows[(c*numLaser) + 13][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 14) if numLaser > 14 and ((c*numLaser) + 14)<height and imageRows[(c*numLaser) + 14][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 15) if numLaser > 15 and ((c*numLaser) + 15)<height and imageRows[(c*numLaser) + 15][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 16) if numLaser > 16 and ((c*numLaser) + 16)<height and imageRows[(c*numLaser) + 16][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 17) if numLaser > 17 and ((c*numLaser) + 17)<height and imageRows[(c*numLaser) + 17][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 18) if numLaser > 18 and ((c*numLaser) + 18)<height and imageRows[(c*numLaser) + 18][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 19) if numLaser > 19 and ((c*numLaser) + 19)<height and imageRows[(c*numLaser) + 19][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 20) if numLaser > 20 and ((c*numLaser) + 20)<height and imageRows[(c*numLaser) + 20][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 21) if numLaser > 21 and ((c*numLaser) + 21)<height and imageRows[(c*numLaser) + 21][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 22) if numLaser > 22 and ((c*numLaser) + 22)<height and imageRows[(c*numLaser) + 22][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 23) if numLaser > 23 and ((c*numLaser) + 23)<height and imageRows[(c*numLaser) + 23][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 24) if numLaser > 24 and ((c*numLaser) + 24)<height and imageRows[(c*numLaser) + 24][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 25) if numLaser > 25 and ((c*numLaser) + 25)<height and imageRows[(c*numLaser) + 25][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 26) if numLaser > 26 and ((c*numLaser) + 26)<height and imageRows[(c*numLaser) + 26][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 27) if numLaser > 27 and ((c*numLaser) + 27)<height and imageRows[(c*numLaser) + 27][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 28) if numLaser > 28 and ((c*numLaser) + 28)<height and imageRows[(c*numLaser) + 28][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 29) if numLaser > 29 and ((c*numLaser) + 29)<height and imageRows[(c*numLaser) + 29][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 30) if numLaser > 30 and ((c*numLaser) + 30)<height and imageRows[(c*numLaser) + 30][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 31) if numLaser > 31 and ((c*numLaser) + 31)<height and imageRows[(c*numLaser) + 31][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 32) if numLaser > 32 and ((c*numLaser) + 32)<height and imageRows[(c*numLaser) + 32][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 33) if numLaser > 33 and ((c*numLaser) + 33)<height and imageRows[(c*numLaser) + 33][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 34) if numLaser > 34 and ((c*numLaser) + 34)<height and imageRows[(c*numLaser) + 34][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 35) if numLaser > 35 and ((c*numLaser) + 35)<height and imageRows[(c*numLaser) + 35][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 36) if numLaser > 36 and ((c*numLaser) + 36)<height and imageRows[(c*numLaser) + 36][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 37) if numLaser > 37 and ((c*numLaser) + 37)<height and imageRows[(c*numLaser) + 37][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 38) if numLaser > 38 and ((c*numLaser) + 38)<height and imageRows[(c*numLaser) + 38][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 39) if numLaser > 39 and ((c*numLaser) + 39)<height and imageRows[(c*numLaser) + 39][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 40) if numLaser > 40 and ((c*numLaser) + 40)<height and imageRows[(c*numLaser) + 40][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 41) if numLaser > 41 and ((c*numLaser) + 41)<height and imageRows[(c*numLaser) + 41][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 42) if numLaser > 42 and ((c*numLaser) + 42)<height and imageRows[(c*numLaser) + 42][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 43) if numLaser > 43 and ((c*numLaser) + 43)<height and imageRows[(c*numLaser) + 43][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 44) if numLaser > 44 and ((c*numLaser) + 44)<height and imageRows[(c*numLaser) + 44][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 45) if numLaser > 45 and ((c*numLaser) + 45)<height and imageRows[(c*numLaser) + 45][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 46) if numLaser > 46 and ((c*numLaser) + 46)<height and imageRows[(c*numLaser) + 46][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 47) if numLaser > 47 and ((c*numLaser) + 47)<height and imageRows[(c*numLaser) + 47][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 48) if numLaser > 48 and ((c*numLaser) + 48)<height and imageRows[(c*numLaser) + 48][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 49) if numLaser > 49 and ((c*numLaser) + 49)<height and imageRows[(c*numLaser) + 49][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 50) if numLaser > 50 and ((c*numLaser) + 50)<height and imageRows[(c*numLaser) + 50][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 51) if numLaser > 51 and ((c*numLaser) + 51)<height and imageRows[(c*numLaser) + 51][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 52) if numLaser > 52 and ((c*numLaser) + 52)<height and imageRows[(c*numLaser) + 52][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 53) if numLaser > 53 and ((c*numLaser) + 53)<height and imageRows[(c*numLaser) + 53][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 54) if numLaser > 54 and ((c*numLaser) + 54)<height and imageRows[(c*numLaser) + 54][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 55) if numLaser > 55 and ((c*numLaser) + 55)<height and imageRows[(c*numLaser) + 55][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 56) if numLaser > 56 and ((c*numLaser) + 56)<height and imageRows[(c*numLaser) + 56][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 57) if numLaser > 57 and ((c*numLaser) + 57)<height and imageRows[(c*numLaser) + 57][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 58) if numLaser > 58 and ((c*numLaser) + 58)<height and imageRows[(c*numLaser) + 58][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 59) if numLaser > 59 and ((c*numLaser) + 59)<height and imageRows[(c*numLaser) + 59][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 60) if numLaser > 60 and ((c*numLaser) + 60)<height and imageRows[(c*numLaser) + 60][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 61) if numLaser > 61 and ((c*numLaser) + 61)<height and imageRows[(c*numLaser) + 61][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 62) if numLaser > 62 and ((c*numLaser) + 62)<height and imageRows[(c*numLaser) + 62][colChunk]==255 else 0x00
                        cylinderRow[colChunk] |= (0x01 << 63) if numLaser > 63 and ((c*numLaser) + 63)<height and imageRows[(c*numLaser) + 63][colChunk]==255 else 0x00
                    rawImage[c * numPixelCircumference:] = array("L", cylinderRow)
                with open("./1b-64laser.raw", "wb") as f:
                    f.write(rawImage.tobytes())

        elif sc==2:
            if numLaser == 1:
                chunk = math.ceil(height / numLaser)
                # bytesPerRow = math.ceil(numPixelCircumference) * 1
                # bytesPerImage = bytesPerRow * height
                # rawImage = array("B", [0] * bytesPerImage)
                rawImage = array("B", [0] * numPixels)
                for c in range(chunk):
                    cylinderRow = [0] * numPixelCircumference
                    # for col in range(width):
                    #     cylinderRow[col] = imageRows[c][col]
                    cylinderRow[:width] = imageRows[c]
                    rawImage[c * numPixelCircumference:] = array("B", cylinderRow)

                with open("./GS8-1laser.raw", "wb") as f:
                    f.write(rawImage.tobytes())

            elif numLaser == 2:
                chunk = math.ceil(height / numLaser)
                # bytesPerRow = math.ceil(numPixelCircumference) * 2
                # bytesPerImage = bytesPerRow * height
                # rawImage = array("H", [0] * bytesPerImage)
                rawImage = array("H", [0] * numPixels)
                for c in range(chunk):
                    cylinderRow = [0] * numPixelCircumference
                    for col in range(width):
                        cylinderRow[col] |= imageRows[(c*numLaser) + 0][col]
                        cylinderRow[col] |= (imageRows[(c*numLaser) + 1][col] << 8) if ((c*numLaser) + 1)<height else 0x00
                    rawImage[c*numPixelCircumference:] = array("H", cylinderRow)

                with open("./GS8-2laser.raw", "wb") as f:
                    f.write(rawImage.tobytes())

            elif numLaser <= 4:
                chunk = math.ceil(height / numLaser)
                # bytesPerRow = math.ceil(numPixelCircumference) * 4
                # bytesPerImage = bytesPerRow * height
                # rawImage = array("I", [0] * bytesPerImage)
                rawImage = array("I", [0] * numPixels)
                for c in range(chunk):
                    cylinderRow = [0] * numPixelCircumference
                    for col in range(width):
                        cylinderRow[col] |= (imageRows[(c*numLaser) + 0][col] << 0) if numLaser > 0 and ((c*numLaser) + 0) < height else 0x00
                        cylinderRow[col] |= (imageRows[(c*numLaser) + 1][col] << 8) if  numLaser > 1 and ((c*numLaser) + 1) < height else 0x00
                        cylinderRow[col] |= (imageRows[(c*numLaser) + 2][col] << 16) if numLaser > 2 and ((c*numLaser) + 2) < height else 0x00
                        cylinderRow[col] |= (imageRows[(c*numLaser) + 3][col] << 24) if numLaser > 3 and ((c*numLaser) + 3) < height else 0x00
                    rawImage[c * numPixelCircumference:] = array("I", cylinderRow)

                with open("./GS8-4laser.raw", "wb") as f:
                    f.write(rawImage.tobytes())

            elif numLaser <= 8:
                chunk = math.ceil(height / numLaser)
                # bytesPerRow = math.ceil(numPixelCircumference) * 4
                # bytesPerImage = bytesPerRow * height
                # rawImage = array("L", [0] * bytesPerImage)
                rawImage = array("L", [0] * numPixels)
                for c in range(chunk):
                    cylinderRow = [0] * numPixelCircumference
                    for col in range(width):
                        cylinderRow[col] |= (imageRows[(c*numLaser) + 0][col] << 0) if numLaser > 0 and ((c*numLaser) + 0) < height else 0x00
                        cylinderRow[col] |= (imageRows[(c*numLaser) + 1][col] << 8) if  numLaser > 1 and ((c*numLaser) + 1) < height else 0x00
                        cylinderRow[col] |= (imageRows[(c*numLaser) + 2][col] << 16) if numLaser > 2 and ((c*numLaser) + 2) < height else 0x00
                        cylinderRow[col] |= (imageRows[(c*numLaser) + 3][col] << 24) if numLaser > 3 and ((c*numLaser) + 3) < height else 0x00
                        cylinderRow[col] |= (imageRows[(c*numLaser) + 4][col] << 32) if numLaser > 4 and ((c*numLaser) + 4) < height else 0x00
                        cylinderRow[col] |= (imageRows[(c*numLaser) + 5][col] << 40) if numLaser > 5 and ((c*numLaser) + 5) < height else 0x00
                        cylinderRow[col] |= (imageRows[(c*numLaser) + 6][col] << 48) if numLaser > 6 and ((c*numLaser) + 6) < height else 0x00
                        cylinderRow[col] |= (imageRows[(c*numLaser) + 7][col] << 56) if numLaser > 7 and ((c*numLaser) + 7) < height else 0x00
                    rawImage[c * numPixelCircumference:] = array("L", cylinderRow)

                with open("./GS8-8laser.raw", "wb") as f:
                    f.write(rawImage.tobytes())

        elif sc==3:

            if numLaser == 1:
                chunk = math.ceil(height / numLaser)
                # bytesPerRow = math.ceil(numPixelCircumference) * 2
                # bytesPerImage = bytesPerRow * height
                # rawImage = array("H", [0] * bytesPerImage)
                rawImage = array("H", [0] * numPixels)
                for c in range(chunk):
                    cylinderRow = [0] * numPixelCircumference
                    for col in range(width):
                        cylinderRow[col] = imageRows[c][col]
                    rawImage[c * numPixelCircumference:] = array("H", cylinderRow)

                with open("./GS16-1laser.map", "wb") as f:
                    f.write(rawImage.tobytes())

            elif numLaser == 2:
                chunk = math.ceil(height / numLaser)
                # bytesPerRow = math.ceil(numPixelCircumference) * 4
                # bytesPerImage = bytesPerRow * height
                # rawImage = array("I", [0] * bytesPerImage)
                rawImage = array("I", [0] * numPixels)
                for c in range(chunk):
                    cylinderRow = [0] * numPixelCircumference
                    for col in range(width):
                        cylinderRow[col] |= imageRows[(c*numLaser) + 0][col]
                        cylinderRow[col] |= (imageRows[(c*numLaser) + 1][col] << 16) if ((c*numLaser) + 1) < height else 0x00
                    rawImage[c * numPixelCircumference:] = array("I", cylinderRow)

                with open("./GS8-2laser.raw", "wb") as f:
                    f.write(rawImage.tobytes())

            elif numLaser <= 4:
                chunk = math.ceil(height / numLaser)
                # bytesPerRow = math.ceil(numPixelCircumference) * 8
                # bytesPerImage = bytesPerRow * height
                # rawImage = array('L', [0] * bytesPerImage)
                rawImage = array("L", [0] * numPixels)
                for c in range(chunk):
                    cylinderRow = [0] * numPixelCircumference
                    for col in range(width):
                        cylinderRow[col] |= (imageRows[(c*numLaser) + 0][col] << 0) if numLaser > 0 and ((c*numLaser) + 0) < height else 0x00
                        cylinderRow[col] |= (imageRows[(c*numLaser) + 1][col] << 16) if numLaser > 1 and ((c*numLaser) + 1) < height else 0x00
                        cylinderRow[col] |= (imageRows[(c*numLaser) + 2][col] << 32) if numLaser > 2 and ((c*numLaser) + 2) < height else 0x00
                        cylinderRow[col] |= (imageRows[(c*numLaser) + 3][col] << 48) if numLaser > 3 and ((c*numLaser) + 3) < height else 0x00
                    rawImage[c * numPixelCircumference:] = array("L", cylinderRow)

                with open("./GS8-4laser.raw", "wb") as f:
                    f.write(rawImage.tobytes())

    exit(0)