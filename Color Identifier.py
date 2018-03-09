from PIL import Image
import math
import os


sourceDir = './'+input('Source directory name: ')+'/'

originalImages = [file for file in os.listdir(sourceDir) if file.endswith('.png')]
print("{} images found\nProcessing...\n".format(len(originalImages)))

print ("((", end="")
for i, file in enumerate(originalImages):
    img = Image.open(sourceDir+file)
    bands = list(img.split())
    img = Image.merge("RGB", bands[0:3])
    img.resize((1, 1), Image.ANTIALIAS)
    color = img.getpixel((0, 0))
    print(color, end=",")
    if not((i+1) % 8):
        print("),\n(", end=",")
    
print("Job complete")
