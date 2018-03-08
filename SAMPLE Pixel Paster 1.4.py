#file name      :Pixel Paster 1.4.py
#author         :Stellarend
#date           :5.25.2016
#python version :2.7.10
#notes          :Download pywin32 aswell as the python image library
#               :Set ingame mouse sensitivity to 100%

#import libraries
from PIL import Image
import time
import win32api, win32con
import math

#global variables and constants
TO_PIX = 180/math.pi/0.15
COL_MAP = {0:[72.5, 57.5],
           1:[72.5, 55.5],
           2:[72.5, 53.5],
           3:[70.5, 57.5],
           4:[70.5, 55.5],
           5:[70.5, 53.5],
           6:[68.5, 57.5],
           7:[68.5, 55.5],
           8:[68.5, 53.5]}

#classes
class Mouse:
    def move(self, x, y):
        win32api.SetCursorPos((x, y))

    def left_click(self):
        for i in xrange(20):
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0)
            time.sleep(CS)
        for i in xrange(20):
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0)
            time.sleep(CS)

    def right_down(self):
        for i in xrange(20):
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0,0)
            time.sleep(CS)

    def right_up(self):
        for i in xrange(20):
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0,0)
            time.sleep(CS)

    def right_click(self):
        for i in xrange(20):
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0,0)
            time.sleep(CS)
        for i in xrange(20):    
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0,0)
            time.sleep(CS)

    def get_pos(self):
        return win32api.GetCursorPos()

#objects
mouse = Mouse()

#functions
def press_key(vkCode):
    win32api.keybd_event(vkCode, 0,0,0)

def release_key(vkCode):
    win32api.keybd_event(vkCode,0 ,win32con.KEYEVENTF_KEYUP ,0)
    
#x(float)the x-coord of the block you are trying to get to
#y(float)the y-coord of the block you are trying to get to
def go_to_block(x, y):
    global overflow, curAngle
    mousePos = mouse.get_pos()
    thetaX = math.atan((x-39.0)/17.036) * TO_PIX
    thetaY = math.atan((y-25.5)/math.sqrt((x-39.0)**2 +17.036**2)) * TO_PIX
    deltaThetaX = (thetaX - curAngle[0])
    deltaThetaY = (thetaY - curAngle[1])
    cutX = round(deltaThetaX)
    cutY = round(deltaThetaY)
    overflow[0] += deltaThetaX - cutX
    overflow[1] += deltaThetaY - cutY
    cutX += overflow[0] - (overflow[0] % 1)
    cutY += overflow[1] - (overflow[1] % 1)
    overflow[0] %= 1
    overflow[1] %= 1
    mouse.move(int(mousePos[0] + cutX), int(mousePos[1] + cutY))
    curAngle = [thetaX, thetaY]

#main program
source = raw_input('Enter image name (.jpg only) or "end": ')
while source != 'end':
    if source[-4:-1]+source[-1] != '.jpg':
        source += '.jpg'
    picture = Image.open(source)
    picture.resize((79, 52), Image.ANTIALIAS)
    img = picture.load()
    colList = [[] for i in xrange(9)]
    old_grey = int(round(sum(img[0, 0]) / 96.0))
    
    print 'Analyzing Image'
    for y in xrange(52):
        #if y value is odd
        if y % 2:
            start = 78
            for x in xrange(78, -1, -1):
                grey = int(round(sum(img[x, y]) / 96.0))

                #check if the streak of colors ended
                if grey != old_grey:
                    colList[old_grey].append([start, y, x + 1])
                    old_grey = grey
                    x1 = x
                    start = x
                    
            #cut off streak when end streak
            colList[old_grey].append([start, y, x])
        #if y value is even 
        else:
            start = 0
            for x in xrange(0, 79, 1):
                grey = int(round(sum(img[x, y]) / 96.0))

                #check if the streak of colors ended
                if grey != old_grey:
                    colList[old_grey].append([start, y, x - 1])
                    old_grey = grey
                    start = x

            #cut off streak when end streak
            colList[old_grey].append([start, y, x])
    colList.pop()
    print 'Image Analyzed'
    
    time.sleep(1)
    print 'Commencing in 5'
    time.sleep(1)
    print 'Commencing in 4'
    time.sleep(1)
    print 'Commencing in 3'
    time.sleep(1)
    print 'Commencing in 2'
    time.sleep(1)
    print 'Commencing in 1'
    time.sleep(1)
    print 'Painting'

    total = 0
    for color in xrange(len(colList)):
        total += len(colList[color])

    CS = 5.0/total #click speed
    
    press_key(0xA2)
    press_key(0x57) 
    time.sleep(.8)
    release_key(0x57)
    release_key(0xA2)
    press_key(0x53)
    time.sleep(.5)
    release_key(0x53)
    time.sleep(.25)

    curAngle = [0.0, 0.6]
    overflow = [0.0, 0.0]

    go_to_block(COL_MAP[8][0], COL_MAP[8][1])
    time.sleep(0.200)
    mouse.right_click()
    go_to_block(39.0, 25.5)
    time.sleep(0.200)
    go_to_block(31.5, -8)
    time.sleep(0.200)
    mouse.left_click()
    go_to_block(32.5, 5)
    time.sleep(0.200)
    mouse.right_click()
    go_to_block(-4.0, -8)
    time.sleep(0.200)
    mouse.left_click()
    go_to_block(-3.0, 13.5)
    time.sleep(0.200)
    go_to_block(39.0, 25.5)
    time.sleep(0.200)

    for color in xrange(len(colList)):#dont color white cause background is already white
        go_to_block(COL_MAP[color][0], COL_MAP[color][1])
        time.sleep(0.200)
        mouse.right_click()
        go_to_block(51.6, 33.6)
        time.sleep(0.200)
        go_to_block(25.3, 16.3)
        time.sleep(0.200)
        
        for line in colList[color]:
            go_to_block(line[0], line[1])
            mouse.right_down()
            go_to_block(line[2], line[1])
            mouse.right_up()
        
    source = raw_input('Enter image name (.jpg only) or "end": ')

print "Program Terminated"
