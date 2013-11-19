from ea_keybd_type import keybd_type, keybd_clear, normal_type
from ea_auto import focus_window, try_to_focus_window, closeWindowWithMouse
from constant_utility import time_sleep, ts_path, ts_name
import time, logging, os
import win32process

def ts_test_case_1():
    r''' handle the click operation needed for C:\Users\Public\Documents\National Instruments\TestStand 2012\Examples\Demo\C\computer.seq .'''
    try_to_focus_window('About This Example')
    normal_type(0x0D) # 0x0D is the ENTER key.
    try_to_focus_window('Test Simulator')
    normal_type(0x0D)
    time_sleep(10)

def ts_close():
    logger = logging.getLogger("COSMO.ts.auto")
    closed = False
    for i in range(1,10):
        logger.debug('try to find ts window')
        win = focus_window('NI TestStand - Sequence Editor [Edit]')
        if win != 0:
            logger.debug('try to close ts')
            try:
                closeWindowWithMouse(win)
            except:
                continue
            time_sleep(10)
            normal_type(0x0D) # 0x0D is the ENTER key.
            closed = True
        else:
            return closed
    return closed

def ts_start(delay=0):
    win32process.CreateProcess(
            os.path.join(ts_path, ts_name),
            '', None, None, 0,
            win32process.CREATE_NO_WINDOW,
            None,
            ts_path,
            win32process.STARTUPINFO())
    if try_to_focus_window('Compatibility'):
        normal_type(0x0D) # 0x0D is the ENTER key.
    if try_to_focus_window('Login'):
        normal_type(0x0D) # 0x0D is the ENTER key.
    time_sleep(delay)
    return
