import unittest, time, shutil, datetime, glob
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
import browser_auto
from removeall import removeall

test_name = 'config_test'
test_root_folder = 'C:\\cosmo_autotest\\'
if not os.path.exists(test_root_folder):
    os.mkdir(test_root_folder)
ea_log_path = test_root_folder + test_name + '\\'
if not os.path.exists(ea_log_path):
    os.mkdir(ea_log_path)
ea_log_file = os.path.join(ea_log_path, 'system log.html')

config_path = r'C:\Users\Public\Documents\National Instruments\Test Integration Adapter 1.0'
config_file = os.path.join(config_path, 'Configuration.ini')
active_str = 'Client State Changed From REGISTRATION To ACTIVE'
active_kwd_list = ['Client State Changed From INITIALIZATION To LOGIN',
        'Client State Changed From LOGIN To REGISTRATION',
        'Client State Changed From REGISTRATION To ACTIVE',
        ]
task_executed_kwd_list = [
        'Process Task',
        'Finished Execution',
        ]

tps_state_str = 'TPS: {}, step: {}, state: {}'

def lookup_keyword_in_ea_log(keywords, ea_log=ea_log_file):
    if not os.path.exists(ea_log):
        logger.error('EA log file not found in {}'.format(ea_log))
        return False
    with open(ea_log, 'rt') as f:
        log_content = f.read()
    logger.debug(log_content)
    keyword_found = True
    for kwd in keywords:
        if not kwd in log_content:
            logger.info('Keyword {} is NOT found in EA log {}'.format(kwd, ea_log))
            keyword_found = False
        else:
            logger.info('Keyword {} is found in EA log {}'.format(kwd, ea_log))
    return keyword_found


class COSMO_test_case_config(unittest.TestCase):

    def setUp(self):
        shutil.copy(r'./Configuration.ini', config_file)
        pass

    def config_test(self, opt, inp_str, veri_keyword, delay=10, expect_result=True):
        ea_config_procedure(opt, inp_str, delay, ea_log_path, ea_log_file)
        logger = logging.getLogger("COSMO.ea.config")
        ea_wait_process_end()
        if not os.path.isfile(ea_log_file):
            logger.error('EA\'s log file not found in {}'.format(ea_log_file))
            return False

        keyword_found = False
        with open(ea_log_file, 'rt') as f:
            logger.debug(f.read())
        with open(ea_log_file, 'rt') as f:
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

