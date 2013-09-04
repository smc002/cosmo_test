from ea.ea_keybd_type import keybd_type, keybd_clear, normal_type
from ea.ea_auto import focus_window
import time, logging

def try_to_focus_window(title):
    logger = logging.getLogger("COSMO.ts")
    logger.info('Looking for the window: {}.'.format(title))
    for i in range(20):
        win = focus_window(title=title, suppress_warning=True)
        if win != 0:
            logger.info('Window: {} found.'.format(title))
            return
    else:
        logger.warning('Window: {} not found.'.format(title))

def ts_test_case_1():
    r''' handle the click operation needed for C:\Users\Public\Documents\National Instruments\TestStand 2012\Examples\Demo\C\computer.seq .'''


    try_to_focus_window('About This Example')
    normal_type(0x0D) # 0x0D is the ENTER key.
    try_to_focus_window('Test Simulator')
    normal_type(0x0D)
    time.sleep(10)
