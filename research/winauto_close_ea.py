import win32gui, win32api, win32con
import time, ctypes

title = 'NI Execution Adapter for IBM Rational Quality Manager'
position_close = [408, 471]

win = win32gui.FindWindow(None, title)
if win == 0:
    print('window not found!')
print(win)
ctypes.windll.user32.SwitchToThisWindow(win, True)
ctypes.windll.user32.SetFocus(win)
##(left, top, right, bottom) = win32gui.GetWindowRect(hedit)
position_ref = win32gui.GetWindowRect(win)
print(position_ref)
position_ref = position_ref[0:2]
print(position_ref)

def mouse_click(position):
    position[0] += position_ref[0]
    position[1] += position_ref[1]
    win32api.SetCursorPos((position[0], position[1]))
    #time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

#win32api.SetCursorPos((position_ref[0]+position_close[0],position_ref[1]+position_close[1]))
time.sleep(0.1)
mouse_click(position_close)
win32api.mouse