# log file test
    def test_config_log(self):
        logger = logging.getLogger("COSMO.ea.config")
        tps_name = 'Configurations of log file'
        # initialize
        tps_step = 'Initialize log path'
        logger.critical(tps_state_str.format(tps_name, tps_step, 'BEGIN'))
        ea_start(delay=15)
        ea_config('folder', ea_log_path)
        ea_close()
        ea_wait_process_end()
        # step 1-2
        removeall(ea_log_path)
        tps_step = '1 - 2'
        logger.critical(tps_state_str.format(tps_name, tps_step, 'BEGIN'))
        ea_start(delay=15)
        ea_close()
        ea_wait_process_end()
        try:
            self.assertTrue(os.path.exists(ea_log_file), 'EA log: {} not found!'.format(ea_log_file))
            self.assertTrue(lookup_keyword_in_ea_log(active_kwd_list), 'Not all the keywords were found in EA log!')
        except AssertionError as e:
            logger.critical(tps_state_str.format(tps_name, tps_step, 'FAILED'))
            logger.critical(str(e))
        except Exception as e:
            logger.critical(tps_state_str.format(tps_name, tps_step, 'UNKOWN ERROR'))
            logger.critical(str(e))
        else:
            logger.critical(tps_state_str.format(tps_name, tps_step, 'PASSED'))
        # step 3
        removeall(ea_log_path)
        tps_step = '3'
        logger.critical(tps_state_str.format(tps_name, tps_step, 'BEGIN'))
        ea_start(delay=15)
        passed = browser_auto.run_normal_test()
        time.sleep(20)
        ea_close()
        ea_wait_process_end()
        try:
            self.assertTrue(passed, 'Browser Automation Failed!')
            self.assertTrue(os.path.exists(ea_log_file), 'EA log: {} not found!'.format(ea_log_file))
            self.assertTrue(lookup_keyword_in_ea_log(active_kwd_list), 'Not all the keywords were found in EA log!')
            self.assertTrue(lookup_keyword_in_ea_log(task_executed_kwd_list), 'Not all the keywords were found in EA log!')
        except AssertionError as e:
            logger.critical(tps_state_str.format(tps_name, tps_step, 'FAILED'))
            logger.critical(str(e))
        except Exception as e:
            logger.critical(tps_state_str.format(tps_name, tps_step, 'UNKOWN ERROR'))
            logger.critical(str(e))
        else:
            logger.critical(tps_state_str.format(tps_name, tps_step, 'PASSED'))
        # step 4
        tps_step = '4'
        logger.critical('TPS: {}, step: {}, test begin.'.format(tps_name, tps_step))
        ea_log_path_exists = ea_log_path + 'exists\\'
        ea_log_file_step4 = os.path.join(ea_log_path_exists, 'system log.html')
        ea_start(delay=15)
        ea_config('folder', ea_log_path_exists)
        ea_close()
        ea_wait_process_end()
        removeall(ea_log_path)
        os.mkdir(ea_log_path_exists)
        ea_start(delay=15)
        ea_close()
        ea_wait_process_end()
        try:
            self.assertTrue(os.path.exists(ea_log_file_step4), 'EA log: {} not found!'.format(ea_log_file_step4))
            self.assertTrue(lookup_keyword_in_ea_log(active_kwd_list, ea_log=ea_log_file_step4), 'Not all the keywords were found in EA log!')
        except AssertionError as e:
            logger.critical(tps_state_str.format(tps_name, tps_step, 'FAILED'))
            logger.critical(str(e))
        except Exception as e:
            logger.critical(tps_state_str.format(tps_name, tps_step, 'UNKOWN ERROR'))
            logger.critical(str(e))
        else:
            logger.critical(tps_state_str.format(tps_name, tps_step, 'PASSED'))
        # step 5
        tps_step = '5'
        logger.critical('TPS: {}, step: {}, test begin.'.format(tps_name, tps_step))
        ea_log_path_not_exists = ea_log_path + 'not_exists\\'
        ea_log_file_step5 = os.path.join(ea_log_path_not_exists, 'system log.html')
        ea_start(delay=15)
        ea_config('folder', ea_log_path_not_exists)
        ea_close()
        ea_wait_process_end()
        removeall(ea_log_path)
        ea_start(delay=15)
        ea_close()
        ea_wait_process_end()
        try:
            self.assertTrue(os.path.exists(ea_log_file_step5), 'EA log: {} not found!'.format(ea_log_file_step5))
            self.assertTrue(lookup_keyword_in_ea_log(active_kwd_list, ea_log=ea_log_file_step5), 'Not all the keywords were found in EA log!')
        except AssertionError as e:
            logger.critical(tps_state_str.format(tps_name, tps_step, 'FAILED'))
            logger.critical(str(e))
        except Exception as e:
            logger.critical(tps_state_str.format(tps_name, tps_step, 'UNKOWN ERROR'))
            logger.critical(str(e))
        else:
            logger.critical(tps_state_str.format(tps_name, tps_step, 'PASSED'))
        # step 6
        tps_step = '6'
        logger.critical('TPS: {}, step: {}, test begin.'.format(tps_name, tps_step))
        ea_start(delay=15)
        ea_click(item='file_name_time')
        ea_config('folder', ea_log_path)
        ea_close()
        ea_wait_process_end()
        removeall(ea_log_path)
        ea_start(delay=15)
        ea_close()
        ea_wait_process_end()
        try:
            validate_str = datetime.datetime.now().strftime('system log %Y-%m-%d ') + '*.html' 
            validate_str = ea_log_path + validate_str
            logger.debug('Validate string is {}'.format(validate_str))
            files_found = glob.glob(validate_str)
            self.assertTrue(len(files_found) == 1, '{} of log(s) with {} format were found'.format(len(files_found), validate_str))
            ea_log_file_step6 = files_found[0]
            self.assertTrue(os.path.exists(ea_log_file_step6), 'EA log: {} not found!'.format(ea_log_file_step6))
            self.assertTrue(lookup_keyword_in_ea_log(active_kwd_list, ea_log=ea_log_file_step6), 'Not all the keywords were found in EA log!')
        except AssertionError as e:
            logger.critical(tps_state_str.format(tps_name, tps_step, 'FAILED'))
            logger.critical(str(e))
        except Exception as e:
            logger.critical(tps_state_str.format(tps_name, tps_step, 'UNKOWN ERROR'))
            logger.critical(str(e))
        else:
            logger.critical(tps_state_str.format(tps_name, tps_step, 'PASSED'))


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
        ea_start(delay=15)
        logger.critical('test end.')
        ea_close(delay=10)

if __name__ == "__main__":
    py_log_file = os.path.join(test_root_folder, test_name + '.log')
    debug_log_file = os.path.join(test_root_folder, test_name + '_debug.log')
    print("Logging to", py_log_file)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(logging.Formatter('%(asctime)s : %(levelname)s : %(message)s'))
    logger.addHandler(ch)

    ch2 = logging.StreamHandler(open(py_log_file,'at'))
    ch2.setLevel(logging.WARNING)
    ch2.setFormatter(logging.Formatter('%(asctime)s : %(levelname)s : %(message)s'))
    logger.addHandler(ch2)

    ch_debug = logging.StreamHandler(open(debug_log_file,'at'))
    ch_debug.setLevel(logging.DEBUG)
    ch_debug.setFormatter(logging.Formatter('%(asctime)s : %(levelname)s : %(message)s'))
    logger.addHandler(ch_debug)

    #ea_start_close_test()

    unittest.main(verbosity=2, exit=False)
