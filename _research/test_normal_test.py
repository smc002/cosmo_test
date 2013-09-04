import unittest, time, shutil, datetime, glob
import os, os.path, sys
import logging
from ea.ea_auto import item_click as ea_click, ea_start, ea_close, ea_config, ea_wait_process_end
import browser.browser_auto as browser_auto
from constant_utility import test_root_folder, config_file, active_kwd_list, task_executed_kwd_list, tps_state_str, initialize_test_folders, lookup_keyword_in_ea_log, removeall


test_name = 'stress_test'
TEST_REPEAT = 100
ea_log_path, ea_log_file, autotest_log_file, debug_log_file = initialize_test_folders(test_name)

def repeat(times):
    def repeatHelper(f):
        def callHelper(*args):
            for i in range(0, times):
                f(*args)
        return callHelper
    return repeatHelper

class COSMO_test_case_stress(unittest.TestCase):

    def setUp(self):
        ea_start(15)

    #@repeat(100)
    def test_normal_test(self):
        passed = browser_auto.run_normal_test()
        self.assertTrue(passed, 'Browser Automation Failed!')

    def tearDown(self):
        time.sleep(10)
        ea_close()

if __name__ == "__main__":
    print("Logging to", autotest_log_file)
    print("Logging to", debug_log_file)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(logging.Formatter('%(asctime)s : %(levelname)s : %(message)s'))
    logger.addHandler(ch)

    ch2 = logging.StreamHandler(open(autotest_log_file,'at'))
    ch2.setLevel(logging.WARNING)
    ch2.setFormatter(logging.Formatter('%(asctime)s : %(levelname)s : %(message)s'))
    logger.addHandler(ch2)

    ch_debug = logging.StreamHandler(open(debug_log_file,'at'))
    ch_debug.setLevel(logging.DEBUG)
    ch_debug.setFormatter(logging.Formatter('%(asctime)s : %(levelname)s : %(message)s'))
    logger.addHandler(ch_debug)

    cnt = 0
    while cnt < TEST_REPEAT:
        cnt += 1
        logger.critical("Stress Test No.{} begin.".format(cnt))
        unittest.main(verbosity=2, exit=False)
        if cnt%100 == 0:
            time.sleep(2)  #delete temp file too hurry might prevent firefox from closing
            removeall(r'C:\Users\msun\AppData\Local\temp')  #the files here could be too large, if running for hours
    
    '''while 1:
        try:
            unittest.main(verbosity=2,exit=False)
        except:
            print("An exception is detected.")
            logging.warning("An exception is detected.")
            continue
        else:
            suc_cnt += 1
            print("Test {} successed.".format(suc_cnt))
            logging.info("Test {} successed.".format(suc_cnt))'''
