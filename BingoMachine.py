from PIL import Image, ImageDraw, ImageFont
import os
import math
from random import shuffle

background = Image.new("RGBA", (794, 1122), color="white")
W, H = background.size
columns = int(input("How many columns do you want on your bingo cards?"))
numberOfCards = int(input("How many bingo cards do you want?"))
cardTitles = input("What title do you want at the top of your bingo cards?")
squarewidth = int((W*.90)/columns)
squareheight = squarewidth
numberOfBingoItems = int(columns*columns)

def drawborder():
    draw = ImageDraw.Draw(background)
    draw.rectangle(((int(W*.01)),(int(H*.01)),(int(W*.99)),(int(H*.99))), fill=None, outline="black")

def loadimages():
    global bingoitems
    bingoitems = []
    for filename in os.listdir("BingoItems"):
        try:
            im = Image.open("BingoItems/%s" %filename, 'r')
            basewh = int(squarewidth/1.2)
            #im = im.resize((basewh,basewh), resample=0).convert("RGBA")
            if im.height == im.width:
               im = im.resize((basewh,squareheight), 0).convert("RGBA")
            if im.width > im.height:
               wpercent = (basewh/float(im.size[0]))
               hsize = int((float(im.size[1])*float(wpercent)))
               im = im.resize((basewh,hsize), 0).convert("RGBA")
            if im.height > im.width:
               hpercent = (basewh/float(im.size[1]))
               wsize = int((float(im.size[0])*float(hpercent)))
               im = im.resize((wsize,basewh), 0).convert("RGBA")

            #paste images centered onto square canvas
            centeredImage = Image.new("RGBA", (squarewidth,squareheight), color="white")
            x1 = int(math.floor((centeredImage.width - im.width) / 2))
            y1 = int(math.floor((centeredImage.height - im.height) / 2))
            centeredImage.paste(im, (x1,y1,x1+im.width,y1+im.height), mask=im)
            im = centeredImage
            bingoitems.append(im)
        except:
            pass
    return bingoitems

def pasteimages():
    draw = ImageDraw.Draw(background)
    y = (H*.3)
    x = (W*.05)
    nextitem = 0
    for j in range(0, columns+1):
        for i in range(0, columns):
            x1 = x+(squarewidth*i)
            y1 = y+(squareheight*j)

            if nextitem < columns **2:
                background.paste(bingoitems[nextitem], box=(int(x1), int(y1)), mask=None)
                nextitem = nextitem +1


def drawgrid(color):
    draw = ImageDraw.Draw(background)
    y = (H*.3)
    x = (W*.05)
    for j in range(0, columns+1):
        for i in range(0, columns):
            x1 = x+(squarewidth*i)
            y1 = y+(squareheight*j)
            x2 = x+(squarewidth*i)+squarewidth
            y2 = y+(squareheight*j)
            draw.line(((x1,y1), (x2,y2)), fill=color, width=3)

            x3 = x+(squarewidth*j)
            y3 = y+(squareheight*i)
            x4 = x+(squarewidth*j)
            y4 = y+(squareheight*i)+squareheight

            draw.line(((x3,y3), (x4,y4)), fill=color, width=3)


def shuffleimages():
    loadimages()
    shuffle(bingoitems)
    del bingoitems[numberOfBingoItems:]

def title(title):
    draw = ImageDraw.Draw(background)
    w, h = draw.textsize(title, font=ImageFont.truetype("/Library/Fonts/Avenir LT 95 Black.ttf", 50))
    draw.text((((W-w)/2), ((H-h)/5)), title, font=ImageFont.truetype("/Library/Fonts/Avenir LT 95 Black.ttf", 50), fill=(0,0,0,255))

count = 1
def savecards():
    global count
    background.save("NewBingo%s.png" %count, "PNG")
    print ("Making Bingo Card #%s.png" %count, "PNG")
    count = count + 1

if __name__ == "__main__":
    for x in range(0,numberOfCards):
        loadimages()
        shuffleimages()
        pasteimages()
        drawgrid("black")
        drawborder()
        title(cardTitles)
        savecards()
