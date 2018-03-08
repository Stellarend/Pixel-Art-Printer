from PIL import Image
import ctypes
from ctypes import wintypes
import time

source = raw_input('Enter image name (.jpg only): ')
if source[-4:-1]+source[-1] != '.jpg':
    source += '.jpg'
im = Image.open(source)

pix = im.load()

guidelines = raw_input('Guidelines on? (yes/no): ').lower()

user32 = ctypes.WinDLL('user32', use_last_error=True)

INPUT_MOUSE    = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP       = 0x0002
KEYEVENTF_UNICODE     = 0x0004
KEYEVENTF_SCANCODE    = 0x0008

timePassed = 0

MAPVK_VK_TO_VSC = 0

# msdn.microsoft.com/en-us/library/dd375731
VK_TAB  = 0x09
VK_MENU = 0x12

# C struct definitions

wintypes.ULONG_PTR = wintypes.WPARAM

class MOUSEINPUT(ctypes.Structure):
    _fields_ = (("dx",          wintypes.LONG),
                ("dy",          wintypes.LONG),
                ("mouseData",   wintypes.DWORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))

class KEYBDINPUT(ctypes.Structure):
    _fields_ = (("wVk",         wintypes.WORD),
                ("wScan",       wintypes.WORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))

    def __init__(self, *args, **kwds):
        super(KEYBDINPUT, self).__init__(*args, **kwds)
        # some programs use the scan code even if KEYEVENTF_SCANCODE
        # isn't set in dwFflags, so attempt to map the correct code.
        if not self.dwFlags & KEYEVENTF_UNICODE:
            self.wScan = user32.MapVirtualKeyExW(self.wVk,
                                                 MAPVK_VK_TO_VSC, 0)

class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (("uMsg",    wintypes.DWORD),
                ("wParamL", wintypes.WORD),
                ("wParamH", wintypes.WORD))

class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = (("ki", KEYBDINPUT),
                    ("mi", MOUSEINPUT),
                    ("hi", HARDWAREINPUT))
    _anonymous_ = ("_input",)
    _fields_ = (("type",   wintypes.DWORD),
                ("_input", _INPUT))

LPINPUT = ctypes.POINTER(INPUT)

def _check_count(result, func, args):
    if result == 0:
        raise ctypes.WinError(ctypes.get_last_error())
    return args

user32.SendInput.errcheck = _check_count
user32.SendInput.argtypes = (wintypes.UINT, # nInputs
                             LPINPUT,       # pInputs
                             ctypes.c_int)  # cbSize

# Functions

def PressKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode,
                            dwFlags=KEYEVENTF_KEYUP))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

def moveDown():
    time.sleep(0.1)
    PressKey(0xA0)
    PressKey(0x53)
    time.sleep(0.782)
    ReleaseKey(0x53)
    ReleaseKey(0xA0)
    time.sleep(0.1)

def rightClick():
    ctypes.windll.user32.mouse_event(8, 0, 0, 0,0)
    time.sleep(.005)
    ctypes.windll.user32.mouse_event(16, 0, 0, 0,0)

def press1():
    PressKey(0x31)
    time.sleep(.005)
    ReleaseKey(0x31)

def press2():
    PressKey(0x32)
    time.sleep(.005)
    ReleaseKey(0x32)

def press3():
    PressKey(0x33)
    time.sleep(.005)
    ReleaseKey(0x33)

def press4():
    PressKey(0x34)
    time.sleep(.005)
    ReleaseKey(0x34)
    
def press5():
    PressKey(0x35)
    time.sleep(.005)
    ReleaseKey(0x35)

def press6():
    PressKey(0x36)
    time.sleep(.005)
    ReleaseKey(0x36)

def press7():
    PressKey(0x37)
    time.sleep(.005)
    ReleaseKey(0x37)

def press8():
    PressKey(0x38)
    time.sleep(.005)
    ReleaseKey(0x38)

def select(coord):
    total = coord[0] + coord[1] + coord[2]
    if total <= 318:
        if total <= 131:
            if total <= 64: press8()
            else: press7()
        else:
            if total <= 226: press6()
            else: press5()
    else:
        if total <= 572:
            if total <= 426: press4()
            else: press3()
        else:
            if total <= 704: press2()
            else: press1()

etc = im.size[0] * 0.23164 * im.size[1] + im.size[1] * (0.982 + .074)

print '''
1. Make sure your rotation is exactly a multiple of 90 exactly
2. Have an angle of about 55 degrees to the block infront of you
3. Stand near the middle of the a block slightly to the bottom left
4. Make sure the path behind you is clear

Source                          : %s
Image Size (pixels)             : %i, %i
Estimated Time of Completion    : %.0f seconds (%.2f minutes)'''%(source, im.size[0], im.size[1], etc, etc/60)

if raw_input('\nType start to commence: ').lower() == 'start':
    print '\nCommencing in:'
    time.sleep(1)
    print '5'
    time.sleep(1)
    print '4'
    time.sleep(1)
    print '3'
    time.sleep(1)
    print '2'
    time.sleep(1)
    print '1\n'
    
       
    for y in range(0, im.size[1], 2):


        PressKey(0x44)
        select(pix[0, y])
        rightClick()
        time.sleep(.072)
        
        for x in range(1, im.size[0]):
            time.sleep(0.22164)
            c = pix[x, y]
            select(c)
            rightClick()

        if guidelines == 'yes':
            time.sleep(0.1)
            timePassed += 0.1
            
        ReleaseKey(0x44)
        timePassed += (im.size[0] * 0.22164) + 0.074
        print '%3.0f%% complete %7.0f seconds passed' %(float(y + 1)/im.size[1]*100.0, timePassed)
        moveDown()

        PressKey(0x41)
        select(pix[im.size[0]-1, y])
        rightClick()
        time.sleep(.072)
        
        for x in range(1, im.size[0]):
            time.sleep(0.22164)
            c = pix[im.size[0] - x - 1, y + 1]
            select(c)
            rightClick()

        if guidelines == 'yes':
            time.sleep(0.1)
            timePassed += 0.1

        ReleaseKey(0x41)
        timePassed += (im.size[0] * 0.22164) + 0.074
        print '%3.0f%% complete %7.0f seconds passed' %(float(y + 2)/im.size[1]*100.0, timePassed)    
        moveDown()
        
print '\nCompleted'

raw_input('Type anything to quit')
