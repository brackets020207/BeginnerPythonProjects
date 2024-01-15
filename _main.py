from PIL import Image
import os, sys, time

compress = True
BrightnessMapping = 'luminosity'
width = 3

def clear():
    os.system('cls')

def menu():
    print('Ascii converter')
    print('------------------------')
    print('Options')
    print('Convert')
    print('Exit')
    meen = input()
    choices = {'convert':main, 'options': options, 'exit': leave}
    try:
        choices[meen]()
    except KeyError:
        print('not an option')
        menu()

def options():
    global compress
    global BrightnessMapping
    global width
    print('1 - Compress:', str(compress))
    print('2 - Brightness Mapping:', BrightnessMapping)
    print('3 - Width Multiplier:', str(width))
    print('q - Return to menu')
    option = {'1':compressoption, '2':mapping, '3':widthsetting, 'q':menu}
    choice = input()
    try:
        option[choice]()
    except KeyError:
        print('not an option')
        options()

def widthsetting():
    global width
    new = input('Enter width')
    try:
        width = int(new)
    except:
        print('Please enter an integer')
    

def mapping():
    global BrightnessMapping
    print('1 - Average')
    print('2 - Lightness')
    print('3 - Luminosity')
    print('4 - Back')
    choice = input()
    mappingdict = {'1':'average', '2':'lightness', '3':'luminosity'}
    if choice == '4':
        options()
    else:
        try:
            BrightnessMapping = mappingdict[choice]
            options()
        except KeyError:
            print('not an option')
            mapping()
        

def compressoption():
    global compress
    compress = input('Would you like the picture to be compressed?')
    compress = compress.startswith('y')
    options()
    


def leave():
    
    sys.exit()
    

def main():
    global compress
    global BrightnessMapping
    global width
    file = input('Enter filename\n')
    outfile = input('Enter outfile name\n')
    clear()
    try:
        img = Image.open(file)
    except FileNotFoundError:
        print('File was not found in the current directory')
    except OSError:
        print("That's not a picture file")
        
    if compress:
        for i in range(10):
            if img.width > 300:
                
                img = img.resize((round(img.width/2), round(img.height/2)))
        
    pixels = []
    for i in range(img.height):
        row = []
        for j in range(img.width):
            try:
                r,b,g = img.getpixel((j,i))
                if BrightnessMapping.lower() == 'average':
                    value = round(((r+b+g)/3))
                elif BrightnessMapping.lower() == 'lightness':
                    value = (max(r,g,b)+min(r,g,b))/2
                elif BrightnessMapping.lower() == 'luminosity':
                    value = round(0.21*r + 0.72*g + 0.07*b)
            except:
                try:
                    c,y,m,k = img.getpixel((j,i))
                    value = round((c+y+m+k)/4)
                except:
                    value = img.getpixel((j,i))

            row.append(value)
        pixels.append(row)


    characters = '`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'[::-1]
    unit = 255/len(characters)
    AsciiArt = []
    for x in range(len(pixels)):
        row = []
        for y in range(len(pixels[x])):
            pixel = pixels[x][y]
            scale = round(pixel/unit)
            if scale == 65: scale = 64
            letter = characters[scale]
            row.append(letter)
            
        AsciiArt.append(row)

    with open(outfile+'.txt', 'w') as output:
        for x in range(len(AsciiArt)):
            output.write('\n')
            for y in range(len(AsciiArt[x])):
                output.write(AsciiArt[x][y]*width)
    print('exported to ' +outfile+'.txt')
    menu()
    
    



menu()

