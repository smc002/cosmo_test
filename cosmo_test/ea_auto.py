import win32process, win32event, win32api, win32con, win32com.client, win32gui
import time, ctypes, shutil
import os, os.path, sys
import configparser, logging
from ea_keybd_type import keybd_type, keybd_clear, normal_type
from constant_utility import title, ea_path, ea_name, config_file, time_sleep
from constant_utility import default_server, default_username, default_password, default_project_area, default_adapter_name, default_resource_folder, default_log_folder 
import config_file

logger = logging.getLogger("COSMO.ea.auto")

ea_handle = None
positions = {}
config = configparser.ConfigParser()
config.read('ea_positions.ini')
ea_tabs = config.sections()
# ea_tabs = ('_main', 'login', 'adapter', 'resources', 'http', 'upload', 'log')
for tab in ea_tabs:
    positions[tab] = dict(config[tab])
    for n in positions[tab]:
        pos = positions[tab][n].split(',')
        pos = [int(x) for x in pos]
        positions[tab][n] = pos

def focus_window(title=title, suppress_warning=False):
    win = win32gui.FindWindow(None, title)
    if win == 0:
        if suppress_warning:
            logger.debug('focus window failed, window "{}" not found!'.format(title))
        else:
            logger.warning('focus window failed, window "{}" not found!'.format(title))
    ctypes.windll.user32.SwitchToThisWindow(win, True)
    ctypes.windll.user32.SetFocus(win)
    time_sleep(0.5)
    return win

def try_to_focus_window(title):
    logger.info('Try to find the window: {}.'.format(title))
    for i in range(40):
        win = focus_window(title=title, suppress_warning=True)
        if win != 0:
            logger.info('Window: {} found.'.format(title))
            return True
    else:
        logger.warning('Window: {} not found.'.format(title))
        return False

def mouse_click(position):
    win = focus_window()
    position_ref = win32gui.GetWindowRect(win)
    #print('ea found', position_ref)

    time_sleep(0.03)
    win32api.SetCursorPos((position[0]+position_ref[0], position[1]+position_ref[1]))
    time_sleep(0.03)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time_sleep(0.03)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    time_sleep(0.5)

def item_click(tab=None, item='_tab', delay=0.5):
    if None == tab:
        if '_tab' == item:
            logger.error('item = _tab is illegal')
            return False
        for tabgroup in positions:
            for n in positions[tabgroup]:
                if item == n:
                    logger.debug('item_click: tab = {}, item = {}, pos = {}'.format(tabgroup, n, positions[tabgroup]['_tab']))
                    mouse_click(positions[tabgroup]['_tab'])
                    mouse_click(positions[tabgroup][n])
                    time_sleep(delay)
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
    time_sleep(delay)
    return True

def clear_type(inp_str, clear_length=30):
    logger.debug('clear_type: input string = {}'.format(inp_str))
    win = focus_window()
    keybd_clear(clear_length)
    win = focus_window()
    keybd_type(inp_str)

def ea_config(opt, inp_str, clear_length=30):
    item_click(item=opt)
    if 'folder' in opt:
        clear_length = 80
    clear_type(inp_str, clear_length)
    time_sleep(0.5)
# Click twice on Aplly button
    item_click('_main', 'apply')
    item_click('_main', 'apply')

def ea_wait_process_end():
    if ea_handle == None:
        return
    logger.info('looking for the process' + str(ea_handle)) 
    ver = win32process.GetProcessVersion(ea_handle[2])
    while ver != 0:
        if win32gui.FindWindow(None, title) != 0:
            logger.warning('Window of EA exists. Try to close it again.') 
            ea_close()
        time_sleep(3)
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

def ea_close(delay=5):
    #print(win32process.GetProcessVersion(ea_handle[2]))
    time_sleep(0.1)
    item_click('_main', 'close')
    time_sleep(0.1)
# some prompt window (like "Cannot close TS auto...", which is added in cosmo 1.5 b5) could block for the click
    normal_type(0x0D) # 0x0D is the ENTER key.
    time_sleep(0.1)
    item_click('_main', 'close')
    logger.info('UI of EA is end')
    time_sleep(1)
    ea_wait_process_end()
    time_sleep(delay)

def ea_start(delay=0, handle_ts=True):
    # todo: look for the thread of teststand
    # todo: make sure thread of ea is not exist
    global ea_handle
    if ea_handle != None:
        ea_wait_process_end()
        ea_handle = ea_start_process()
    else:
        ea_handle = ea_start_process()
    logger.debug('EA is started')
    time_sleep(5)
    if handle_ts:
        if try_to_focus_window('Compatibility'):
            normal_type(0x0D) # 0x0D is the ENTER key.
        if try_to_focus_window('Login'):
            normal_type(0x0D) # 0x0D is the ENTER key.

    # item_click('_main', 'connect') EA GUI is not started yet, so could not click for now
    # todo: make sure the "auto connect" option is on or off
    time_sleep(delay)

def test_positions():
    ea_start()
    time_sleep(5)
    for tabgroup in positions:
        if tabgroup == '_main':
            continue
        for n in tabgroup:
            print(tabgroup, n)
            item_click(positions[tabgroup][n])
            time_sleep(2)
    ea_close()

'''def test_positions_log():
    ea_start()
    time_sleep(5)
    for n in ('log', 'log_folder', 'log_file_name'):
        print(n)
        mouse_click(positions[n])
        time_sleep(2)
    ea_close()'''

def test_keybd(): # todo: this function is for test only.
    ea_start()
    time_sleep(5)
    #item_click('login', 'server')
    print(item_click(item='server'))
    clear_type(r'C:\cosmo_auotest\test1()_;')

def test_start_close(): # todo: this function is for test only.
    for i in range(0, 100):
        print('i = ', i)
        ea_start(10)
        print('\tEA created')
        ea_close()
        print('\tEA closed')

    print('CREATED!', ea_handle)

def ea_initialize_test(
        server = default_server,
        username = default_username,
        password = default_password,
        project_area = default_project_area,
        adapter_name = default_adapter_name,
        resource_folder = default_resource_folder,
        log_folder = default_log_folder,
        delay=15):
# This function is outdated. Use ea.config_file.initialize instead.
    config_file.initialize(
        server = server,
        username = username,
        password = password,
        project_area = project_area,
        adapter_name = adapter_name,
        resource_folder = resource_folder,
        log_folder = log_folder,
        remove_original_file = False
        );

    # logger.info('Copying the default configuration file to ea config folder.')
    # shutil.copy('ea/Configuration.ini', config_file)

    # ea_start(delay=delay)
    # ea_config('server', server)
    # ea_config('username', username)
    # ea_config('password', password)
    # ea_config('project_area', project_area)
    # ea_config('adapter_name', adapter_name)
    # ea_config('resource_folder', resource_folder)
    # ea_config('folder', log_folder)
    # ea_close()
    # logger.info('Copying the new configuration file to script location: \'ea/Configuration.ini\', for further use.')
    # shutil.copy(config_file, 'ea/Configuration.ini')

def clickOnWindow(hld, pos):
    cursor_pos = win32gui.GetCursorPos()
    win32api.SetCursorPos(pos)

    win32gui.SetForegroundWindow(hld)
    time.sleep(0.2)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, pos[0], pos[1],0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, pos[0], pos[1],0,0)

    win32api.SetCursorPos(cursor_pos)

def closeWindowWithMouse(hld):
    rect = win32gui.GetWindowRect(hld)
    btn_pos = (rect[2]-10, rect[1]+10)
    clickOnWindow(hld, btn_pos)
    

if __name__ == "__main__":
    #test_keybd()
    test_start_close()
