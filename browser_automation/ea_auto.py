import win32process, win32event, win32api, win32con, win32com.client, win32gui
import time, ctypes
import os, os.path, sys
import configparser, logging
from ea_keybd_type import keybd_type, keybd_clear

title = 'NI Execution Adapter for IBM Rational Quality Manager'
ea_path = r'C:\Program Files (x86)\National Instruments\Test Integration Adapter 1.0'
ea_name = 'Test Integration Adapter.exe'
ea_tabs = ('_main', 'login', 'adapter', 'resources', 'http', 'upload', 'log')
logger = logging.getLogger("COSMO.ea.auto")

ea_handle = None
positions = {}
config = configparser.ConfigParser()
config.read('ea_positions.ini')
for tab in ea_tabs:
    positions[tab] = dict(config[tab])
    for n in positions[tab]:
        pos = positions[tab][n].split(',')
        pos = [int(x) for x in pos]
        positions[tab][n] = pos

def focus_window():
    win = win32gui.FindWindow(None, title)
    if win == 0:
        logger.warning('focus window failed, window not found!')
    ctypes.windll.user32.SwitchToThisWindow(win, True)
    ctypes.windll.user32.SetFocus(win)
    return win

def mouse_click(position):
    win = focus_window()
    position_ref = win32gui.GetWindowRect(win)
    #print('ea found', position_ref)

    time.sleep(0.03)
    win32api.SetCursorPos((position[0]+position_ref[0], position[1]+position_ref[1]))
    time.sleep(0.03)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.03)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def item_click(tab=None, item='_tab', delay=0):
    if None == tab:
        if '_tab' == item:
            logger.error('item = _tab is illegal')
            return False
        for tabgroup in positions:
            for n in positions[tabgroup]:
                if item == n:
                    logger.debug('item_click: tab = {}, item = {}, pos = {}'.format(tabgroup, n, positions[tabgroup][n]))
                    mouse_click(positions[tabgroup]['_tab'])
                    mouse_click(positions[tabgroup][n])
                    time.sleep(delay)
                    return True
        logger.error('item = {} not found'.format(item))
        return False

    if not tab in ea_tabs:
        logger.error('tab = {} not found'.format(item, tab))
        return False
    if not item in positions[tab]:
        logger.error('item = {} in tab = {} not found'.format(item, tab))
        return False

    #print(tab, item, positions[tab][item])
    logger.debug('item_click: tab = {}, item = {}, pos = {}'.format(tab, item, positions[tab][item]))
    if '_main' != tab:
        mouse_click(positions[tab]['_tab'])
    mouse_click(positions[tab][item])
    time.sleep(delay)
    return True

def clear_type(inp_str):
    logger.debug('clear_type: input string = {}'.format(inp_str))
    win = focus_window()
    keybd_clear(50)
    win = focus_window()
    keybd_type(inp_str)

def ea_config(opt, inp_str):
    item_click(item=opt)
    clear_type(inp_str)
    time.sleep(1)

def ea_wait_process_end():
    if ea_handle == None:
        return
    logger.info('looking for the process' + str(ea_handle)) 
    ver = win32process.GetProcessVersion(ea_handle[2])
    while ver != 0:
        if win32gui.FindWindow(None, title) != 0:
            logger.warning('Window of EA exists. Try to close it again.') 
            ea_close()
        time.sleep(3)
        ver = win32process.GetProcessVersion(ea_handle[2])
        logger.debug('Version of EA\'s process is ' + str(ver)) 
    logger.info('Process of EA is end')
    return

def ea_start_process():
    return win32process.CreateProcess(
            os.path.join(ea_path, ea_name),
            '', None, None, 0,
            win32process.CREATE_NO_WINDOW,
            None,
            ea_path,
            win32process.STARTUPINFO())

def ea_close(delay=0):
    #print(win32process.GetProcessVersion(ea_handle[2]))
    time.sleep(0.1)
    item_click('_main', 'close')
    logger.info('UI of EA is end')
    time.sleep(delay)

def ea_start(delay=0):
    # todo: look the thread of teststand
    global ea_handle
    if ea_handle != None:
        ea_wait_process_end()
        ea_handle = ea_start_process()
    else:
        ea_handle = ea_start_process()

#debug
    #print(win32process.GetThreadTimes(ea_handle[0]))
    #print(win32process.GetProcessId(ea_handle[0]))
    logger.debug('EA is started')
    time.sleep(delay)

def ea_config_procedure(opt, inp_str, delay, log_path, log_file):
    logger = logging.getLogger("COSMO.ea.config")
    logger.critical('{} = {}, test begin.'.format(opt, inp_str))
    ea_start(delay=10)
    ea_config(opt, inp_str)
    ea_config('folder', log_path)
    item_click('_main', 'apply', delay=1)
    item_click('log', 'file_name', delay=1)
    ea_close()
    ea_wait_process_end()
    logger.info("deleting EA's log file...")
    os.remove(log_file)
    logger.debug("delay = {}".format(delay))
    ea_start(delay=delay)
    ea_close(delay=10)


def test_positions():
    ea_start()
    time.sleep(5)
    for tabgroup in positions:
        if tabgroup == '_main':
            continue
        for n in tabgroup:
            print(tabgroup, n)
            item_click(positions[tabgroup][n])
            time.sleep(2)
    ea_close()

'''def test_positions_log():
    ea_start()
    time.sleep(5)
    for n in ('log', 'log_folder', 'log_file_name'):
        print(n)
        mouse_click(positions[n])
        time.sleep(2)
    ea_close()'''

def test_keybd():
    ea_start()
    time.sleep(5)
    #item_click('login', 'server')
    print(item_click(item='server'))
    clear_type(r'C:\cosmo_auotest\test1()_;')

def test_start_close():
    for i in range(0, 100):
        print('i = ', i)
        ea_start(10)
        print('\tEA created')
        ea_close()
        print('\tEA closed')

    print('CREATED!', ea_handle)
if __name__ == "__main__":
    #test_keybd()
    test_start_close()
