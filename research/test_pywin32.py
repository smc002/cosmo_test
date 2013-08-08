import os, os.path, sys, time
import win32process, win32event, win32api, win32con, win32com.client
ea_path = r'C:\Program Files (x86)\National Instruments\Test Integration Adapter 1.0'
ea_name = 'Test Integration Adapter.exe'
handle = win32process.CreateProcess(
    os.path.join(ea_path, ea_name),
    '', None, None, 0,
    0,
    None,
    None,
    win32process.STARTUPINFO())
print(handle)
time.sleep(5)
handle[0].Close()
handle[1].Close()
