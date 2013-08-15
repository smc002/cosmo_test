import win32api, win32con
import time

normal_keys = {
        '/' : 0xBF,
        '\\' : 0xDC,
        '-' : 0xBD,
        ';' : 0xBA,
        ',' : 0xBC,
        '.' : 0xBE,
        }

shift_keys = {
        ':' : 0xBA,
        '_' : 0xBD,
        '<' : 0xBC,
        '>' : 0xBE,
        '?' : 0xBF,
        '(' : ord('9'),
        ')' : ord('0'),
        }

def keybd_clear(times):
    for i in range(0, times):
        win32api.keybd_event(8, 0, 0, 0)
        time.sleep(0.03)
        win32api.keybd_event(8, 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(0.03)

def shift_type(vk_code):
    win32api.keybd_event(0x10, 0, 0, 0)
    win32api.keybd_event(vk_code, 0, 0, 0)
    time.sleep(0.03)
    win32api.keybd_event(vk_code, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(0x10, 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(0.03)

def normal_type(vk_code):
    win32api.keybd_event(vk_code, 0, 0, 0)
    time.sleep(0.03)
    win32api.keybd_event(vk_code, 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(0.03)

def keybd_type(inp_str):
    for s in inp_str:
        #print(s, ord(s))
        if s.isupper():
            shift_type(ord(s))
        elif s.islower():
            normal_type(ord(s.upper()))
        elif s in normal_keys:
            normal_type(normal_keys[s])
        elif s in shift_keys:
            shift_type(shift_keys[s])
        else:
            win32api.keybd_event(ord(s), 0, 0, 0)
            win32api.keybd_event(ord(s), 0, win32con.KEYEVENTF_KEYUP, 0)
