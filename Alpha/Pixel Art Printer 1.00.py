# program version   : Alpha 1.00
# python version    : 3.6.3
# date              : 2018.03.07

import win32api, win32con, time
from PIL import Image

# the time to hold down keys, default = 0.005, max should be 0.017 which is 1 frame
holdTime = 0.005
# the index of the currently selected toolbar with range [0,8]
selectedToolbar = 0
# the index of the currently selected block with range [0, 7]
selectedBlock = 0
# map of the blocks and their color. Index corresponds to toolbar and pos
blockMap = (
    (), # Toolbar 0
    (), # Toolbar 1
    (), # Toolbar 2
    (), # Toolbar 3
    (), # Toolbar 4
    (), # Toolbar 5
    (), # Toolbar 6
    (), # Toolbar 7
    ()) # Toolbar 8

# map of the key which corresponds to indexs used
# vk code list can be found here:
# https://msdn.microsoft.com/en-us/library/windows/desktop/dd375731(v=vs.85).aspx
keyMap = (0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39)

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
    # try to find the block with the most similar color
    bestDifference = 9999
    bestToolbar = -1
    bestBlock = -1
    for i, toolbar in enumerate(blockMap):
        for j, blockColor in enumerate(blockMap[toolbar]):
            difference = abs(targetColor[0] - blockColor[0]) + abs(targetColor[1] - blockColor[1]) + abs(targetColor[2] - blockColor[2])
            # if this block is a better fit than the current best, make this the best
            if difference < bestDifference:
                bestDifference = difference
                bestToolbar = i
                bestBlock = j

    # select the appropriate toolbar if not already selected
    if bestToolbar != selectedToolbar:
        global selectedToolbar
        selectedToolbar = bestToolbar
        # hold down x to load toolbars
        press_key(0x58)
        time.sleep(holdTime)
        # press key to select toolbar
        press_key(keyMap[selectedToolbar])
        time.sleep(holdTime)
        release_key(keyMap[selectedToolbar])
        release_key(0x58)
    
    # select the appropriate block if not already selected
    if bestBlock != selectedBlock:
        global selectedBlock
        selectedBlock = bestBlock
        press_key(keyMap[selectedBlock])
        time.sleep(holdTime)
        release_key(keyMap[selectedBlock])

for i in range(5, 0, -1):
    print("Script will run in {}".format(i))
    time.sleep(1)

imgHeight = 1
for i in range(imgHeight, 0, -1):
    x = 0.3
    startTick = time.perf_counter()
    # hold "d" key to strafe right
    press_key(0x44)
    #while(x < 19.7): #whatever the max width is
    while(time.perf_counter() - startTick < 5):
        place_block()
    release_key(0x44)

    # vk code for "a" key is 0x41

#when above the middle of the block, switch to the next one
#since the block below should have been placed already so
#player can spam click right and place when reach the next block

input("Press enter key to exit . . . ")
