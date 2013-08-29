import win32process, win32event, win32api, win32con, win32com.client, win32gui
import time, ctypes

title = 'NI Execution Adapter for IBM Rational Quality Manager'
ea_path = r'C:\Program Files (x86)\National Instruments\Test Integration Adapter 1.0'
ea_name = 'Test Integration Adapter.exe'
position_close = [408, 471]

def mouse_click(position):
    win = win32gui.FindWindow(None, title)
    if win == 0:
        print('window not found!')
    ctypes.windll.user32.SwitchToThisWindow(win, True)
    ctypes.windll.user32.SetFocus(win)
    position_ref = win32gui.GetWindowRect(win)

    position[0] += position_ref[0]
    position[1] += position_ref[1]
    win32api.SetCursorPos((position[0], position[1]))
    #time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def ea_close():
    time.sleep(0.1)
    mouse_click(position_close)

def ea_start():
    handle = win32process.CreateProcess(
        os.path.join(ea_path, ea_name),
        '', None, None, 0,
        win32process.CREATE_NO_WINDOW,
        None,
        ea_path,
        win32process.STARTUPINFO())

if __name__ == "__main__":
    ea_start()
    time.sleep(20)
    ea_close()
