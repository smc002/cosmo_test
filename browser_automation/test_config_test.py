import unittest, time, shutil
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os, os.path, sys
import win32process, win32event, win32api, win32con, win32com.client
import logging
from ea_auto import item_click as ea_click, ea_start, ea_close, ea_config, ea_wait_process_end, ea_config_procedure
from removeall import removeall

log_path = r'C:\cosmo_auotest\test3'
log_file = os.path.join(log_path, 'system log.html')
config_path = r'C:\Users\Public\Documents\National Instruments\Test Integration Adapter 1.0'
config_file = os.path.join(config_path, 'Configuration.ini')
active_str = 'Client State Changed From REGISTRATION To ACTIVE'

class COSMO_test_case_config(unittest.TestCase):

    def setUp(self):
        if not os.path.exists(log_path):
            os.mkdir(log_path)
        shutil.copy(r'./Configuration.ini', config_file)
        pass

    def config_test(self, opt, inp_str, veri_keyword, delay=10, expect_result=True):
        ea_config_procedure(opt, inp_str, delay, log_path, log_file)
        logger = logging.getLogger("COSMO.ea.config")
        ea_wait_process_end()
        if not os.path.isfile(log_file):
            logger.error('EA\'s log file not found in {}'.format(log_file))
            return False

        keyword_found = False
        with open(log_file, 'rt') as f:
            logger.debug(f.read())
        with open(log_file, 'rt') as f:
            keyword_found = veri_keyword in f.read()
        try:
            self.assertTrue(keyword_found == expect_result, veri_keyword + ' not found in log')
        except AssertionError as e:
            logger.critical('{} = {}, test FAILED.'.format(opt, inp_str))
            logger.critical(str(e))
        except Exception as e:
            logger.critical('{} = {}, UNKOWN ERROR.'.format(opt, inp_str))
            logger.critical(str(e))
        else:
            logger.critical('{} = {}, test PASSED.'.format(opt, inp_str))
        return keyword_found == expect_result

# This test would be failed. Possible reason is too many failed try of login would cause connect-refuse from server.
    '''def test_config_password(self):
        pwd_kwd_pair = {
                'test'                  : 'Client State Changed From REGISTRATION To ACTIVE',
                'test_wrong_password'   : 'LOGIN FAILED' ,
                }
        for pwd in pwd_kwd_pair:
            test_passed = self.config_test(self, 'password', pwd, pwd_kwd_pair[pwd])
            test_passed = self.config_test(self, 'username', pwd, pwd_kwd_pair[pwd])'''

    def test_config_server(self):
        right_server = [
                '10.144.10.217:9443/qm',
                'https://10.144.10.217:9443/qm',
                ]
        wrong_server = [
                'https://10.145.10.217:9443/qm',
                ]
        for ser in wrong_server:
            test_passed = self.config_test('server', ser, active_str, expect_result=False)
        for ser in right_server:
            test_passed = self.config_test('server', ser, active_str)

    def tearDown(self):
        try:
            ea_close()
        except:
            pass
        pass
        #self.driver.close()

def ea_start_close_test():
    for i in range(100):
        logger.critical('test begin.')
        ea_start(delay=10)
        logger.critical('test end.')
        ea_close(delay=10)

if __name__ == "__main__":
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    logging_file = os.path.join(log_path, 'test_config.log')
    print("Logging to", logging_file)

    logger = logging.getLogger('COSMO.ea')
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(logging.Formatter('%(asctime)s : %(levelname)s : %(message)s'))
    logger.addHandler(ch)

    logger2 = logging.getLogger('COSMO')
    logger2.setLevel(logging.DEBUG)
    ch2 = logging.StreamHandler(open(logging_file,'at'))
    ch2.setLevel(logging.INFO)
    ch2.setFormatter(logging.Formatter('%(asctime)s : %(levelname)s : %(message)s'))
    logger2.addHandler(ch2)

    #ea_start_close_test()
    unittest.main(verbosity=2, exit=False)
