# program version   : Alpha 1.00
# python version    : 3.6.3
# date              : 2018.03.07

import win32api, win32con, time, requests, sys
from io import BytesIO
from PIL import Image

import random

#demo image:
#http://tutorials-cdn.pixelmator.com/gradient-tool/top.jpg

# the time to hold down keys, default = 0.005, max should be 0.017 which is 1 frame
holdTime = 0.005
# the index of the currently selected toolbar with range [0,8]
selectedToolbar = -1
# the index of the currently selected block with range [0, 7]
selectedBlock = -1
# map of the blocks and their color. Index corresponds to toolbar and pos
blockMap = (
((218, 213, 189),(130, 136, 147),(21, 21, 21),(8, 10, 15),(45, 47, 144),(95, 59, 31),(21, 119, 136),(55, 58, 62)),
((73, 91, 36),(37, 138, 200),(93, 168, 24),(169, 48, 159),(225, 99, 2),(212, 100, 141),(18, 21, 25),(63, 65, 154)),
((113, 77, 47),(35, 132, 146),(101, 115, 119),(95, 119, 38),(77, 183, 209),(111, 174, 38),(178, 72, 170),(226, 137, 44)),
((223, 146, 172),(126, 54, 169),(165, 55, 48),(138, 138, 130),(224, 226, 226),(226, 188, 47),(101, 32, 157),(143, 33, 33)),
((126, 126, 116),(207, 213, 214),(242, 176, 21),(0, 173, 160),(145, 239, 172),(216, 175, 45),(149, 91, 66),(37, 22, 16)),
((74, 59, 91),(77, 50, 36),(86, 90, 91),(57, 42, 36),(75, 82, 42),(112, 108, 138),(103, 117, 52),(149, 87, 108)),
((160, 83, 37),(160, 77, 78),(118, 69, 86),(142, 60, 46),(135, 106, 97),(209, 177, 161),(185, 132, 35),(53, 96, 155)),
((36, 20, 23),(111, 15, 17),(16, 16, 24),(241, 239, 233),(227, 38, 12),(56, 3, 5),(155, 75, 26),(177, 90, 33)),
((177, 90, 33),(199, 190, 141),(232, 223, 177),(255, 255, 255),(127, 127, 127),(171, 172, 167),(214, 185, 173),(108, 35, 162)))

# map of the key which corresponds to indexs used
# vk code list can be found here:
# https://msdn.microsoft.com/en-us/library/windows/desktop/dd375731(v=vs.85).aspx
keyMap = (0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39)

maxSpeed = 10.92 # max speed when flying
acceleration = maxSpeed * 0.75 #8.72 # in blocks/second^2

def press_key(vkCode):
    win32api.keybd_event(vkCode,0,0,0)

def release_key(vkCode):
    win32api.keybd_event(vkCode,0,win32con.KEYEVENTF_KEYUP,0)

def place_block():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0,0)
    time.sleep(holdTime)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0,0)
    time.sleep(holdTime)
    
def select_block(targetColor):
    global selectedToolbar, selectedBlock
    # try to find the block with the most similar color
    bestDifference = 9999
    bestToolbar = -1
    bestBlock = -1
    for i, toolbar in enumerate(blockMap):
        for j, blockColor in enumerate(toolbar):
            difference = abs(targetColor[0] - blockColor[0]) + abs(targetColor[1] - blockColor[1]) + abs(targetColor[2] - blockColor[2])
            # if this block is a better fit than the current best, make this the best
            if difference < bestDifference:
                bestDifference = difference
                bestToolbar = i
                bestBlock = j

    # select the appropriate toolbar if not already selected
    if bestToolbar != selectedToolbar:
        selectedToolbar = bestToolbar
        # hold down x to load toolbars
        press_key(0x58)
        time.sleep(holdTime*4)
        # press key to select toolbar
        press_key(keyMap[selectedToolbar])
        time.sleep(holdTime*4)
        release_key(keyMap[selectedToolbar])
        release_key(0x58)
    
    # select the appropriate block if not already selected
    if bestBlock != selectedBlock:
        selectedBlock = bestBlock
        press_key(keyMap[selectedBlock])
        time.sleep(holdTime*4)
        release_key(keyMap[selectedBlock])

#address = input("Address of image(local or from network): ")
address = ".\demoimg.jpg"
print("Retreving image . . .")
if address.startswith("http"):
    response = requests.get(address)
    img = Image.open(BytesIO(response.content))
else:
    img = Image.open(address)
print("Image retrieved\n\tsource width  : {}px\n\tsource height : {}px\n".format(img.width, img.height))

targetWidth = int(input("Target width(31 for solo, 43 for team): "))
maxHeight = int(input("Max height(default is 73): "))
print("Processing . . .")
targetHeight = min(round(float(targetWidth*img.height)/img.width), maxHeight)
img = img.resize((targetWidth, targetHeight), Image.LANCZOS)
print("Image processed\n\tprint width  : {} blocks\n\tprint height : {} blocks\n".format(targetWidth, targetHeight))

input("To exit script during runtime press \"end\" key\nPress enter key to begin countdown . . .")
for i in range(5, 0, -1):
    print("Printing will start in {}".format(i))
    time.sleep(1)

for i in range(targetHeight-1, -1, -1):
    speed = 0
    prevTime = time.perf_counter()
    tpl = 0
    if ((targetHeight - i)%2):
        x = 0.3
        block = 0
        select_block(img.getpixel((block, i)))
        # hold "d" key to strafe right
        press_key(0x44)
        while(x < targetWidth):
            currTime = time.perf_counter()
            tpl = currTime - prevTime
            prevTime = currTime

            speed += acceleration * tpl
            if speed > maxSpeed:
                speed = maxSpeed
            x += speed * tpl

            # trigger from block-0.5 to block+0.5
            if block+0.5 < x and block <targetWidth - 1:
                block += 1
                select_block(img.getpixel((block, i)))
                print(block)
                
            place_block()
            # if the end key is pressed, exit
            if win32api.GetKeyState(0x23):
                print("Script will now exit")
                sys.exit(0)
                exit()
        release_key(0x44)
    else:
        x = targetWidth - 0.3
        block = targetWidth - 1
        select_block(img.getpixel((block, i)))
        # hold "a" key to strafe left
        press_key(0x41)
        while(x > 0.5):
            currTime = time.perf_counter()
            tpl = currTime - prevTime
            prevTime = currTime

            speed -= acceleration * tpl
            if speed < -maxSpeed:
                speed = -maxSpeed
            x += speed * tpl

            # trigger from block-0.5 to block+0.5
            if block+0.5 > x and block > 0:
                block -= 1
                select_block(img.getpixel((block, i)))
                print(block)
            
            place_block()
            # if the end key is pressed, exit
            if win32api.GetKeyState(0x23):
                print("Script will now exit")
                sys.exit(0)
                exit()
        release_key(0x41)
    # hold space to increase elevation
    press_key(0x20)
    time.sleep(0.15)
    release_key(0x20)

#when above the middle of the block, switch to the next one
#since the block below should have been placed already so
#player can spam click right and place when reach the next block

input("Press enter key to exit . . .")
