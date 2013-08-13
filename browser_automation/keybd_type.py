import win32api, win32con

def shift_type(vk_code):
    win32api.keybd_event(0x10, 0, 0, 0)
    win32api.keybd_event(vk_code, 0, 0, 0)
    win32api.keybd_event(vk_code, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(0x10, 0, win32con.KEYEVENTF_KEYUP, 0)

def normal_type(vk_code):
    win32api.keybd_event(vk_code, 0, 0, 0)
    win32api.keybd_event(vk_code, 0, win32con.KEYEVENTF_KEYUP, 0)

def keybd_type(inp_str):
    for s in inp_str:
        print(s, ord(s))
        if s.isupper():
            shift_type(ord(s))
        elif s.islower():
            normal_type(ord(s.upper()))
        elif s == '/':
            normal_type(0xBF)
        elif s == ':':
            shift_type(0xBA)
        else:
            win32api.keybd_event(ord(s), 0, 0, 0)
            win32api.keybd_event(ord(s), 0, win32con.KEYEVENTF_KEYUP, 0)
