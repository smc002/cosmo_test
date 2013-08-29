import unittest, time, logging, ctypes
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os, os.path, sys
from removeall import removeall
import ea_auto, browser_auto

test_name = 'normal_test'
test_root_folder = 'C:\\cosmo_autotest\\'
if not os.path.exists(test_root_folder):
    os.mkdir(test_root_folder)
log_path = test_root_folder + test_name + '\\'
if not os.path.exists(log_path):
    os.mkdir(log_path)

def repeat(times):
    def repeatHelper(f):
        def callHelper(*args):
            for i in range(0, times):
                f(*args)
        return callHelper
    return repeatHelper

class COSMO_test_case_1(unittest.TestCase):

    def setUp(self):
        ea_auto.ea_start()
        #self.driver = webdriver.Firefox()
        #self.driver.implicitly_wait(10)

    #@repeat(100)
    def test_normal_test(self):
        log = logging.getLogger("COSMO.normal")
        passed = browser_auto.run_normal_test()
        self.assertTrue(passed, 'Browser Automation Failed!')

    def tearDown(self):
        time.sleep(15)
        ea_auto.ea_close()
        pass
        #self.driver.close()

if __name__ == "__main__":
    cnt = 0
    logging_file = os.path.join(log_path, 'py_test.log')
    print("Logging to", logging_file)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s : %(levelname)s : %(message)s',
        filename = logging_file,
        filemode = 'a',
        )
    log = logging.getLogger("COSMO")
    while cnt < 1:
        cnt += 1
        log.info("Normal Test No.{} begin.".format(cnt))
        try:
            unittest.main(verbosity=2, exit=False)
        except:
            log.error("An unexpected exception is detected.")
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
