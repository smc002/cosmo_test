import win32process, win32event, win32api, win32con, win32com.client, win32gui
import time, ctypes
import os, os.path, sys
import configparser

title = 'NI Execution Adapter for IBM Rational Quality Manager'
ea_path = r'C:\Program Files (x86)\National Instruments\Test Integration Adapter 1.0'
ea_name = 'Test Integration Adapter.exe'

positions = {}
config = configparser.ConfigParser()
config.read('ea_positions.ini')
positions = dict(config['login'])
for n in positions:
    pos = positions[n].split(',')
    pos = [int(x) for x in pos]
    positions[n] = pos

def focus_window():
    win = win32gui.FindWindow(None, title)
    if win == 0:
        print('window not found!')
    ctypes.windll.user32.SwitchToThisWindow(win, True)
    ctypes.windll.user32.SetFocus(win)
    return win

def mouse_click(position):
    win = focus_window()
    position_ref = win32gui.GetWindowRect(win)

    position[0] += position_ref[0]
    position[1] += position_ref[1]
    time.sleep(0.03)
    win32api.SetCursorPos((position[0], position[1]))
    time.sleep(0.03)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.03)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def ea_close():
    time.sleep(0.1)
    mouse_click(positions['close'])

def ea_start():
    handle = win32process.CreateProcess(
        os.path.join(ea_path, ea_name),
        '', None, None, 0,
        win32process.CREATE_NO_WINDOW,
        None,
        ea_path,
        win32process.STARTUPINFO())

def keybd_clear(times):
    for i in range(0, times):
        win32api.keybd_event(8, 0, 0, 0)
        win32api.keybd_event(8, 0, win32con.KEYEVENTF_KEYUP, 0)

def keybd_type(inp_str):
    for s in upper(inp_str):
        print(s, ord(s))
        win32api.keybd_event(ord(s), 0, 0, 0)
        win32api.keybd_event(ord(s), 0, win32con.KEYEVENTF_KEYUP, 0)


def test_positions():
    ea_start()
    time.sleep(5)
    for n in positions:
        if n == 'close':
            continue
        print(n)
        mouse_click(positions[n])
        time.sleep(2)
    ea_close()

def test_keybd():
    ea_start()
    time.sleep(1)
    mouse_click(positions['server'])
    keybd_clear(20)
    keybd_type(r' / ABC123')

if __name__ == "__main__":
    ea_start()
    time.sleep(20)
    ea_close()
