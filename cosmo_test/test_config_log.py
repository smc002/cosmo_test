import unittest, time, shutil, datetime, glob
import os, os.path, sys
import logging
from ea.ea_auto import item_click as ea_click, ea_start, ea_close, ea_config, ea_wait_process_end
import browser.browser_auto as browser_auto
from constant_utility import test_root_folder, config_file, active_kwd_list, task_executed_kwd_list, tps_state_str, initialize_test_folders, lookup_keyword_in_ea_log, removeall


test_name = 'config_log'
TEST_REPEAT = 1
ea_log_path, ea_log_file, logger = initialize_test_folders(test_name)

class COSMO_test_case_config_log(unittest.TestCase):

    def setUp(self):
        shutil.copy('ea/Configuration.ini', config_file)
        pass

# log file test
    def test_config_log(self):
        logger = logging.getLogger("COSMO.config.log")
        tps_name = 'Configurations of log file'
        # initialize
        tps_step = 'Initialize log path'
        logger.critical(tps_state_str.format(tps_name, tps_step, 'BEGIN'))
        ea_start(delay=15)
        ea_config('folder', ea_log_path)
        ea_close()
        # step 1-2
        removeall(ea_log_path)
        tps_step = '1 - 2'
        logger.critical(tps_state_str.format(tps_name, tps_step, 'BEGIN'))
        ea_start(delay=15)
        ea_close()
        try:
            self.assertTrue(os.path.exists(ea_log_file), 'EA log: {} not found!'.format(ea_log_file))
            self.assertTrue(lookup_keyword_in_ea_log(active_kwd_list, ea_log_file), 'Not all the keywords were found in EA log!')
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
        try:
            self.assertTrue(passed, 'Browser Automation Failed!')
            self.assertTrue(os.path.exists(ea_log_file), 'EA log: {} not found!'.format(ea_log_file))
            self.assertTrue(lookup_keyword_in_ea_log(active_kwd_list, ea_log_file), 'Not all the keywords were found in EA log!')
            self.assertTrue(lookup_keyword_in_ea_log(task_executed_kwd_list, ea_log_file), 'Not all the keywords were found in EA log!')
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
        removeall(ea_log_path)
        os.mkdir(ea_log_path_exists)
        ea_start(delay=15)
        ea_close()
        try:
            self.assertTrue(os.path.exists(ea_log_file_step4), 'EA log: {} not found!'.format(ea_log_file_step4))
            self.assertTrue(lookup_keyword_in_ea_log(active_kwd_list, ea_log_file_step4), 'Not all the keywords were found in EA log!')
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
        removeall(ea_log_path)
        ea_start(delay=15)
        ea_close()
        try:
            self.assertTrue(os.path.exists(ea_log_file_step5), 'EA log: {} not found!'.format(ea_log_file_step5))
            self.assertTrue(lookup_keyword_in_ea_log(active_kwd_list, ea_log_file_step5), 'Not all the keywords were found in EA log!')
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
        removeall(ea_log_path)
        ea_start(delay=15)
        ea_close()
        try:
            validate_str = datetime.datetime.now().strftime('system log %Y-%m-%d ') + '*.html' 
            validate_str = ea_log_path + validate_str
            logger.debug('Validate string is {}'.format(validate_str))
            files_found = glob.glob(validate_str)
            self.assertTrue(len(files_found) == 1, '{} of log(s) with {} format were found'.format(len(files_found), validate_str))
            ea_log_file_step6 = files_found[0]
            self.assertTrue(os.path.exists(ea_log_file_step6), 'EA log: {} not found!'.format(ea_log_file_step6))
            self.assertTrue(lookup_keyword_in_ea_log(active_kwd_list, ea_log_file_step6), 'Not all the keywords were found in EA log!')
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
    for cnt in range(TEST_REPEAT):
        unittest.main(verbosity=2, exit=False)
