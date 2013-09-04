import unittest, time, shutil, datetime, glob
import os, os.path, sys
import logging
from ea.ea_auto import item_click as ea_click, ea_start, ea_close, ea_config, ea_wait_process_end, ea_initialize_test
import browser.browser_auto as browser_auto
from constant_utility import test_root_folder, config_file, active_kwd_list, task_executed_kwd_list, tps_state_str, initialize_test_folders, lookup_keyword_in_ea_log, removeall


test_name = 'demo'
tps_name = 'This is a demo'
TEST_REPEAT = 1
ea_log_path, ea_log_file, logger = initialize_test_folders(test_name)

class COSMO_test_case_config_log(unittest.TestCase):

    def setUp(self):
        removeall(config_file)
        pass

    def test_config_log(self):
        logger = logging.getLogger("COSMO.config.log")
        # initialize
        tps_step = 'Initialization'
        logger.critical(tps_state_str.format(tps_name, tps_step, 'BEGIN'))
        ea_initialize_test(log_folder=ea_log_path, delay=5)
        logger.critical(tps_state_str.format(tps_name, tps_step, 'FINISHED'))
        input()
        # step 1
        removeall(ea_log_path)
        tps_step = '1'
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


    def tearDown(self):
        try:
            ea_close()
        except:
            pass
        pass
        #self.driver.close()

if __name__ == "__main__":
    for cnt in range(TEST_REPEAT):
        unittest.main(verbosity=2, exit=False)
