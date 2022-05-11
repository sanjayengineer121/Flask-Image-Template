from PIL import Image
from random import randint
import sys
import os

class PixelFilterIterator:
    def __init__(self, image, mask):
        self.original = image
        self.pixels = image.load()
        self.output = image.copy()
        self.outputPixels = self.output.load()
        self.x = 0
        self.y = 0
        self.currentPixel = self.pixels[0,0]
        self.sizeX = image.size[0]
        self.sizeY = image.size[1]
        self.mask = mask
        self.maskSum = self.calculateMask()
        if(len(self.mask) % 2 == 0):
            print("Not supporting even filters")
            raise Exception("Not supporting even filters")

    def calculateMask(self):
        summedMaskValue = 0
        for y in range(0, len(self.mask)):
            for x in range(0, len(self.mask[0])):
                maskValue = self.mask[x][y]
                summedMaskValue = summedMaskValue + maskValue
        if(summedMaskValue == 0):
            return 1
        return summedMaskValue

    def nextX(self):
        if(self.x < self.sizeX):
            self.x = self.x + 1
            self.currentPixel = self.pixels[self.x, self.y]
            print(str(round((self.y / self.sizeY*100),2)) + "%           ", end = "\r")
        else:
            raise Exception("No next x")

    def nextY(self):
        if(self.y < self.sizeY):
            self.y = self.y + 1
            self.x = 0
            self.currentPixel = self.pixels[self.x, self.y]
        else:
            raise Exception("No next y")

    def getPixelAt(self, x, y):
        if(x >= self.sizeX or x < 0):
            return None
        elif(y >= self.sizeY or y < 0):
            return None
        return self.pixels[x, y]
        

    def filterCurrentPixel(self):
        center = len(self.mask)//2
        pix = [self.currentPixel[0],self.currentPixel[1],self.currentPixel[2]]
        summed = [0, 0, 0]
        for y in range(0, len(self.mask)):
            for x in range(0, len(self.mask[0])):
                maskValue = self.mask[x][y]
                if(maskValue == 0):
                    continue
                pixelValue = self.getRelativePixel(x - center, y - center)
                if(pixelValue == None):
                    continue
                    
                r = pixelValue[0]
                g = pixelValue[1]
                b = pixelValue[2]
                summed[0] = summed[0] + (r * maskValue)
                summed[1] = summed[1] + (g * maskValue)
                summed[2] = summed[2] + (b * maskValue)
        for index in range(0, len(summed)):
            piece = summed[index]
            pix[index] = round(piece / self.maskSum)
        self.outputPixels[self.x, self.y] = (pix[0], pix[1], pix[2])

    def getRelativePixel(self, xDelta, yDelta):
        return self.getPixelAt(self.x + xDelta, self.y + yDelta)

    def filterImage(self):
        for y in range(0, self.sizeY - 1):
            for x in range(0, self.sizeX - 1):
                self.filterCurrentPixel()
                self.nextX()
            self.nextY()
        print("100.00%")
        print("Done")
    
def loadImage(path):
    image = Image.open(path)
    return image

def maskGenerator(n):
    result = []
    for y in range(0, n):
        xRow = []
        for x in range(0, n):
            xRow.append(randint(-5, 5))
        result.append(xRow)
    print(result)
    return result

def parseMask(maskString):
    realMask = []
    splitted = maskString.split(":")
    for element in splitted:
        xRow = []
        splittedX = element.split(",")
        for xElement in splittedX:
            xRow.append(float(xElement))
        realMask.append(xRow)
    return realMask

def parseMaskFromFile(maskFilePath):
    maskFile = open(maskFilePath, "r")
    content = maskFile.readlines()
    realMask = []
    for element in content:
        xRow = []
        splittedX = element.split(",")
        for xElement in splittedX:
            xRow.append(float(xElement))
        realMask.append(xRow)
    return realMask
    
def preetyPrintMask(mask):
    print("---------------------------------")
    print("Loaded mask:")
    for y in range(0, len(mask)):
        for x in range(0, len(mask[0])):
            val = mask[y][x]
            if(val >= 0):
                print("", mask[y][x], end="\t")
            else:
                print(mask[y][x], end="\t")
        print()
    print("---------------------------------")

def main():
    if(len(sys.argv) < 4):
        print("Usage:   [from] [to] [maskOrMaskFile]")
        print("Example: test.jpg test-done.jpg 1,1,1:1,1,1:1,1,1")
        print("Example: test.jpg test-done.jpg mask.txt")
        f=open('mask.txt','r')
        
        sys.exit(1)
    maskArg = sys.argv[3]
    mask = []
    if(os.path.exists(maskArg)):
        mask = parseMaskFromFile(maskArg)
    else:
        mask = parseMask(maskArg)
    preetyPrintMask(mask)
    image = loadImage(sys.argv[1])
    pixelIterator = PixelFilterIterator(image, mask)
    pixelIterator.filterImage()
    pixelIterator.output.save(sys.argv[2])

if __name__ == "__main__":
    main()
